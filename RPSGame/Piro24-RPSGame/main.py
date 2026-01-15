import cv2
import mediapipe as mp
import time
from visualization import draw_manual, print_RSP_result

# MediaPipe 관련 설정
BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

def get_rps_value(landmarks):
    """
    형님의 visualization.py에 맞춰 0(Rock), 1(Paper), 2(Scissors) 반환
    """
    # y값 비교 (작을수록 위쪽)
    # 8, 12, 16, 20번 끝마디가 6, 10, 14, 18번 중간마디보다 위에 있는지 확인
    is_index_open = landmarks[8].y < landmarks[6].y
    is_middle_open = landmarks[12].y < landmarks[10].y
    is_ring_open = landmarks[16].y < landmarks[14].y
    is_pinky_open = landmarks[20].y < landmarks[18].y

    # 1. 보 (Paper): 모든 손가락이 펴짐
    if is_index_open and is_middle_open and is_ring_open and is_pinky_open:
        return 1
    
    # 2. 가위 (Scissors): 검지와 중지만 펴짐
    if is_index_open and is_middle_open and not is_ring_open and not is_pinky_open:
        return 2
    
    # 3. 바위 (Rock): 모든 손가락이 접힘 (엄지는 제외하고 판단)
    if not any([is_index_open, is_middle_open, is_ring_open, is_pinky_open]):
        return 0
        
    return None

def main():
    # 1. 모델 설정 (VIDEO 모드 사용)
    options = HandLandmarkerOptions(
        base_options=BaseOptions(model_asset_path='hand_landmarker.task'),
        running_mode=VisionRunningMode.VIDEO,
        num_hands=1
    )

    cap = cv2.VideoCapture(0)

    with HandLandmarker.create_from_options(options) as landmarker:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret: break

            frame = cv2.flip(frame, 1)
            # MediaPipe용 RGB 이미지 변환
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
            
            # 타임스탬프 계산
            timestamp_ms = int(time.time() * 1000)
            
            # 2. 랜드마크 검출
            result = landmarker.detect_for_video(mp_image, timestamp_ms)

            # 3. 결과 시각화 및 판별
            if result.hand_landmarks:
                # 점과 선 그리기 (형님의 visualization.py 활용)
                frame = draw_manual(frame, result)
                
                # 가위바위보 판별 (숫자 0, 1, 2)
                rps_val = get_rps_value(result.hand_landmarks[0])
                
                # 결과 텍스트 출력 (형님의 visualization.py 활용)
                frame = print_RSP_result(frame, rps_val)

            cv2.imshow('RPS Project', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()