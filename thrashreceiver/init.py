import cv2
import zmq
import numpy as np

def main():
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://192.168.1.2:5555")
    socket.setsockopt_string(zmq.SUBSCRIBE, '')

    # Fullscreen window setup
    cv2.namedWindow("Stream", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Stream", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    try:
        while True:
            encoded_frame = socket.recv()
            np_frame = np.frombuffer(encoded_frame, dtype=np.uint8)
            frame = cv2.imdecode(np_frame, cv2.IMREAD_COLOR)
            
            if frame is not None:
                cv2.imshow("Stream", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                print("Failed to decode the frame.")
    except KeyboardInterrupt:
        print("Streaming stopped.")
    finally:
        cv2.destroyAllWindows()
        socket.close()
        context.term()

if __name__ == "__main__":
    main()