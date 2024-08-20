import socket
import pyautogui
from PIL import Image
import io

# Server setup
server_ip = '192.168.1.1'  # Replace with your server's IP address
server_port = 12345
buffer_size = 4096

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_ip, server_port))
server_socket.listen(1)

print(f"Server listening on {server_ip}:{server_port}")

conn, addr = server_socket.accept()
print(f"Connected by {addr}")

try:
    while True:
        # Capture the screen
        screenshot = pyautogui.screenshot()
        img_bytes = io.BytesIO()
        screenshot.save(img_bytes, format='PNG')
        img_bytes.seek(0)

        # Send image size
        image_size = len(img_bytes.getvalue())
        conn.sendall(image_size.to_bytes(4, byteorder='big'))

        # Send image data
        while True:
            img_data = img_bytes.read(buffer_size)
            if not img_data:
                break
            conn.sendall(img_data)
finally:
    conn.close()
    server_socket.close()