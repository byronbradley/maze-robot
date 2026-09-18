robot_maze = [
    [0, 0, 1, 0, 0],
    [1, 0, 1, 0, 1],
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 1, 0],
]
goal_row = 4
goal_column = 4

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

def display_maze(maze, current_row, current_column, target_row, target_column):
    for row_number, row in enumerate(maze):
        for column_number, cell in enumerate(row):
            if row_number == current_row and column_number == current_column:
                print("R", end=" ")
            elif cell == 1:
                print("#", end=" ")
            elif row_number == target_row and column_number == target_column:
                print("G", end=" ")
            else:
                print(".", end=" ")
        print()

def get_neighbors(maze, row, column):
    neighbors = []
    next_column = move_right(maze,row,column)
    if next_column != column:
        neighbors.append((row,next_column))
    next_column = move_left(maze,row,column)
    if next_column != column:
        neighbors.append((row,next_column))
    next_row = move_down(maze,row,column)
    if next_row != row:
        neighbors.append((next_row,column))
    next_row = move_up(maze,row,column)
    if next_row != row:
        neighbors.append((next_row,column))
    return neighbors

def find_path(maze, start, goal):
    queue = [start]
    visited = {start}
    came_from = {}

    while queue:
        current = queue.pop(0)
        if current == goal:
            break

        row, column = current
        for neighbor in get_neighbors(maze, row, column):
            if neighbor not in visited:
                visited.add(neighbor)
                came_from[neighbor] = current
                queue.append(neighbor)

    if goal not in visited:
        return []

    path = [goal]
    current = goal

    while current != start:
        current = came_from[current]
        path.append(current)

    path.reverse()
    return path

def main():
    robot_row = 0
    robot_column = 0

    print("Before moving:")
    display_maze(robot_maze, robot_row, robot_column, goal_row, goal_column)

    robot_column = move_right(robot_maze, robot_row, robot_column)

    print("After moving right:")
    display_maze(robot_maze, robot_row, robot_column, goal_row, goal_column)

    robot_column = move_right(robot_maze, robot_row, robot_column)

    print("After trying to move into the wall:")
    display_maze(robot_maze, robot_row, robot_column, goal_row, goal_column)

    robot_row = move_down(robot_maze, robot_row, robot_column)

    print("After moving down:")
    display_maze(robot_maze, robot_row, robot_column, goal_row, goal_column)

    position = (robot_row, robot_column)
    goal = (goal_row, goal_column)
    print("Current position:",position)
    print("Goal position:",goal)

    if position == goal:
        print("Goal reached!")
    else:
        print("Not at the goal yet.")

    print("Neighbors of start:", get_neighbors(robot_maze, 0, 0))
    print("Neighbors of middle:", get_neighbors(robot_maze, 2, 2))
    print("Neighbors of corridor:", get_neighbors(robot_maze, 1, 1))

    path = find_path(robot_maze, (0, 0), goal)

    if path:
        print("Path from start to goal:", path)

        for row, column in path:
            print("Robot at:", row, column)
            display_maze(robot_maze, row, column, goal_row, goal_column)
            print()
    else:
        print("No route to the goal.")

if __name__ == "__main__":
    main()