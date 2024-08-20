import cv2
import zmq
import numpy as np

def apply_delta_frame(base_frame, changed_coords, changed_values):
    for (y, x), value in zip(changed_coords, changed_values):
        base_frame[y, x] = value
    return base_frame

def main():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://192.168.1.2:5555")

    # Signal readiness to receive the initial frame
    socket.send_string("READY")
    encoded_frame = socket.recv()

    np_frame = np.frombuffer(encoded_frame, dtype=np.uint8)
    base_frame = cv2.imdecode(np_frame, cv2.IMREAD_COLOR)
    
    if base_frame is None or base_frame.size == 0:
        print("Error: Received empty or invalid initial frame.")
        return

    print(f"Base frame dimensions: {base_frame.shape}")

    # Send confirmation message to sender
    socket.send_string("RECEIVED")

    # Create a named window and set it to full screen
    cv2.namedWindow("Stream", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Stream", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    
    # Display the initial frame
    cv2.imshow("Stream", base_frame)

    while True:
        try:
            # Signal readiness for next frame data
            socket.send_string("READY_FOR_NEXT")
            next_message = socket.recv_string()  # Blocking receive to ensure correct sync

            if next_message == "SENDING_DELTA":
                changed_coords, changed_values = socket.recv_pyobj()
            else:
                print("Unexpected message received: ", next_message)
                break

            if base_frame is None or base_frame.size == 0:
                print("Error: Base frame is invalid.")
                continue
            
            # Apply the delta frame to reconstruct the current frame
            base_frame = apply_delta_frame(base_frame, changed_coords, changed_values)
            
            # Display the reconstructed frame
            cv2.imshow("Stream", base_frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        except Exception as e:
            print(f"An error occurred: {e}")
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
