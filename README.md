# Maze robot

IEEE, University at Buffalo | Fall 2026

[Simulation replay](https://byronbradley.github.io/maze-robot/) · [Firmware](firmware/README.md) · [Wiring](hardware/wiring.md) · [Parts](hardware/parts.md)

[![Tests](https://github.com/byronbradley/maze-robot/actions/workflows/tests.yml/badge.svg)](https://github.com/byronbradley/maze-robot/actions/workflows/tests.yml)

My part of this IEEE project is the Python maze simulator and C++ firmware for
an Arduino Nano 33 BLE Sense Rev2. The robot is meant to find a goal without knowing the
interior walls in advance. It builds a map from front, left, and right wall
readings, then uses flood-fill to choose its next move.

The simulation runs and the firmware compiles in GitHub Actions. Assembly,
calibration, and physical trials are next. All results here are from simulation
or software tests.

![Simulated discovered map beside the reference maze](docs/simulation-preview.png)

## Run the simulation

Use Python 3.12. No extra packages are needed.

```sh
python maze_sim.py
python -m unittest discover -v
```

The demo compares a route through the known maze with a route found by
exploring it. It also runs a separate corridor-following experiment.

## How the planner works

The planner knows the starting cell, heading, maze size, outer boundary, and
goal. Each wall reading updates both cells beside that passage. Flood-fill
then recalculates the distance to the goal.

Unseen passages count as open when planning, but the robot must confirm an
opening before moving through it. This lets it explore without treating a
guess as a safe move. The route it takes while discovering walls can be longer
than the shortest route through the finished map.

The Python simulation uses exact cell positions and wall readings. It does
not model the physical error in a turn or a one-cell move.

## Firmware and movement

The [Arduino sketch](firmware/README.md) has an 8×8 map and controls a DRV8833
motor driver with three ultrasonic sensors. Moves and turns use timers, so
battery voltage, load, and wheel slip can put the robot somewhere other than
its stored position. Motion is disabled until the timing constants have been
measured and calibration is enabled.

The firmware guide covers the serial commands and calibration settings.
[Design notes](docs/design-decisions.md) explain the planning and control choices.

## Corridor experiment

`python wall_following.py` compares steering feedback on and off with unequal
motor speeds. It also removes a sensor reading to check stopping and recovery.
This is a separate model from the grid navigation above.

The [controller results](docs/controller-results.md) compare nine gain
combinations. The model assumes ideal wall ranges, known heading, and instant
stops. The firmware uses PWM commands and has no heading feedback, so these
gains cannot be copied directly to the robot. Run `python controller_experiment.py`
to reproduce the tables.

## Tests

The tests check wall-map consistency, blocked and unknown passages, sensor
faults, and controller behavior. For example, recording a wall east of one
cell must also record a wall west of its neighbor.

[GitHub Actions](https://github.com/byronbradley/maze-robot/actions/workflows/tests.yml)
also compares the Python and C++ planners on the same partial maps, compiles
the Nano sketch, and checks that the saved replay and result tables match the
source. The [file and test guide](docs/architecture.md) lists the individual checks.

## Replay files

The [browser replay](https://byronbradley.github.io/maze-robot/) shows the map
being discovered beside the actual maze. Play it, step through it, or drag the
slider to inspect a particular reading. For an offline copy, open `visual_sim.html`.

After changing the maze, explorer, or page template, regenerate both replay files:

```sh
python export_visual.py
```

The exporter writes identical copies to `index.html` for GitHub Pages and
`visual_sim.html` for local viewing.
