"""Compare the embedded planner with Python on seeded partial maps.

Run: python check_planner_parity.py /path/to/compiled/planner_probe
"""
import random
import subprocess
import sys

from exploration import DiscoveredMap, adjacent


def check(binary):
    rng = random.Random(2026)
    fixtures, expected = [], []
    for _ in range(200):
        known = DiscoveredMap(10, 10)
        # Observe each interior edge at most once; leave some unknown.
        for r in range(1, 9):
            for c in range(1, 9):
                for d in (1, 2):
                    if adjacent((r, c), d) in known.cells and rng.random() < 0.7:
                        known.record((r, c), d, rng.random() < 0.3)
        start = (rng.randrange(1, 9), rng.randrange(1, 9))
        goal = (rng.randrange(1, 9), rng.randrange(1, 9))
        heading = rng.randrange(4)
        distances = known.distances(goal)
        choices = [] if start == goal or start not in distances else [
            d for d in range(4) if known.state(start, d) is not True
            and distances.get(adjacent(start, d)) == distances[start] - 1]
        expected.append(heading if heading in choices else choices[0] if choices else -1)
        values = [start[0]-1, start[1]-1, heading, goal[0]-1, goal[1]-1]
        for r in range(1, 9):
            for c in range(1, 9):
                mask = 0
                for d in range(4):
                    state = known.state((r, c), d)
                    if state is True:
                        mask |= 1 << d
                    elif state is False:
                        mask |= 1 << (d + 4)
                values.append(mask)
        fixtures.append(' '.join(map(str, values)))
    result = subprocess.run([binary], input=str(len(fixtures))+'\n'+'\n'.join(fixtures),
                            text=True, capture_output=True, check=True)
    actual = [int(value) for value in result.stdout.split()]
    if actual != expected:
        raise AssertionError([(i, a, e) for i, (a, e) in
                              enumerate(zip(actual, expected)) if a != e] or 'Wrong output count')
    print(f'Python/C++ planner decisions match on all {len(fixtures)} partial maps.')


if __name__ == '__main__':
    check(sys.argv[1])
