import random


def generate_maze():
    maze = []

    for row in range(5):
        cells = []
        for column in range(5):
            if random.random() < 0.3:
                cells.append(1)
            else:
                cells.append(0)
        maze.append(cells)

    maze[0][0] = 0
    maze[4][4] = 0
    return maze