from maze_path import MazePath
from image_processor import get_image, has_reached_end, has_straight_path, has_right_path, has_left_path, process_image, read_image, test
import cv2
import serial
import time

# Adjust these for your own ESP-32 and COM-Port
URL = 'http://10.0.0.161/capture'
MCU = serial.Serial("COM6", 9600)



def solve_maze():
    maze_path = MazePath()
    imNum = 0
    # image_array = [
    #     'turnDetector/left.png', 
    #     'turnDetector/back3.png', 
    #     'turnDetector/left.png',
    #     'turnDetector/left.png',
    #     'turnDetector/straight.png',
    #     'turnDetector/back3.png',
    #     'turnDetector/left.png',
    #     'turnDetector/back3.png',
    #     'turnDetector/left.png',
    #     'turnDetector/left.png',
    #     'turnDetector/straight.png', 
    #     'turnDetector/back3.png', 
    #     'turnDetector/left.png', 
    #     'turnDetector/left.png', 
    #     'turnDetector/back3.png', 
    #     'turnDetector/straight.png' ,
    #     'turnDetector/end.png'
    #     ]
    time.sleep(2)
    while (True):
        image = get_image(URL)
        #image = get_image(image_array[imNum])
        imNum += 1
        trackState, final = process_image(image)
        #print(trackState)
        if not has_reached_end(trackState):
            # Move forward an inch
            if has_left_path(trackState): # Can bot go left
                # Rotate -90 degrees
                maze_path.push_move('L')
                MCU.write('1'.encode()) # Sends encoded 1 to make the bot go left
                print('L') 
            elif has_straight_path(trackState) and has_right_path(trackState):
                # Stay straight0
                print('S')
                maze_path.push_move('S')
                MCU.write('4'.encode()) # Sends encoded 4 to make the bot go straight
            elif has_straight_path(trackState):
                # Stay straight
                print('S2')
                MCU.write('4'.encode()) # Sends encoded 4 to make the bot go straight
            elif has_right_path(trackState):
                # Rotate 90 degrees
                maze_path.push_move('R')
                MCU.write('2'.encode()) # Sends encoded 2 to make the bot go right
                print('R')
            else:
                # Rotate 180 degrees
                print('B')
                maze_path.push_move('B')
                MCU.write('0'.encode()) # Sends encoded 0 to make the bot stop
            maze_path.reduce_path()
        else:
            # The end has been reached
            break
        # Sleep for 1 sec after a movement
        time.sleep(1)

        #cv2.imshow("result", final)

        # Closes the video feed if showing
        if cv2.waitKey(1) & 0xFF == ord('e'):
            break

    #TODO add program pause here reset robot
    
    #begins second pass where the maze is solved
    # turnNum = 0
    # while (True):
    #     #image = get_image(URL)
    #     trackState = process_image(image)

    #     if not has_reached_end(trackState):
    #         if trackState['J'] == 'S':
    #             #Stay straight
    #             pass
    #         else:
    #             turn = maze_path.path[turnNum]
    #             if turn == 'L':
    #                 #Rotate -90 degrees -- program must pause for turning
    #                 pass
    #             elif turn == 'R':
    #                 #Rotate 90 degrees
    #                 pass
    #             elif turn == 'B':
    #                 #rotate 180 degrees
    #                 pass
    #             turnNum += 1
    #     else:
    #         print('Maze Solved!')
    #         break


def solve_maze_demo():
    maze_path = MazePath()

    '''image_array = [
        'turnDetector/left.png', 
        'turnDetector/end.png', 
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
        ]'''

    image_array = [
        'turnDetector/rightReal.png', 
        'turnDetector/leftOrRightReal.png', 
        ]

    move = {
        'S': '4',
        'B': '0',
        'L': '1',
        'R': '2'
    }
    for image_url in image_array:
        image = read_image(image_url)
        dir = process_image(image)
        maze_path.push_move(dir)
        MCU.write(move[dir['J'][0]].encode())

        maze_path.reduce_path()


    print('Final Path: ', maze_path.path, 'Total Moves:', maze_path.length)



def main():
    '''
    m = MazePath()
    m.path = ['x', 's', 'r', 'f', '0']
    print(m)
    x,y,t = m.get_prev_moves()
    print(x +y + t)
    m.path = m.path[:-3] + ['w']
    print(m)
    '''
    solve_maze()


if __name__ == '__main__':
    main()
