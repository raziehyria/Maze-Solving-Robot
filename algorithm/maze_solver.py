from maze_path import MazePath
from image_processor import get_image, has_reached_end, has_straight_path, has_right_path, has_left_path

URL = 'http://x.x.x.x/caputre'

def solve_maze():
    maze_path = MazePath()

    while (True):
        image = get_image(URL)

        if not has_reached_end(image):
            # Move forward an inch
            if has_left_path(image): # Can bot go left
                # Rotate -90 degrees
                maze_path.push_move('R')
                pass
            elif has_straight_path(image) and has_right_path():
                # Stay straight
                maze_path.push_move('S')
                pass
            elif has_straight_path(image):
                # Stay straight
                pass
            elif has_right_path(image):
                # Rotate 90 degrees
                maze_path.push_move('L')
                pass
            else:
                # Rotate 180 degrees
                maze_path.push_move('B')
            maze_path.reduce_path()
        else:
            # The end has been reached
            break



def main():
    m = MazePath()
    m.path = ['x', 's', 'r', 'f', '0']
    print(m)
    x,y,t = m.get_prev_moves()
    print(x +y + t)
    m.path = m.path[:-3] + ['w']
    print(m)


if __name__ == '__main__':
    main()
