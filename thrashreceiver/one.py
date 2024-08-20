import socket
from PIL import Image
from io import BytesIO
import numpy as np
import cv2
# Set up client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('192.168.1.2', 12345))  # Replace with sender’s IP

try:
    while True:
        # Receive image size
        size_data = client_socket.recv(4)
        if not size_data:
            break
        size = int.from_bytes(size_data, byteorder='big')

        # Receive image data
        data = b''
        while len(data) < size:
            packet = client_socket.recv(size - len(data))
            if not packet:
                break
            data += packet

        # Convert to image and display
        base_frame = Image.open(BytesIO(data))
        # image.show()  # This will open the image in the default viewer
        cv2.imshow("Stream", base_frame)
finally:
    client_socket.close()
