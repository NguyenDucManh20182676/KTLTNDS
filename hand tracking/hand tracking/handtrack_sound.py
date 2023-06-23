import json
import cv2
import mediapipe as mp
import redis
import pygame
import math

# Khởi tạo pygame
pygame.init()

# Tạo cửa sổ âm thanh
pygame.mixer.init()

# Tải âm thanh từ file
sound = pygame.mixer.Sound("D:/hand tracking/nhac.mp3")  # Thay đường dẫn đến file âm thanh của bạn

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

    prev_hand_landmarks = None
    hand_moved = False

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
            hand_landmarks = results.multi_hand_landmarks[0]
            current_hand_landmarks = hand_landmarks.landmark

            # Kiểm tra sự thay đổi tọa độ tay
            if prev_hand_landmarks:
                prev_positions = [(prev_hand_landmarks[i].x, prev_hand_landmarks[i].y, prev_hand_landmarks[i].z)
                                  for i in range(len(prev_hand_landmarks))]
                current_positions = [(current_hand_landmarks[i].x, current_hand_landmarks[i].y, current_hand_landmarks[i].z)
                                     for i in range(len(current_hand_landmarks))]
                distances = [math.dist(prev_positions[i], current_positions[i])
                             for i in range(len(prev_positions))]
                hand_moved = any(distance > 0 for distance in distances)

                # Nếu có sự thay đổi, phát nhạc
                if hand_moved and sound.get_num_channels() == 0:
                    sound.play()
                # Nếu không có sự thay đổi, tạm dừng nhạc
                elif not hand_moved and sound.get_num_channels() > 0:
                    sound.stop()

            prev_hand_landmarks = current_hand_landmarks

            mp_drawing.draw_landmarks(
                image,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())

        # Hiển thị hình ảnh và kiểm tra sự thoát
        cv2.imshow('MediaPipe Hands', image)
        if cv2.waitKey(5) & 0xFF == 27:
            break

# Kết thúc pygame
pygame.quit()

cap.release()
