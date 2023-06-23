import redis
import json
import time

# Kết nối tới Redis server
redis_client = redis.Redis()

# Chụp sự kiện di chuyển con trỏ và gửi thông tin vị trí tới Redis
def capture_cursor_position():
    while True:
        # Giả định bạn đã có mã thực tế để lấy vị trí con trỏ
        x, y = get_cursor_position()
        position = {'x': x, 'y': y}

        # Gửi thông tin vị trí tới Redis
        redis_client.set('cursorPosition', json.dumps(position))

        # Ngừng thực thi trong một khoảng thời gian nhất định (ví dụ: 0.1 giây)
        time.sleep(0.1)

# Hàm giả định để lấy vị trí con trỏ (thay thế bằng mã thực tế)
def get_cursor_position():
    # Giả định vị trí con trỏ x và y
    x = 100
    y = 200
    return x, y

# Thực thi chụp sự kiện di chuyển con trỏ
capture_cursor_position()
