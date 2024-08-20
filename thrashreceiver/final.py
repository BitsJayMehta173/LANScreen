import socket
import pickle
import zlib
import cv2
import numpy as np
import pyautogui

# Define the IP and port to listen on
receiver_ip = '192.168.1.1'
port = 12345

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((receiver_ip, port))

# Buffer to hold the incoming chunks
buffer = b""

# Get the receiver's screen size
screen_width, screen_height = pyautogui.size()

# Create a named window for OpenCV and set it to full screen
cv2.namedWindow('Screen', cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty('Screen', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

while True:
    # Receive a chunk of data from the sender
    chunk, _ = sock.recvfrom(65536)

    # Add the chunk to the buffer
    buffer += chunk

    # Attempt to decompress and deserialize the buffer
    try:
        data = zlib.decompress(buffer)
        img = pickle.loads(data)
        buffer = b""  # Clear the buffer after successful decompression

        # Convert the image to a format suitable for OpenCV
        img_np = np.array(img)

        # Resize the image to fit the screen size
        img_resized = cv2.resize(img_np, (screen_width, screen_height), interpolation=cv2.INTER_LINEAR)

        # Display the resized image in full screen
        cv2.imshow('Screen', img_resized)

        # Exit on pressing 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    except zlib.error:
        # If decompression fails, continue to collect more data
        continue

# Clean up
cv2.destroyAllWindows()
sock.close()
