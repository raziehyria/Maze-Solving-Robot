from maze_path import MazePath
from image_processor import get_image, has_reached_end, has_straight_path, has_right_path, has_left_path, process_image, read_image, test

URL = 'http://x.x.x.x/caputre'

def solve_maze():
    maze_path = MazePath()

    while (True):
        #image = get_image(URL)
        image = read_image('turnDetector/left.png')
        process_image(image)

        if not has_reached_end():
            # Move forward an inch
            if has_left_path(): # Can bot go left
                # Rotate -90 degrees
                maze_path.push_move('L')
                pass
            elif has_straight_path() and has_right_path():
                # Stay straight
                maze_path.push_move('S')
                pass
            elif has_straight_path():
                # Stay straight
                pass
            elif has_right_path():
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
    solve_maze_demo()


if __name__ == '__main__':
    main()
