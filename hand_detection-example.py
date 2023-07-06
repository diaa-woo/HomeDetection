import cv2
import mediapipe as mp
import time

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

'''
# 이미지 파일의 경우일 때 사용
IMAGE_FILES = []
with mp_hands.Hands(
    static_image_mode=True,
    max_num_hands=2,
    min_detection_confidence=0.5
    ) as hands:

    for idx, file in enumerate(IMAGE_FILES):
        # 이미지를 불러오고, 이미지 좌우반전
        image = cv2.flip(cv2.imread(file), 1)
        # 작업 전에 BGR 이미지를 RGB로 변환.
        results = hands.process(cv2.cvtColor(image, cv2.COLOR_BAYER_BG2BGR))
        
        # 손으로 프린트하고 이미지에 손 랜드마크를 그림
        print('Handedness: ', results.multi_handedness)
        if not results.multi_hand_landmarks:
            continue
        image_height, image_width, _ = image.shape
        annotated_image = image.copy()
        for hand_landmarks in results.multi_hand_landmarks:
            print('hand_landmarks:', hand_landmarks)
            print(
                f'Index finger tip coordinates: (',
                f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * image_width}, ',
                f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_height}, ',
            )
            mp_drawing.draw_landmarks(
                annotated_image,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style()
            )
        cv2.imwrite('/tmp/annotated_image' + str(idx) + '.png', cv2.flip(annotated_image, 1))
'''
 
current_time = time.time()
previous_time = time.time()
cur_coordinate = [0,0]
pre_coordinate = [0,0]

# 웹캠, 영상 파일의 경우
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 200)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 200)

font=cv2.FONT_HERSHEY_SIMPLEX
text = ""

with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
    max_num_hands=1) as hands:
    
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("카메라를 찾을 수 없습니다.")
        
            # 동영상을 불러올 경우는 'continue' 대신 'break'를 사용함
            continue
    
        # 필요에 따라 성능 향상을 위해 이미지 작성을 불가능함으로 하는 설정 파일
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image)
        
        # 이미지에 손 주석 그림
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:
            if(current_time - previous_time >= 0.5) :
                previous_time = time.time()
                cur_coordinate = [hand_landmarks.landmark[8].x, hand_landmarks.landmark[8].y]
                
                if cur_coordinate[0] > pre_coordinate[0]:
                    text = "LEFT"
                else:
                    text = "RIGHT"
                pre_coordinate = cur_coordinate
            
            else:
                current_time = time.time()

            # Landmarks Drawing
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style()
                )
        else :
            previous_time = time.time()

        # 보기 편하게 이미지 좌우반전
        image = cv2.flip(image, 1)
        cv2.putText(image, text, (50, 100), font, 1, (255,0,0),2)
        cv2.imshow('MediaPipe Hands', image)
        if cv2.waitKey(5) & 0xFF == 27:
            break
cap.release()
