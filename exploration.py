"""Ideal cell-based sensing and online flood-fill exploration."""

from collections import deque

DIRECTIONS = ((-1, 0), (0, 1), (1, 0), (0, -1))
NAMES = ("north", "east", "south", "west")


def adjacent(cell, direction):
    dr, dc = DIRECTIONS[direction]
    return cell[0] + dr, cell[1] + dc


class DiscoveredMap:
    """Known dimensions and boundary; interior passage states start unknown.

    Edges are stored in both directions: True = wall, False = open.
    Missing edges mean unknown and are tentatively open for planning.
    """

    def __init__(self, height, width):
        self.cells = {(r, c) for r in range(1, height - 1)
                      for c in range(1, width - 1)}
        self.walls = {}

    def record(self, cell, direction, wall):
        other = adjacent(cell, direction)
        self.walls[cell, direction] = wall
        self.walls[other, (direction + 2) % 4] = wall

    def state(self, cell, direction):
        if adjacent(cell, direction) not in self.cells:
            return True
        return self.walls.get((cell, direction))

    def distances(self, goal):
        distances = {goal: 0}
        queue = deque([goal])
        while queue:
            cell = queue.popleft()
            for direction in range(4):
                other = adjacent(cell, direction)
                if self.state(cell, direction) is not True and other not in distances:
                    distances[other] = distances[cell] + 1
                    queue.append(other)
        return distances


class SimulatedWorld:
    """Only this component reads the true wall layout."""

    def __init__(self, maze):
        if not maze or len({len(row) for row in maze}) != 1:
            raise ValueError("Maze must be a nonempty rectangle")
        if any(value != "#" for value in maze[0] + maze[-1]):
            raise ValueError("Maze needs a closed outer boundary")
        if any(row[0] != "#" or row[-1] != "#" for row in maze):
            raise ValueError("Maze needs a closed outer boundary")
        self.maze = maze

    def sense(self, cell, heading):
        readings = []
        for label, offset in (("front", 0), ("left", -1), ("right", 1)):
            direction = (heading + offset) % 4
            r, c = adjacent(cell, direction)
            readings.append((label, direction, self.maze[r][c] == "#"))
        return readings

    def move(self, cell, direction):
        target = adjacent(cell, direction)
        if self.maze[target[0]][target[1]] == "#":
            raise RuntimeError("Attempted collision")
        return target


def explore(world, start, goal, initial_heading=1, max_cycles=10000):
    discovered = DiscoveredMap(len(world.maze), len(world.maze[0]))
    position, heading = start, initial_heading
    route, log = [start], []
    for cycle in range(max_cycles):
        readings = world.sense(position, heading)
        for _, direction, wall in readings:
            discovered.record(position, direction, wall)
        log.append(f"At {position}, facing {NAMES[heading]}: " + ", ".join(
            f"{label}={'wall' if wall else 'open'}" for label, _, wall in readings))
        if position == goal:
            return route, log, discovered
        distances = discovered.distances(goal)
        if position not in distances:
            raise ValueError("Goal unreachable according to discovered walls")
        choices = [d for d in range(4)
                   if discovered.state(position, d) is not True
                   and distances.get(adjacent(position, d)) == distances[position] - 1]
        # Prefer continuing straight when shortest-distance choices tie.
        direction = heading if heading in choices else choices[0]
        turn = (direction - heading) % 4
        if turn:
            log.append({1: "Turn right 90 degrees", 2: "Turn around 180 degrees",
                        3: "Turn left 90 degrees"}[turn])
            heading = direction
            # Re-sense after turning, including a previously unseen rear passage.
            continue
        if discovered.state(position, heading) is not False:
            raise RuntimeError("Refusing to enter an unconfirmed passage")
        position = world.move(position, heading)
        route.append(position)
        log.append(f"Drive forward one cell to {position}; replan after sensing")
    raise RuntimeError("Exploration exceeded the cycle limit")


def render_discovered(discovered, visited, start, goal, position):
    """Draw known edges without reading the world's hidden maze."""
    height = max(r for r, _ in discovered.cells)
    width = max(c for _, c in discovered.cells)
    drawing = [[" " for _ in range(width * 2 + 1)]
               for _ in range(height * 2 + 1)]
    for cell in sorted(discovered.cells):
        r, c = cell
        y, x = 2 * r - 1, 2 * c - 1
        drawing[y][x] = "R" if cell == position else "S" if cell == start else (
            "G" if cell == goal else "." if cell in visited else "?")
        for direction, (dr, dc) in enumerate(DIRECTIONS):
            state = discovered.state(cell, direction)
            drawing[y + dr][x + dc] = "#" if state is True else " " if state is False else "?"
    for y in range(0, len(drawing), 2):
        for x in range(0, len(drawing[0]), 2):
            drawing[y][x] = "+"
    return "\n".join("".join(row) for row in drawing)
