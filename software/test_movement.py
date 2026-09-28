from main import robot_maze, is_open, move_right, move_left, move_down, move_up, get_neighbors, find_path
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



    print("All movement tests passed.")

if __name__ == "__main__":
    check_movement()