import cv2
import mediapipe as mp
import serial
import time
import math

# Initialize serial communication with Arduino
arduino = serial.Serial(port='COM6', baudrate=9600, timeout=1)
time.sleep(2)  # Wait for the serial connection to initialize

# Initialize Mediapipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

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

# Function to estimate a servo angle (0–180) based on distance
def calculate_servo_angle(hand_landmarks, image_width, image_height):
    wrist = hand_landmarks.landmark[0]
    index_tip = hand_landmarks.landmark[8]

    x1, y1 = int(wrist.x * image_width), int(wrist.y * image_height)
    x2, y2 = int(index_tip.x * image_width), int(index_tip.y * image_height)

    distance = math.hypot(x2 - x1, y2 - y1)
    distance = max(20, min(distance, 200))  # Clamp between 20–200 pixels

    # Map distance to angle (0–180)
    angle = int((distance - 20) / (200 - 20) * 180)
    return angle

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

            # Detect finger states
            fingers_state = detect_fingers(hand_landmarks)

            # Calculate servo angle from wrist-index distance
            servo_angle = calculate_servo_angle(hand_landmarks, image_width, image_height)

            # Combine and send to Arduino
            data = fingers_state + [servo_angle]
            arduino.write(bytes(data))
            print(f"Data sent: {data}")

    cv2.imshow('Hand Tracking', image)
    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
arduino.close()