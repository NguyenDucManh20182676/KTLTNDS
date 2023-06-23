import json
import redis
import pyautogui
import keyboard

r = redis.StrictRedis(host='localhost', port=6379, db=0)

def on_key_event(event):
    if event.name == 'esc':
        keyboard.unhook_all()  # Hủy bỏ lắng nghe sự kiện phím
        return False  # Thoát khỏi vòng lặp
    
while True:
    # Lấy thông tin vị trí của con chuột
    mouse_x, mouse_y = pyautogui.position()

    # Gửi thông tin vị trí tới Redis
    position = {'x': mouse_x, 'y': mouse_y}
    r.set('mousePosition', json.dumps(position))

    # Tiếp tục vòng lặp
    