from maze_path import MazePath
from image_processor import get_image, has_reached_end, has_straight_path, has_right_path, has_left_path, process_image, read_image, test

URL = 'http://x.x.x.x/caputre'

def solve_maze():
    maze_path = MazePath()
    imNum = 0
    image_array = [
        'turnDetector/left.png', 
        'turnDetector/back3.png', 
        'turnDetector/left.png',
        'turnDetector/left.png',
        'turnDetector/straight.png',
        'turnDetector/back3.png',
        'turnDetector/left.png',
        'turnDetector/back3.png',
        'turnDetector/left.png',
        'turnDetector/left.png',
        'turnDetector/straight.png', 
        'turnDetector/back3.png', 
        'turnDetector/left.png', 
        'turnDetector/left.png', 
        'turnDetector/back3.png', 
        'turnDetector/straight.png' ,
        'turnDetector/end.png'
        ]
    while (True):
        #image = get_image(URL)
        image = read_image(image_array[imNum])
        imNum += 1
        trackState = process_image(image)
        print(trackState)
        if not has_reached_end(trackState):
            # Move forward an inch
            if has_left_path(trackState): # Can bot go left
                # Rotate -90 degrees
                maze_path.push_move('L')
                pass
            elif has_straight_path(trackState) and has_right_path(trackState):
                # Stay straight
                maze_path.push_move('S')
                pass
            elif has_straight_path(trackState):
                # Stay straight
                pass
            elif has_right_path(trackState):
                # Rotate 90 degrees
                maze_path.push_move('R')
                pass
            else:
                # Rotate 180 degrees
                maze_path.push_move('B')
            maze_path.reduce_path()
        else:
            # The end has been reached
            break

    #TODO add program pause here reset robot
    
    #begins second pass where the maze is solved
    turnNum = 0
    while (True):
        #image = get_image(URL)
        trackState = process_image(image)

        if not has_reached_end(trackState):
            if trackState['J'] == 'S':
                #Stay straight
                pass
            else:
                turn = maze_path.path[turnNum]
                if turn == 'L':
                    #Rotate -90 degrees -- program must pause for turning
                    pass
                elif turn == 'R':
                    #Rotate 90 degrees
                    pass
                elif turn == 'B':
                    #rotate 180 degrees
                    pass
                turnNum += 1
        else:
            print('Maze Solved!')
            break


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

    for image_url in image_array:
        image = read_image(image_url)
        maze_path.push_move(process_image(image))
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
