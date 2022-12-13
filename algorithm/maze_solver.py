from maze_path import MazePath
from image_processor import get_image, has_reached_end, has_straight_path, has_right_path, has_left_path, process_image, read_image
import cv2
import serial
import time

# Adjust these for your own ESP-32 and COM-Port
URL = 'http://10.0.0.161/capture'
#MCU = serial.Serial("COM6", 9600)
MAZE_PATH = MazePath()


def solve_maze():
    time.sleep(2)
    while (True):
        image = get_image(URL)
        trackState, final = process_image(image)
        if not has_reached_end(trackState):
            # Move forward an inch
            if has_left_path(trackState): # Can bot go left
                # Rotate -90 degrees
                MAZE_PATH.push_move('L')
                MCU.write('1'.encode()) # Sends encoded 1 to make the bot go left
                print('Turn Left') 
            elif has_straight_path(trackState) and has_right_path(trackState):
                # Stay straight0
                print('Stay Straight')
                MAZE_PATH.push_move('S')
                MCU.write('4'.encode()) # Sends encoded 4 to make the bot go straight
            elif has_straight_path(trackState):
                # Stay straight
                print('Stay Straight')
                MCU.write('4'.encode()) # Sends encoded 4 to make the bot go straight
            elif has_right_path(trackState):
                # Rotate 90 degrees
                MAZE_PATH.push_move('R')
                MCU.write('2'.encode()) # Sends encoded 2 to make the bot go right
                print('Turn Right')
            else:
                # Rotate 180 degrees
                print('Turn Back')
                MAZE_PATH.push_move('B')
                MCU.write('3'.encode()) # Sends encoded 0 to make the bot stop
            MAZE_PATH.reduce_path()
        else:
            # The end has been reached
            break
        # Sleep for a half sec after a movement
        time.sleep(.5)

        cv2.imshow("result", final)

        # Closes the video feed if showing
        if cv2.waitKey(1) & 0xFF == ord('e'):
            break

def do_maze(maze_path):
    time.sleep(2)
    while (True):
        image = get_image(URL)
        trackState, final = process_image(image)
        if not has_reached_end(trackState):
            # Move forward an inch
            if has_left_path(trackState) and maze_path.path[0] == 'L': # Can bot go left
                # Rotate -90 degrees
                MCU.write('1'.encode()) # Sends encoded 1 to make the bot go left
                maze_path.path.pop()
                print("Turn Left")
            elif has_straight_path(trackState) and maze_path[0] == 'S': 
                # Stay straight
                MCU.write('4'.encode()) # Sends encoded 4 to make the bot go straight
                maze_path.path.pop()
                print("Stay Straight")
            elif has_right_path(trackState) and maze_path.path[0] == 'R':
                # Rotate 90 degrees
                MCU.write('2'.encode()) # Sends encoded 2 to make the bot go right
                maze_path.path.pop()
                print("Turn Right")
            else:
                # Rotate 180 degrees
                MCU.write('4'.encode()) # Sends encoded 0 to make the bot stop
                print("Go Back")
        else:
            # The end has been reached
            break
        # Sleep for a half sec after a movement
        time.sleep()

def solve_maze_demo():
    maze_path = MazePath()

    image_array = [
        'turnDetector/left.png', 
        'turnDetector/back.png',                                                                                     
        'turnDetector/left.png',
        'turnDetector/left.png',
        'turnDetector/straight.png',
        'turnDetector/back.png',
        'turnDetector/left.png',
        'turnDetector/back.png',
        'turnDetector/left.png',
        'turnDetector/left.png',
        'turnDetector/straight.png', 
        'turnDetector/back.png', 
        'turnDetector/left.png', 
        'turnDetector/left.png', 
        'turnDetector/back.png', 
        'turnDetector/straight.png' 
        ]


    move = {
        'S': '4',
        'B': '0',
        'L': '1',
        'R': '2'
    }
    for image_url in image_array:
        image = read_image(image_url)
        dir, final = process_image(image)
        print(dir['J'][0])
        maze_path.push_move(dir['J'][0])
        maze_path.reduce_path()
        cv2.imshow('Image', final)
        cv2.waitKey(0)


    print('Final Path: ', maze_path.path, 'Total Moves:', maze_path.length)

def maze_demo():
    time.sleep(2)
    while (True):
        time.sleep(5)
        image = get_image(URL)
        trackState, final = process_image(image)
        if not has_reached_end(trackState):
            # Move forward an inch
            if has_left_path(trackState): # Can bot go left
                # Rotate -90 degrees
                MAZE_PATH.push_move('L')
                print('Go Left :' + str(MAZE_PATH.path)) 
            elif has_straight_path(trackState) and has_right_path(trackState):
                # Stay straight
                MAZE_PATH.push_move('S')
                print('Go Straight : ' + str(MAZE_PATH.path))
            elif has_straight_path(trackState):
                # Stay straight
                print('Go Straight : ' + str(MAZE_PATH.path))
            elif has_right_path(trackState):
                # Rotate 90 degrees
                MAZE_PATH.push_move('R')
                print('Go Right : ' + str(MAZE_PATH.path))
            else:
                # Rotate 180 degrees
                MAZE_PATH.push_move('B')
                print('Go Back : ' + str(MAZE_PATH.path))
            MAZE_PATH.reduce_path()
        else:
            # The end has been reached
            return MAZE_PATH.path
        # Sleep for a half sec after a movement

        cv2.imshow("result", final)

        # Closes the video feed if showing
        if cv2.waitKey(1) & 0xFF == ord('e'):
            break

def solve_demo(maze_path):
    time.sleep(2)
    while (True):
        time.sleep(5)
        image = get_image(URL)
        trackState, final = process_image(image)
        if not has_reached_end(trackState):
            # Move forward an inch
            if has_left_path(trackState) and maze_path.path[0] == 'L': # Can bot go left
                # Rotate -90 degrees
                print('Go Left', str(maze_path.path[0]))
                maze_path.path.pop(0)
            elif has_straight_path(trackState) and (has_left_path(trackState) or has_right_path(trackState)) and maze_path.path[0] == 'S': 
                # Stay straight
                print('Go Straight', str(maze_path.path[0]))
                maze_path.path.pop(0)
            elif has_right_path(trackState) and maze_path.path[0] == 'R':
                # Rotate 90 degrees
                print('Go Right', str(maze_path.path[0]))
                maze_path.path.pop(0)
            else:
                print('Stay Straight', str(maze_path.path[0]))
        else:
            # The end has been reached
            print("Maze Finished!")
            return

def main():
    #solve_maze()
    #time.sleep(15)
    #do_maze(MAZE_PATH)
    ('Path :' + str(['S', 'S', 'R', 'R']))
    MAZE_PATH.path = ['S', 'S', 'R', 'R']
    solve_demo(MAZE_PATH)
    
if __name__ == '__main__':
    main()
