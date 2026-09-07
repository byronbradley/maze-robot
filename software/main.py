robot_maze = [
    [0, 0, 1, 0, 0],
    [1, 0, 1, 0, 1],
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 1, 0],
]

def is_open(maze,row,column):
    return maze[row][column] == 0

def move_right(maze,row,column):
    width = len(maze[row])
    if column < width - 1:
        if is_open(maze,row,column+1):
            return column + 1
    return column

def move_left(maze,row,column):
    if column > 0:
        if is_open(maze,row,column-1):
            return column - 1
    return column

def move_down(maze,row,column):
    height = len(maze)
    if row < height - 1:
        if is_open(maze,row+1,column):
            return row + 1
    return row

def move_up(maze,row,column):
    if row > 0:
        if is_open(maze,row-1,column):
            return row - 1
    return row

def display_maze(maze, current_row, current_column):
    for row_number, row in enumerate(maze):
        for column_number, cell in enumerate(row):
            if row_number == current_row and column_number == current_column:
                print("R", end=" ")
            elif cell == 1:
                print("#", end=" ")
            else:
                print(".", end=" ")
        print()

def main():
    robot_row = 0
    robot_column = 0
    print("Before moving:")
    display_maze(robot_maze, robot_row, robot_column)

    robot_column = move_right(robot_maze, robot_row, robot_column)

    print("After moving right:")
    display_maze(robot_maze, robot_row, robot_column)

    robot_column = move_right(robot_maze, robot_row, robot_column)

    print("After trying to move into the wall:")
    display_maze(robot_maze, robot_row, robot_column)

    robot_row = move_down(robot_maze, robot_row, robot_column)

    print("After moving down:")
    display_maze(robot_maze, robot_row, robot_column)

if __name__ == "__main__":
    main()