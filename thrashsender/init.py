import cv2
import zmq
import numpy as np
import pyautogui

def main():
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://192.168.1.1:5555")
   
    while True:
        # Capture the full screen
        screenshot = pyautogui.screenshot()
        frame = np.array(screenshot)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
       
        # Get the current mouse position
        mouse_x, mouse_y = pyautogui.position()
       
        # Draw the mouse cursor on the frame (using a red circle)
        cursor_radius = 10
        cursor_color = (0, 0, 255)  # Red color in BGR
        cv2.circle(frame, (mouse_x, mouse_y), cursor_radius, cursor_color, -1)
       
        # Compress the frame to reduce size
        _, encoded_frame = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 50])
       
        # Send the compressed frame
        socket.send(encoded_frame)

if __name__ == "__main__":
    main()
