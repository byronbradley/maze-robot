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
    start_row, start_column = start

    if start_row < 0 or start_row >= len(maze):
        return []
    if start_column < 0 or start_column >= len(maze[start_row]):
        return []

    if not is_open(maze,start_row,start_column):
        return []
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

def get_direction(current, next_position):
    current_row, current_column = current
    next_row, next_column = next_position

    if next_column == current_column + 1 and next_row == current_row:
        return "right"
    if next_column == current_column - 1 and next_row == current_row:
        return "left"
    if next_row == current_row + 1 and next_column == current_column:
        return "down"
    if next_row == current_row - 1 and next_column == current_column:
        return "up"
    return None

def path_to_directions(path):
    directions = []
    for index in range(len(path)-1):
        current = path[index]
        next_position = path[index+1]
        directions.append(get_direction(current, next_position))
    return directions

def get_turn(heading, direction):
    if heading == direction:
        return "straight"
    headings = ["up", "right", "down", "left"]
    current_index = headings.index(heading)
    target_index = headings.index(direction)
    turn_steps = (target_index - current_index) % 4
    if turn_steps == 1:
        return "right"
    if turn_steps == 2:
        return "around"
    if turn_steps == 3:
        return "left"

def directions_to_commands(directions, heading):
    commands = []
    for direction in directions:
        turn = get_turn(heading, direction)
        commands.append((turn, "forward"))
        heading = direction
    return commands

def main():
    robot_row = 0
    robot_column = 0

    heading = "right"
    print("Starting heading:", heading)
    print("Turn needed:", get_turn(heading, "right"))

    print("Before moving:")
    display_maze(robot_maze, robot_row, robot_column, goal_row, goal_column)

    goal = (goal_row,goal_column)
    path = find_path(robot_maze, (0, 0), goal)

    if path:
        print("Path from start to goal:", path)

        for robot_row, robot_column in path:
            print("Robot at:", robot_row, robot_column)
            display_maze(robot_maze, robot_row, robot_column, goal_row, goal_column)
            print()
        print("Final position:", robot_row, robot_column)
        if (robot_row,robot_column) == goal:
            print("Goal reached!")
    else:
        print("No route to the goal.")

    directions = path_to_directions(path)
    print("Directions:",directions)

    commands = directions_to_commands(directions, heading)
    print("Commands:", commands)

    for turn, movement in commands:
        print("Turn:", turn)
        print("Move:", movement)

if __name__ == "__main__":
    main()