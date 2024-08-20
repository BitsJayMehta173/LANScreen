import socket
from PIL import Image
import io

# Client setup
server_ip = '192.168.1.1'  # Replace with your server's IP address
server_port = 12345
buffer_size = 4096

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_ip, server_port))

try:
    while True:
        # Receive image size
        image_size = int.from_bytes(client_socket.recv(4), byteorder='big')

        # Receive image data
        img_data = b''
        while len(img_data) < image_size:
            packet = client_socket.recv(buffer_size)
            if not packet:
                break
            img_data += packet

        # Display image
        img = Image.open(io.BytesIO(img_data))
        img.show()  # This will open the default image viewer
finally:
    client_socket.close()
