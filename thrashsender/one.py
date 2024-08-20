import socket
from PIL import ImageGrab
import io
from PIL import ImageGrab


# Set up server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('192.168.1.2', 12345))  # Bind to all interfaces on port 12345
server_socket.listen(1)
print("Waiting for a connection...")

connection, address = server_socket.accept()
print(f"Connected to {address}")
# # Capture the screen
# screen = ImageGrab.grab()
# screen.save("screen.png")

try:
    while True:
        # Capture screen
        screen = ImageGrab.grab()
        buffer = io.BytesIO()
        screen.save(buffer, format="PNG")
        data = buffer.getvalue()

        # Send image size first
        size = len(data)
        connection.sendall(size.to_bytes(4, byteorder='big'))

        # Send image data
        connection.sendall(data)
finally:
    connection.close()
    server_socket.close()