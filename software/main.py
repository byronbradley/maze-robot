robot_row = 0
robot_column = 0
maze_width = 5
maze_height = 5
print("Robot row:",robot_row)
print("Robot column:",robot_column)
print("Maze width:",maze_width)
print("Maze height:",maze_height)

def move_right(column,width):
    if column < width - 1:
        return column + 1
    return column
robot_column = move_right(robot_column,maze_width)
print("Robot column after moving right:",robot_column)

def move_left(column):
    if column > 0:
        return column - 1
    return column
robot_column = move_left(robot_column)
print("Robot column after moving left:",robot_column)

def move_down(row,height):
    if row < height - 1:
        return row + 1
    return row
robot_row = move_down(robot_row,maze_height)
print("Robot row after moving down:",robot_row)

def move_up(row):
    if row > 0:
        return row - 1
    return row
robot_row = move_up(robot_row)
print("Robot row after moving up:",robot_row)

print("Taller maze:", move_down(4, 7))
print("Bottom of taller maze:", move_down(6, 7))
print("One-row maze:", move_down(0, 1))
print("Top edge:", move_up(0))
print("Left edge:", move_left(0))
print("Right edge:", move_right(4, 5))