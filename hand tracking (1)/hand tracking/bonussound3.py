import json
import redis
import pyautogui
import pygame

# Khởi tạo pygame
pygame.init()

# Tạo cửa sổ âm thanh
pygame.mixer.init()

# Tải âm thanh từ file
sound = pygame.mixer.Sound("D:/hand tracking/nhac2.mp3")  # Thay đường dẫn đến file âm thanh của bạn

# Thiết lập cấu hình âm thanh
volume = 1
sound.set_volume(volume)

# Kết nối Redis
r = redis.StrictRedis(host='localhost', port=6379, db=0)

# Lấy tọa độ chuột ban đầu
prev_x, prev_y = pyautogui.position()

# Biến để kiểm tra sự di chuyển chuột
mouse_moved = False

# Hàm để phát âm thanh
def play_sound():
    sound.play()

# Hàm để tạm dừng âm thanh
def pause_sound():
    sound.stop()

while True:
    # Lấy thông tin vị trí của con chuột
    mouse_x, mouse_y = pyautogui.position()

    # Kiểm tra sự di chuyển chuột
    if mouse_x != prev_x or mouse_y != prev_y:
        mouse_moved = True
    else:
        mouse_moved = False

    # Lưu tọa độ chuột hiện tại
    prev_x, prev_y = mouse_x, mouse_y

    # Gửi thông tin vị trí tới Redis
    position = {'x': mouse_x, 'y': mouse_y}
    r.set('mousePosition', json.dumps(position))

    # Kiểm tra sự di chuyển chuột và điều khiển âm thanh
    if mouse_moved:
        if sound.get_num_channels() == 0:
            play_sound()
    else:
        pause_sound()

    # Kiểm tra sự kiện pygame.MOUSEMOTION (di chuyển chuột)
    for event in pygame.event.get():
        if event.type == pygame.MOUSEMOTION:
            mouse_moved = True

    # Tiếp tục vòng lặp

    # Điều chỉnh âm lượng âm thanh
    volume = 1 if mouse_moved else 0
    sound.set_volume(volume)

    pygame.time.wait(100)  

# Kết thúc pygame
pygame.quit()