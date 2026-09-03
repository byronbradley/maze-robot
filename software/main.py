robot_row = 0
robot_column = 0
maze_width = 5
maze_height = 5
robot_maze = [
    [0, 0, 1, 0, 0],
    [1, 0, 1, 0, 1],
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 1, 0],
]

print("Starting cell:", robot_maze[0][0])
print("Cell two columns right:", robot_maze[0][2])
print("Robot row:",robot_row)
print("Robot column:",robot_column)
print("Maze width:",maze_width)
print("Maze height:",maze_height)

def is_open(maze,row,column):
    return maze[row][column] == 0

def move_right(maze,row,column):
    width = len(maze[row])
    if column < width - 1:
        if is_open(maze,row,column+1):
            return column + 1
    return column
robot_column = move_right(robot_maze, robot_row, robot_column)
print("Robot column after moving right:",robot_column)

def move_left(maze,row,column):
    if column > 0:
        if is_open(maze,row,column-1):
            return column - 1
    return column
robot_column = move_left(robot_maze, robot_row, robot_column)
print("Robot column after moving left:",robot_column)

def move_down(maze,row,column):
    height = len(maze)
    if row < height - 1:
        if is_open(maze,row+1,column):
            return row + 1
    return row
robot_row = move_down(robot_maze, robot_row, robot_column)
print("Robot row after moving down:",robot_row)

def move_up(maze,row,column):
    if row > 0:
        if is_open(maze,row-1,column):
            return row - 1
    return row
robot_row = move_up(robot_maze,robot_row, robot_column)
print("Robot row after moving up:",robot_row)

print("Open below:", move_down(robot_maze, 0, 1))
print("Wall below:", move_down(robot_maze, 0, 0))
print("Bottom edge:", move_down(robot_maze, 4, 0))

print("Top edge:", move_up(robot_maze, 0, 0))
print("Open above:", move_up(robot_maze, 1, 1))
print("Wall above:", move_up(robot_maze, 2, 2))

print("Open left:", move_left(robot_maze, 0, 1))
print("Wall left:", move_left(robot_maze, 0, 3))
print("Left edge:", move_left(robot_maze, 0, 0))

print("Open path:", move_right(robot_maze, 0, 0))
print("Wall ahead:", move_right(robot_maze, 0, 1))
print("Right edge:", move_right(robot_maze, 0, 4))

print("Starting cell open:", is_open(robot_maze, 0, 0))
print("Wall cell open:", is_open(robot_maze, 0, 2))