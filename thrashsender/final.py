import socket
import mss
import pickle
import zlib
import pyautogui
import cv2
import numpy as np

# Define the IP and port of the receiver
receiver_ip = '192.168.1.1'
port = 12345

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Maximum UDP packet size (slightly less to account for overhead)
MAX_PACKET_SIZE = 60000


cnt=0
# Set up screen capture
with mss.mss() as sct:
    monitor = sct.monitors[1]  # Capture the first monitor

    while True:
        # Capture the screen
        img = np.array(sct.grab(monitor))

        # Get the current mouse position
        cursor_x, cursor_y = pyautogui.position()

        # Draw the mouse cursor on the captured screen
        cursor_size = 15  # Adjust the size of the cursor
        cv2.drawMarker(img, (cursor_x, cursor_y), color=(0, 0, 255), markerType=cv2.MARKER_CROSS, markerSize=cursor_size, thickness=2)

        # Serialize and compress the image data
        data = pickle.dumps(img)
        compressed_data = zlib.compress(data, zlib.Z_BEST_COMPRESSION)

        # Split data into chunks if it's too large
        for i in range(0, len(compressed_data), MAX_PACKET_SIZE):
            chunk = compressed_data[i:i + MAX_PACKET_SIZE]
            sock.sendto(chunk, (receiver_ip, port))
        
        cnt+=1

        # Optional: Add a sleep to control the frame rate
        if cnt==2000000:
            time.sleep(0.033)  # ~30 FPS