# Advanced_Home_Automation
A gesture-recognition control system is implemented using a laptop webcam. Hand gestures are detected using OpenCV and MediaPipe to control appliances in real time, enabling intuitive and contactless smart-home automation without physical switches or remotes.

# Hand Gesture: 
A dedicated gesture control module uses a laptop camera and the Mediapipe framework to detect finger movements. Specific finger gestures toggle devices such as LEDs and a servo motor, providing an intuitive and touch-free interaction method. 

# Hardware Components: 

1. Input and Control Setup 
Visual Studio Application: Acts as the interface for inputting gestures (manually or via integrated sensors). 
Serial Communication: Used to transmit gesture commands from the Visual Studio application to the 
Arduino board. 
 
2. Arduino-Based Appliance Control 
Arduino Board: Serves as the central controller interpreting commands and managing output devices. 
Breadboard and Wires: Used for circuit connections and component interfacing. 
LEDs: Act as visual indicators toggled by respective finger gestures. 
Servo Motor: Rotates between 0° and 180° depending on thumb and pinky inputs. 
USB Connection: Facilitates both programming and serial communication with the PC. 
 
# Software Implementation 

1. Visual Studio Application Development 
Developed using Visual Studio, the application allows user input to simulate hand gestures. 
Inputs are mapped to specific serial commands that are transmitted to the Arduino via a COM port. 
The application provides an interactive and user-friendly interface to simulate gesture controls. 
 
2. Arduino Programming via Arduino ID 
The Arduino is programmed using C/C++ in the Arduino IDE. 
It continuously listens for serial data and executes the corresponding logic to toggle LEDs or rotate the 
servo motor.The use of rising-edge detection ensures that each gesture command is executed only once per input, 
preventing duplicate operations. 
