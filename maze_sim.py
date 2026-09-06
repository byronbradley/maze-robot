"""Flood-fill demonstration with a known maze. No physical hardware required.

Run: python maze_sim.py
This plans a route through a complete map; it does not simulate sensors,
motor movement, or exploration of an unknown maze.
"""

from collections import deque

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
    """Yield adjacent open cells; diagonal movement is not allowed."""
    row, col = cell
    for dr, dc in ((-1, 0), (0, 1), (1, 0), (0, -1)):
        nr, nc = row + dr, col + dc
        if 0 <= nr < len(maze) and 0 <= nc < len(maze[nr]):
            if maze[nr][nc] != "#":
                yield nr, nc


def find(maze, symbol):
    matches = [(r, c) for r, line in enumerate(maze)
               for c, value in enumerate(line) if value == symbol]
    if len(matches) != 1:
        raise ValueError(f"Expected exactly one {symbol}")
    return matches[0]


def flood_fill(maze, goal):
    """Assign each reachable cell its shortest move count to the goal."""
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
        next_cell = next(n for n in neighbors(maze, current)
                         if distances.get(n) == distances[current] - 1)
        route.append(next_cell)
    return route


def main():
    start, goal = find(MAZE, "S"), find(MAZE, "G")
    distances = flood_fill(MAZE, goal)
    route = route_to_goal(MAZE, distances, start, goal)
    print("KNOWN MAZE (S = start, G = goal)")
    print("\n".join(MAZE))
    print("\nFLOOD-FILL: shortest number of moves to G")
    for r, line in enumerate(MAZE):
        print(" ".join(" ##" if value == "#" else
                       f"{distances[(r, c)]:3}" if (r, c) in distances else " --"
                       for c, value in enumerate(line)))
    print("\nROUTE (* = intermediate route cell)")
    route_cells = set(route[1:-1])
    for r, line in enumerate(MAZE):
        print("".join("*" if (r, c) in route_cells else value
                      for c, value in enumerate(line)))
    print(f"\nReached the goal in {len(route) - 1} moves.")
    print("Coordinates (row, column), starting from zero:")
    print(" -> ".join(map(str, route)))


if __name__ == "__main__":
    main()
