#include <Servo.h>

// Pin definitions
const int ledPins[] = {2, 3, 4};  // LED1, LED2, LED3
const int servoPin = 9;

Servo myServo;

void setup() {
  // Initialize LED pins
  for (int i = 0; i < 3; i++) {
    pinMode(ledPins[i], OUTPUT);
  }

  // Initialize servo
  myServo.attach(servoPin);

  // Initialize serial communication
  Serial.begin(9600);
}

void loop() {
  // Wait until 4 bytes are available
  if (Serial.available() >= 4) {
    byte led1 = Serial.read();  // Index finger
    byte led2 = Serial.read();  // Middle finger
    byte led3 = Serial.read();  // Ring finger
    byte servoAngle = Serial.read();  // Thumb or pinky

    // Set LEDs
    digitalWrite(ledPins[0], led1);
    digitalWrite(ledPins[1], led2);
    digitalWrite(ledPins[2], led3);

    // Set servo angle
    myServo.write(servoAngle);

    // Debug output (optional)
    Serial.print("LEDs: ");
    Serial.print(led1);
    Serial.print(", ");
    Serial.print(led2);
    Serial.print(", ");
    Serial.print(led3);
    Serial.print(" | Servo: ");
    Serial.println(servoAngle);
  }
}
