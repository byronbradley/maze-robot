"""Run the maze planner and corridor demo with python maze_sim.py.

The maze uses exact cell positions and wall readings. The corridor demo
models motor drift separately. Neither runs on physical hardware.
"""

from collections import deque

from exploration import SimulatedWorld, explore, render_discovered
from wall_following import demo as wall_following_demo

# # = wall, . = open cell, S = start, G = goal.
MAZE = (
    "#########",
    "#S..#..G#",
    "#.#.#.#.#",
    "#.#...#.#",
    "#.#####.#",
    "#.......#",
    "#########",
)


def neighbors(maze, cell):
    """Find open neighbors above, right, below, and left of a cell."""
    row, col = cell
    for dr, dc in ((-1, 0), (0, 1), (1, 0), (0, -1)):
        nr, nc = row + dr, col + dc
        if 0 <= nr < len(maze) and 0 <= nc < len(maze[nr]):
            if maze[nr][nc] != "#":
                yield nr, nc


def find(maze, symbol):
    matches = [
        (r, c)
        for r, line in enumerate(maze)
        for c, value in enumerate(line)
        if value == symbol
    ]
    if len(matches) != 1:
        raise ValueError(f"Expected exactly one {symbol}")
    return matches[0]


def flood_fill(maze, goal):
    """Count the shortest number of moves from each reachable cell to the goal."""
    distances = {goal: 0}
    queue = deque([goal])
    while queue:
        cell = queue.popleft()
        for neighbor in neighbors(maze, cell):
            if neighbor not in distances:
                distances[neighbor] = distances[cell] + 1
                queue.append(neighbor)
    return distances


def route_to_goal(maze, distances, start, goal):
    if start not in distances:
        raise ValueError("The goal is unreachable from the start")
    route = [start]
    while route[-1] != goal:
        current = route[-1]
        next_cell = next(
            n
            for n in neighbors(maze, current)
            if distances.get(n) == distances[current] - 1
        )
        route.append(next_cell)
    return route


def movement_commands(route, initial_heading="east"):
    """Turn a route into turn and forward commands.

    Track the heading after each turn. These commands assume perfect movement;
    no wheel or position feedback is available here.
    """
    headings = ("north", "east", "south", "west")
    heading = headings.index(initial_heading)
    direction_for_step = {(-1, 0): 0, (0, 1): 1, (1, 0): 2, (0, -1): 3}
    commands = []
    for current, target in zip(route, route[1:]):
        step = (target[0] - current[0], target[1] - current[1])
        if step not in direction_for_step:
            raise ValueError("Route must move one adjacent cell at a time")
        target_heading = direction_for_step[step]
        turn = (target_heading - heading) % 4
        if turn:
            commands.append(
                {
                    1: "Turn right 90 degrees",
                    2: "Turn around 180 degrees",
                    3: "Turn left 90 degrees",
                }[turn]
            )
        heading = target_heading
        commands.append(
            f"Drive forward one cell to {target}, facing {headings[heading]}"
        )
    return commands


def main():
    start, goal = find(MAZE, "S"), find(MAZE, "G")
    distances = flood_fill(MAZE, goal)
    route = route_to_goal(MAZE, distances, start, goal)
    print("KNOWN MAZE (S = start, G = goal)")
    print("\n".join(MAZE))
    print("\nFLOOD-FILL: shortest number of moves to G")
    for r, line in enumerate(MAZE):
        print(
            " ".join(
                (
                    " ##"
                    if value == "#"
                    else f"{distances[(r, c)]:3}" if (r, c) in distances else " --"
                )
                for c, value in enumerate(line)
            )
        )
    print("\nROUTE (* = intermediate route cell)")
    route_cells = set(route[1:-1])
    for r, line in enumerate(MAZE):
        print(
            "".join(
                "*" if (r, c) in route_cells else value for c, value in enumerate(line)
            )
        )
    print(f"\nReached the goal in {len(route) - 1} moves.")
    print("Coordinates (row, column), starting from zero:")
    print(" -> ".join(map(str, route)))
    print("\nPLANNED MOVEMENT COMMANDS (starting heading: east)")
    for number, command in enumerate(movement_commands(route), start=1):
        print(f"{number:2}. {command}")
    print("\nThese are simulated commands, not verified physical movements.")
    print("\nUNKNOWN-MAZE EXPLORATION (only dimensions and goal initially known)")
    explored_route, log, discovered = explore(SimulatedWorld(MAZE), start, goal)
    print("\n".join(log))
    print(f"\nReached goal after {len(explored_route) - 1} exploration moves.")
    print("DISCOVERED MAP: R=robot, S=start, .=visited, ?=unknown, #=wall")
    print(render_discovered(discovered, set(explored_route), start, goal, goal))
    wall_following_demo()


if __name__ == "__main__":
    main()
