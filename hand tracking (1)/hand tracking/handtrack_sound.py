import json
import cv2
import mediapipe as mp
import redis
import pygame

# Khởi tạo pygame
pygame.init()

# Tạo cửa sổ âm thanh
pygame.mixer.init()

# Tải âm thanh từ file
sound = pygame.mixer.Sound("D:/hand tracking/nhac2.mp3")  # Thay đường dẫn đến file âm thanh của bạn

# Thiết lập cấu hình âm thanh
volume = 0.5
sound.set_volume(volume)

# Kết nối Redis
r = redis.StrictRedis(host='localhost', port=6379, db=0)

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)
with mp_hands.Hands(
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:
            X = results.multi_hand_landmarks[0].landmark[4]
            Y = results.multi_hand_landmarks[0].landmark[8]

            r.set('media_pipe', json.dumps([[X.x, X.y, X.z], [Y.x, Y.y, Y.z]]))

            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())
        
        # Kiểm tra tọa độ tay và điều khiển âm thanh
        if results.multi_hand_landmarks:
            # Lấy tọa độ tay
            hand_landmarks = results.multi_hand_landmarks[0]
            x_coords = [landmark.x for landmark in hand_landmarks.landmark]
            y_coords = [landmark.y for landmark in hand_landmarks.landmark]
            z_coords = [landmark.z for landmark in hand_landmarks.landmark]

            # Kiểm tra sự thay đổi tọa độ
            if (
                max(x_coords) - min(x_coords) > 0.05 or
                max(y_coords) - min(y_coords) > 0.05 or
                max(z_coords) - min(z_coords) > 0.05
            ):
                if sound.get_num_channels() == 0:
                    sound.play()
            else:
                sound.stop()

        # Hiển thị hình ảnh
        cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
        
        if cv2.waitKey(5) & 0xFF == 27:
            break
            
cap.release()

# Kết thúc pygame
pygame.quit()
