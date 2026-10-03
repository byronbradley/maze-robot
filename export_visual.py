"""Generate a standalone browser replay from the Python exploration algorithm."""
import json
from pathlib import Path
from exploration import SimulatedWorld, DiscoveredMap, explore
from maze_sim import MAZE, find


class RecordedWorld(SimulatedWorld):
    def __init__(self, maze, goal):
        super().__init__(maze)
        self.known = DiscoveredMap(len(maze), len(maze[0]))
        self.frames = []
        self.goal = goal
        self.visited = set()

    def sense(self, cell, heading):
        readings = super().sense(cell, heading)
        self.visited.add(cell)
        for _, direction, wall in readings:
            self.known.record(cell, direction, wall)
        distances = self.known.distances(self.goal)
        self.frames.append(dict(position=cell, heading=heading,
            readings=[dict(sensor=label, wall=wall) for label, _, wall in readings],
            visited=sorted(self.visited),
            walls=[[r, c, d, wall] for ((r, c), d), wall in self.known.walls.items()
                   if (r, c) in self.known.cells],
            distances=[[r, c, distance] for (r, c), distance in distances.items()]))
        return readings


def main():
    root = Path(__file__).resolve().parent
    start, goal = find(MAZE, 'S'), find(MAZE, 'G')
    world = RecordedWorld(MAZE, goal)
    route, _, _ = explore(world, start, goal)
    data = dict(maze=MAZE, start=start, goal=goal, frames=world.frames,
                moves=len(route) - 1)
    template = (root / 'visual_template.html').read_text(encoding='utf-8')
    (root / 'visual_sim.html').write_text(template.replace('/*REPLAY_DATA*/null',
        json.dumps(data)), encoding='utf-8')
    print(f'Exported {len(world.frames)} frames and {len(route)-1} moves to visual_sim.html')


if __name__ == '__main__':
    main()
