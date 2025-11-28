import cv2
import mediapipe as mp
import threading

class HandGestureTracker:
    def __init__(self):
        self.cap = None # opencv camera object
        self.running = False # flag telling loop when to stop
        self.thread = None # thread that runs the camera

        # Model load
        self.mp_hands = mp.solutions.hands
        self.hand = self.mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.5)
        self.mp_draw = mp.solutions.drawing_utils

        # store gesture
        self.gesture = None
    
    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self.camera_loop, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
    
    # public method to get gesture
    def get_gesture(self):
        return self.gesture
    
    def camera_loop(self):
        self.cap = cv2.VideoCapture(0)

        while self.running:
            ret,frame = self.cap.read() #ret = boolean for if fram was successfully read
            if not ret:
                continue

            frame_rgb = cv2.cvtColor(cv2.flip(frame,1), cv2.COLOR_BGR2RGB)
            results = self.hand.process(frame_rgb)

            gesture = None

            if results.multi_hand_landmarks:
                hand = results.multi_hand_landmarks[0]

                pointerfinger_id = 8
                pointerknuckle_id = 6
                #wrist_id = 0

                tipY = hand.landmark[pointerfinger_id].y
                tipX = hand.landmark[pointerfinger_id].x
                knuckleY = hand.landmark[pointerknuckle_id].y
                knuckleX = hand.landmark[pointerknuckle_id].x

                #pointing up
                if tipY < knuckleY:
                    gesture = "UP"
                if tipY > knuckleY:
                    gesture = "DOWN"
                if tipX < knuckleX:
                    gesture = "LEFT"
                if tipX > knuckleX:
                    gesture = "RIGHT"
                
                # Draw landmarks in webcam window
                self.mp_draw.draw_landmarks(frame, hand, self.mp_hands.HAND_CONNECTIONS)
            
            self.gesture = gesture

            cv2.imshow("Hand Tracking", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
                








    

