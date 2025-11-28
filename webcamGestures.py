import cv2
import mediapipe as mp
import time

class HandGestureTracker:
    def __init__(self):
        self.cap = None
        self.running = False

        # Model load
        self.mp_hands = mp.solutions.hands
        self.hand = self.mp_hands.Hands(
            max_num_hands=1, 
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.mp_draw = mp.solutions.drawing_utils

        # store gesture
        self.gesture = None
        self.last_process_time = 0
    
    def start(self):
        self.running = True

    def stop(self):
        self.running = False
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
    
    def get_gesture(self):
        return self.gesture
    
    def camera_loop(self, update_callback=None):
        self.cap = cv2.VideoCapture(0)
        
        if not self.cap.isOpened():
            print("ERROR: Could not open camera!")
            return

        print("Camera opened successfully!")

        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                continue

            # Flip the frame for mirror effect
            frame = cv2.flip(frame, 1)
            
            # Process with MediaPipe (with error handling)
            try:
                # Only process every other frame to avoid timestamp issues
                current_time = time.time()
                if current_time - self.last_process_time > 0.033:  # ~30 fps
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    results = self.hand.process(frame_rgb)
                    self.last_process_time = current_time

                    gesture = None

                    if results.multi_hand_landmarks:
                        hand = results.multi_hand_landmarks[0]

                        pointerfinger_id = 8
                        pointerknuckle_id = 6

                        tipY = hand.landmark[pointerfinger_id].y
                        tipX = hand.landmark[pointerfinger_id].x
                        knuckleY = hand.landmark[pointerknuckle_id].y
                        knuckleX = hand.landmark[pointerknuckle_id].x

                        dx = abs(tipX - knuckleX)
                        dy = abs(tipY - knuckleY)

                        if dy > dx:
                            gesture = "UP" if tipY < knuckleY else "DOWN"

                        if dx > dy:
                            gesture = "LEFT" if tipX < knuckleX else "RIGHT"
                        
                        # Draw landmarks
                        self.mp_draw.draw_landmarks(frame, hand, self.mp_hands.HAND_CONNECTIONS)
                    
                    self.gesture = gesture
            
            except Exception as e:
                print(f"MediaPipe error (ignoring): {e}")
                pass

            # Show camera window
            cv2.imshow("Hand Tracking", frame)
            
            # Call pygame update callback if provided
            if update_callback:
                if not update_callback():
                    break
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        self.stop()
            
        
                








    

