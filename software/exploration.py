from main import (robot_maze, get_neighbors, find_path, path_to_directions, directions_to_commands,
                  follow_commands, get_direction)

def sense_neighbors(maze, row, column):
    neighbors = [
        (row, column + 1),
        (row, column - 1),
        (row + 1, column),
        (row - 1, column)]
    readings = {}

    for next_row, next_column in neighbors:
        if 0 <= next_row < len(maze):
            if 0 <= next_column < len(maze[next_row]):
                readings[(next_row, next_column)] = maze[next_row][next_column]
    return readings

def update_known_maze(maze, known_maze, row, column):
    readings = sense_neighbors(maze, row, column)

    for (next_row, next_column), cell in readings.items():
        known_maze[next_row][next_column] = cell

def main():
    known_maze = [
        [None for column in row]
        for row in robot_maze]

    robot_row = 0
    robot_column = 0
    visited = {(robot_row, robot_column)}
    known_maze[robot_row][robot_column] = 0

    update_known_maze(robot_maze, known_maze, robot_row, robot_column)

    print("At the start:")
    for row in known_maze:
        print(row)

    trail = [(robot_row, robot_column)]
    heading = "down"

    while True:
        neighbors = get_neighbors(known_maze, robot_row, robot_column)
        next_position = None

        for neighbor in neighbors:
            if neighbor not in visited:
                next_position = neighbor
                break

        if next_position is not None:
            trail.append(next_position)
            visited.add(next_position)
        elif len(trail) > 1:
            trail.pop()
            next_position = trail[-1]
            print("Backtracking.")
        else:
            print("Finished exploring from here.")
            break

        heading = get_direction((robot_row, robot_column), next_position)
        robot_row, robot_column = next_position
        update_known_maze(robot_maze, known_maze, robot_row, robot_column)
        print("Robot at:", robot_row, robot_column)

    print("Discovered maze:")
    for row in known_maze:
        print(row)

    position = (robot_row, robot_column)
    path = find_path(known_maze, position, (4, 4))

    if path:
        directions = path_to_directions(path)
        commands = directions_to_commands(directions, heading)

        position, heading = follow_commands(
            known_maze, position, heading, commands)

        robot_row, robot_column = position
        print("Final position:", position)
        print("Final heading:", heading)
    else:
        print("No known route to the goal.")

if __name__ == "__main__":
    main()