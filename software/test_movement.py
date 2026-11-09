from main import (robot_maze, is_open, move_right, move_left, move_down, move_up, get_neighbors, find_path,
                  get_direction, path_to_directions, get_turn, directions_to_commands, apply_turn, move_forward,
                  follow_commands)

from exploration import sense_neighbors, update_known_maze

def check_movement():
    assert move_down(robot_maze, 0, 1) == 1
    assert move_down(robot_maze,0,0) == 0
    assert move_down(robot_maze,4,0) == 4

    assert move_up(robot_maze,0,0) == 0
    assert move_up(robot_maze,1,1) == 0
    assert move_up(robot_maze,2,2) == 2

    assert move_left(robot_maze,0,1) == 0
    assert move_left(robot_maze,0,3) == 3
    assert move_left(robot_maze,0,0) == 0

    assert move_right(robot_maze,0,0) == 1
    assert move_right(robot_maze,0,1) == 1
    assert move_right(robot_maze,0,4) == 4

    assert is_open(robot_maze,0,0)
    assert not is_open(robot_maze,0,2)

    assert get_neighbors(robot_maze, 2, 1) == [(2, 2), (2, 0), (1, 1)]

    small_maze = [[0, 0, 0]]
    assert find_path(small_maze,(0,0),(0,2)) == [(0,0),(0,1),(0,2)]
    assert find_path(small_maze,(0,0),(0,0)) == [(0,0)]
    assert find_path(small_maze, (1, 0), (0, 2)) == []
    assert find_path(small_maze, (-1, 0), (0, 2)) == []
    assert find_path(small_maze, (0, -1), (0, 2)) == []
    assert find_path(small_maze, (0, 3), (0, 2)) == []

    blocked_maze = [[0, 1, 0]]
    assert find_path(blocked_maze, (0,0),(0,2)) == []
    assert find_path(blocked_maze, (0, 1), (0, 2)) == []
    assert find_path(blocked_maze, (0, 0), (0, 1)) == []

    corner_maze = [
        [0, 1],
        [0, 0],
    ]
    assert find_path(corner_maze, (0,0),(1,1)) == [(0,0), (1,0), (1,1)]
    assert find_path(corner_maze, (1, 1), (0, 0)) == [(1, 1), (1, 0), (0, 0)]

    assert get_direction((1, 1), (1, 2)) == "right"
    assert get_direction((1, 1), (1, 0)) == "left"
    assert get_direction((1, 1), (2, 1)) == "down"
    assert get_direction((1, 1), (0, 1)) == "up"
    assert get_direction((1, 1), (1, 1)) is None
    assert get_direction((1, 1), (2, 2)) is None
    assert get_direction((1, 1), (1, 3)) is None

    path = [(0, 0), (0, 1), (1, 1)]
    assert path_to_directions(path) == ["right", "down"]
    assert path_to_directions([]) == []
    assert path_to_directions([(0, 0)]) == []

    square_path = [(0, 0), (0, 1), (1, 1), (1, 0), (0, 0)]
    assert path_to_directions(square_path) == ["right", "down", "left", "up"]

    assert get_turn("right", "right") == "straight"
    assert get_turn("right", "down") == "right"
    assert get_turn("right", "left") == "around"
    assert get_turn("right", "up") == "left"
    assert get_turn("left", "up") == "right"

    assert directions_to_commands(["right", "down"], "right") == [
        ("straight", "forward"),
        ("right", "forward"),]
    assert directions_to_commands([], "right") == []
    assert directions_to_commands(["up", "down"], "right") == [
        ("left", "forward"),
        ("around", "forward"),]

    assert apply_turn("right", "straight") == "right"
    assert apply_turn("right", "right") == "down"
    assert apply_turn("right", "left") == "up"
    assert apply_turn("right", "around") == "left"
    assert apply_turn("left", "right") == "up"

    assert move_forward(robot_maze, 0, 0, "right") == (0, 1)
    assert move_forward(robot_maze, 0, 1, "down") == (1, 1)
    assert move_forward(robot_maze, 1, 1, "up") == (0, 1)
    assert move_forward(robot_maze, 0, 1, "left") == (0, 0)
    assert move_forward(robot_maze, 0, 0, "down") == (0, 0)
    assert move_forward(robot_maze, 0, 0, "up") == (0, 0)

    row, column = 0, 0
    heading = "up"
    path = find_path(robot_maze, (0, 0), (4, 4))
    directions = path_to_directions(path)
    commands = directions_to_commands(directions, heading)

    position, heading = follow_commands(robot_maze, (0, 0), heading, commands)
    assert position == (4, 4)
    assert heading == "down"

    two_routes_maze = [
        [0, 0, 0],
        [0, 1, 0],
        [0, 0, 0],]
    assert find_path(two_routes_maze, (0, 0), (0, 2)) == [
        (0, 0), (0, 1), (0, 2)]
    two_routes_maze[0][1] = 1
    assert find_path(two_routes_maze, (0, 0), (0, 2)) == [
        (0, 0), (1, 0), (2, 0), (2, 1),
        (2, 2), (1, 2), (0, 2)]
    two_routes_maze[1][0] = 1
    assert find_path(two_routes_maze, (0, 0), (0, 2)) == []

    position, heading = follow_commands(
        robot_maze,
        (0, 0),
        "right",
        [("right", "forward"), ("left", "forward")])
    assert position == (0, 0)
    assert heading == "down"

    position, heading = follow_commands(
        robot_maze, (0, 0), "right", [])
    assert position == (0, 0)
    assert heading == "right"

    assert sense_neighbors(robot_maze, 0, 0) == {
        (0, 1): 0,
        (1, 0): 1,}

    maze = [[0, 0, 1]]
    known = [[0, None, None]]
    update_known_maze(maze, known, 0, 0)
    assert known == [[0, 0, None]]
    update_known_maze(maze, known, 0, 1)
    assert known == [[0, 0, 1]]

    print("All movement tests passed.")

if __name__ == "__main__":
    check_movement()