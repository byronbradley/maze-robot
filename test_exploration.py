"""Checks for hidden-map exploration and collision-free movement."""
import random
import unittest

from exploration import DiscoveredMap, SimulatedWorld, explore
from maze_sim import MAZE, find, flood_fill


class ExplorationTests(unittest.TestCase):
    def test_unknown_and_reciprocal_walls(self):
        known = DiscoveredMap(7, 9)
        self.assertIsNone(known.state((2, 2), 1))
        known.record((2, 2), 1, True)
        self.assertIs(known.state((2, 3), 3), True)
        self.assertIs(known.state((1, 1), 0), True)

    def test_demo_all_starting_headings(self):
        for heading in range(4):
            route, _, known = explore(SimulatedWorld(MAZE), find(MAZE, 'S'),
                                      find(MAZE, 'G'), heading)
            self.assertEqual(route[-1], find(MAZE, 'G'))
            self.assertTrue(any(known.state((5, 4), d) is None for d in range(4)))

    def test_unreachable_goal(self):
        maze = ('#####', '#S#G#', '#####')
        with self.assertRaisesRegex(ValueError, 'unreachable'):
            explore(SimulatedWorld(maze), (1, 1), (1, 3))

    def test_seeded_mazes(self):
        rng = random.Random(42)
        checked = 0
        for _ in range(100):
            rows = [['#'] * 9 for _ in range(9)]
            for r in range(1, 8):
                for c in range(1, 8):
                    rows[r][c] = '#' if rng.random() < 0.25 else '.'
            rows[1][1], rows[7][7] = 'S', 'G'
            maze = tuple(''.join(row) for row in rows)
            if (1, 1) not in flood_fill(maze, (7, 7)):
                continue
            route, _, _ = explore(SimulatedWorld(maze), (1, 1), (7, 7))
            self.assertEqual(route[-1], (7, 7))
            for a, b in zip(route, route[1:]):
                self.assertEqual(abs(a[0] - b[0]) + abs(a[1] - b[1]), 1)
                self.assertNotEqual(maze[b[0]][b[1]], '#')
            checked += 1
        self.assertGreater(checked, 30)


if __name__ == '__main__':
    unittest.main()
