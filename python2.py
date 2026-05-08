import cv2
import mediapipe as mp
import serial
import time

# Initialize serial communication with Arduino
arduino = serial.Serial(port='COM5', baudrate=9600, timeout=1)
time.sleep(2)

# Initialize Mediapipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

# Finger toggle states: [LED1, LED2, LED3, Servo]
toggle_states = [0, 0, 0, 0]  # Index, Middle, Ring, Servo (180 or 0)
prev_finger_states = [0, 0, 0, 0, 0]  # Thumb, Index, Middle, Ring, Pinky

# Function to detect individual fingers (1 for up, 0 for down)
def detect_fingers(hand_landmarks):
    finger_tips = [8, 12, 16, 20]  # Index, Middle, Ring, Pinky
    thumb_tip = 4
    finger_states = [0, 0, 0, 0, 0]  # Thumb, Index, Middle, Ring, Pinky

    # Thumb: compare x-coordinates
    if hand_landmarks.landmark[thumb_tip].x < hand_landmarks.landmark[thumb_tip - 1].x:
        finger_states[0] = 1

    # Other fingers: compare y-coordinates
    for idx, tip in enumerate(finger_tips):
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
            finger_states[idx + 1] = 1

    return finger_states

# Start capturing video
cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, image = cap.read()
    if not success:
        break

    image = cv2.flip(image, 1)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)

    image_height, image_width, _ = image.shape

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            current_fingers = detect_fingers(hand_landmarks)

            # Toggle logic: only trigger on rising edge (0 -> 1)
            for i, name in zip(range(1, 4), ['Index', 'Middle', 'Ring']):
                if current_fingers[i] == 1 and prev_finger_states[i] == 0:
                    toggle_states[i - 1] ^= 1  # Toggle LED state
                    print(f"{name} toggled LED {i}: {toggle_states[i - 1]}")

            # Thumb - servo to 180°
            if current_fingers[0] == 1 and prev_finger_states[0] == 0:
                toggle_states[3] = 180
                print("Thumb: Servo -> 180°")

            # Pinky - servo to 0°
            if current_fingers[4] == 1 and prev_finger_states[4] == 0:
                toggle_states[3] = 0
                print("Pinky: Servo -> 0°")

            # Send data: [LED1, LED2, LED3, ServoAngle]
            data_to_send = toggle_states
            arduino.write(bytearray(data_to_send))
            print(f"Sent to Arduino: {data_to_send}")

            # Update previous finger states
            prev_finger_states = current_fingers

    cv2.imshow('Hand Tracking', image)
    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
arduino.close()
