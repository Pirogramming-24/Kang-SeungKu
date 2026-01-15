import os
import sys
import cv2
import numpy as np
import re
from paddleocr import PaddleOCR

# [경로 설정]
if os.name == 'nt':
    target_cache_dir = 'C:/paddle_cache'
    if not os.path.exists(target_cache_dir):
        try: os.makedirs(target_cache_dir)
        except: pass
    os.environ['USERPROFILE'] = target_cache_dir
    os.environ['HOME'] = target_cache_dir
    os.environ['PADDLE_HOME'] = target_cache_dir
    os.environ['PADDLEX_HOME'] = target_cache_dir

# OCR 모델 로드
ocr = PaddleOCR(use_angle_cls=True, lang='korean')

def extract_nutrition_info(image_file):
    # 1. 이미지 읽기
    file_bytes = np.frombuffer(image_file.read(), np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    if image is None: return {}

    # ---------------------------------------------------------
    # [전처리] 5중 필터 (인식 자체는 잘 되므로 유지)
    # ---------------------------------------------------------
    processed_images = []
    
    # 여백 추가
    image_padded = cv2.copyMakeBorder(image, 50, 50, 50, 50, cv2.BORDER_CONSTANT, value=(255, 255, 255))
    
    # 1. 원본
    gray = cv2.cvtColor(image_padded, cv2.COLOR_BGR2GRAY)
    gray_resized = cv2.resize(gray, None, fx=2.0, fy=2.0, interpolation=cv2.INTER_CUBIC)
    processed_images.append(gray_resized)
    
    # 2. 반전
    gray_inv = cv2.bitwise_not(gray_resized)
    processed_images.append(gray_inv)
    
    # 3. 이진화
    _, binary = cv2.threshold(gray_resized, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    processed_images.append(binary)
    processed_images.append(cv2.bitwise_not(binary)) # 반전 이진화

    # 4. 흰색 추출
    hsv = cv2.cvtColor(image_padded, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, np.array([0, 0, 150]), np.array([180, 50, 255]))
    processed_images.append(cv2.bitwise_not(mask))

    # ---------------------------------------------------------
    # [OCR 실행]
    # ---------------------------------------------------------
    all_text_list = []
    for img in processed_images:
        try:
            result = ocr.ocr(img, cls=False)
            if result and result[0]:
                for line in result[0]:
                    if line and len(line) >= 2 and line[1]:
                        if line[1][1] > 0.5:
                            all_text_list.append(line[1][0])
        except: continue
    
    full_text = " ".join(all_text_list)
    print(f"🔍 [OCR 통합 데이터] {full_text}")

    data = { 'calorie': 0, 'carbo': 0, 'protein': 0, 'fat': 0, 'hashtag': '#기타' }

    # ---------------------------------------------------------
    # [핵심] 제품 타입 판단 (새우탕 vs 포스틱)
    # ---------------------------------------------------------
    # "면", "누들", "새우탕", "라면" 중 하나라도 있으면 라면 모드 발동
    is_noodle_mode = any(k in full_text for k in ['새우탕', '누들', '면', '라면', '국수'])

    # ---------------------------------------------------------
    # [파싱 로직] 모드에 따른 이원화 처리
    # ---------------------------------------------------------
    def parse_value_split(text, keywords, nutrient_type):
        # 1. %가 붙은 숫자는 아예 지워버림 (가장 확실한 방법)
        # 예: "28%" -> " " (공백)
        text = re.sub(r'\d+(?:\.\d+)?\s*%', ' ', text)
        
        # 2. g를 9로 읽는 오인식 방지
        text = re.sub(r'(\d)\s*9\s', r'\1g ', text)
        
        target_text = ""
        for keyword in keywords:
            if keyword in text:
                target_text = text.split(keyword, 1)[1]
                break
        
        if not target_text: return 0

        # 3. 숫자 추출
        # 특수문자를 공백으로 바꿈 (점 . 은 살림)
        cleaned_text = re.sub(r'[^\d.]', ' ', target_text)
        tokens = cleaned_text.split()
        
        valid_numbers = []
        for token in tokens:
            try:
                if token.count('.') > 1: # 1.6.3 -> 1.6
                    token = token.split('.')[0] + '.' + token.split('.')[1]
                val = float(token)
                
                # 칼로리 2000 무조건 제외
                if nutrient_type == 'calorie' and val == 2000: continue
                
                valid_numbers.append(val)
            except: continue

        if not valid_numbers: return 0

        # -----------------------------------------------------
        # [모드별 결정 로직] 여기가 핵심입니다
        # -----------------------------------------------------
        val1 = valid_numbers[0]
        
        # [Case 1: 라면 모드 (새우탕)] -> 합치기 & 소수점 적극 보정
        if is_noodle_mode:
            # 탄수화물: 숫자가 끊겨있으면 합침 (2 9 -> 29)
            if nutrient_type == 'carbo':
                if val1 < 10 and len(valid_numbers) >= 2:
                    val2 = valid_numbers[1]
                    merged = float(f"{int(val1)}{int(val2)}")
                    if merged <= 150: val1 = merged
            
            # 지방/단백질: 10 넘으면 무조건 오인식으로 간주 (라면 특성상 16g 지방은 드묾 -> 1.6)
            if nutrient_type in ['fat', 'protein']:
                if val1 >= 10: val1 /= 10.0

        # [Case 2: 스낵 모드 (포스틱)] -> 첫 번째 숫자만 신뢰
        else:
            # 탄수화물/단백질/지방: 뒤에 숫자가 더 있어도 무시함 (이미 %는 위에서 지웠으므로)
            # 단백질/지방이 35 넘으면 소수점 누락으로 의심 (38 -> 3.8)
            if nutrient_type in ['fat', 'protein']:
                if val1 > 35: val1 /= 10.0
            
            # 탄수화물은 그냥 둠 (60은 60임)

        # 공통 오인식 방지 (너무 큰 값)
        if nutrient_type == 'carbo' and val1 > 300: val1 /= 10.0

        return val1

    # 1. 칼로리
    cal_match = re.search(r'(\d{2,4})\s*(?:kcal|Kcal)', full_text)
    if cal_match:
        try:
            val = float(cal_match.group(1))
            if val != 2000: data['calorie'] = val
        except: pass
        
    if data['calorie'] == 0:
        data['calorie'] = parse_value_split(full_text, ['칼로리', '열량'], 'calorie')

    # 2. 탄수화물
    data['carbo'] = parse_value_split(full_text, ['탄수화물', '탄수', '화물'], 'carbo')
    
    # 3. 단백질
    data['protein'] = parse_value_split(full_text, ['단백질', '단백'], 'protein')
    
    # 4. 지방
    clean_fat_text = full_text.replace('트랜스지방', '').replace('포화지방', '')
    data['fat'] = parse_value_split(clean_fat_text, ['지방'], 'fat')

    # 해시태그
    if is_noodle_mode:
        data['hashtag'] = '#컵라면 #라면'
    elif '과자' in full_text or '스낵' in full_text or '유탕' in full_text:
        data['hashtag'] = '#과자'
    elif '음료' in full_text or '커피' in full_text:
        data['hashtag'] = '#음료'
    elif '빵' in full_text:
        data['hashtag'] = '#빵'
    elif data['protein'] >= 10:
        data['hashtag'] = '#고단백'

    return data