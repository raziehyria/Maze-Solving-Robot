# Maze-Solving-Robot
This project aims to utilize camera vision and artificial intelligence to maneuver through and solve a 2D maze. Our group hopes to create a fully functional maze-solving robot. Using the feed of an ESP32 camera mounted onto the robot, the program will read the track and junctions along the maze path and use artificial intelligence to solve the maze
## Objectives

1. Build a rover robot equipped with a camera.
2. Program Arduino to traverse lines and execute left or right turns when necessary.
3. Interpret the camera stream with OpenCV to learn about the environment.
4. Program rover to traverse the maze along the left-hand side.
5. Develop an algorithm to optimize the stored path and come up with a solution for the maze.
6. Program rover to execute the solved path onto the maze.

## Requirements
### User
1. Access to a computer with COM ports
2. Access to Arduino environment 
3. Access to PyCharm (or a similar IDE) and Python environment. 
4. Maze creation
5. Readjust robot for 2nd attempt
6. Note the displaying information of junctions and turns through python terminal
### Functional
7. Traverse any user-made maze
8. Relay information about turns and junctions
9. Save path
10. Solve maze on 2nd attempt

## How the maze algorithm works:
1. Given the processed image, assess if there is a left turn
..* Take a left turn if available, and add ‘L’ to the path taken
2. If there is no left path, asses if there is a straight path
..* Take the straight path, and add ‘S’ to the path taken if there is no ‘S’ at the front of the path 
3. If there is no straight or right path, asses if there is a right path
..* Take the right path and add ‘R’ to the path taken
4. After any action, check if there is at least a sequence of 3 actions
..* Try to reduce the last 3 actions into an optimal action
 LBR → B
....2. LBS → R
....2. LBL → S
....4. SBL → R
....5. SBS → B
....6. RBL → B

## Robot Logic
Every time the image process algorithm returns the available actions, the maze algorithm will determine which action the robot should take. Actions are added to the path and at the same time, a value will be serialized and sent to the Arduino using the COM port. There are 5 values that are sent over the COM port to trigger the robot's movement function. The message sent over the port is parsed to an int and a switch statement is used to choose which action to trigger.
* COM port values:
..* ‘0’: Triggers a stop action
..* ‘1’: Triggers a left action
..* ‘2’: Triggers a right action
..* ‘3’: Triggers a turnaround action
..* ‘4’: Triggers a straight action
