<<<<<<< HEAD
from paddleocr import PaddleOCR

=======
import numpy as np
from paddleocr import PaddleOCR
from PIL import Image, ImageDraw, ImageFont

# 모델 로드는 서버 시작 시 한 번만 되도록 함수 밖에서 선언
ocr_engine = PaddleOCR(lang='korean')

def extract_text_from_image(image_field_path):
    """
    이미지 경로를 받아 OCR을 수행하고 결과 이미지를 저장하는 서비스 함수
    """
    image = Image.open(image_field_path)
    image_np = np.array(image)
    
    result = ocr_engine.ocr(image_np, cls=True)
    
    draw = ImageDraw.Draw(image)
    
    # 윈도우 기본 폰트 설정 (없으면 기본 시스템 폰트)
    try:
        font = ImageFont.truetype("malgun.ttf", 24)
    except:
        font = ImageFont.load_default()

    if result[0]:
        for line in result[0]:
            box = line[0]
            text = line[1][0]
            
            top_left = tuple(map(int, box[0]))
            bottom_right = tuple(map(int, box[2]))
            
            # 박스 및 텍스트 그리기
            draw.rectangle([top_left, bottom_right], outline=(0, 255, 0), width=2)
            draw.text(top_left, text, font=font, fill=(255, 0, 0))

    # 저장 경로 예시: static 폴더 등
    output_path = "static/posts/image/ocr_result.jpg"
    image.save(output_path)
    
    return result, output_path
>>>>>>> 833371fd1ece0725c07e84d6928be4e919fcd986
