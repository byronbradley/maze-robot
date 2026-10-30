# Maze robot

IEEE, University at Buffalo | Fall 2026

[Open the replay](https://byronbradley.github.io/maze-robot/) · [Firmware](firmware/README.md) · [Wiring](hardware/wiring.md) | [Parts](hardware/parts.md)

[![Tests](https://github.com/byronbradley/maze-robot/actions/workflows/tests.yml/badge.svg)](https://github.com/byronbradley/maze-robot/actions/workflows/tests.yml)

Flood-fill maze navigation for an IEEE project at UB. This repository contains
a Python simulator, a browser replay, and Arduino Nano 33 BLE firmware.

The simulation runs and the firmware compiles in CI. Hardware assembly,
calibration, and physical maze trials are next. The replay and controller
results below come from simulation.

![Simulated discovered map beside the reference maze](docs/simulation-preview.png)

## Run

Python 3.12; no extra packages.

```sh
python maze_sim.py
python -m unittest discover -v
```

The demo compares a full-map route with exploration using front, left, and right wall readings, then runs a corridor-following experiment.

## Checks

[Automated runs](https://github.com/byronbradley/maze-robot/actions/workflows/tests.yml)
check navigation, sensor faults, and controller behavior in Python; compare
Python and C++ planner decisions; and compile the Nano 33 BLE sketch.
They also check that the replay and experiment tables match the source.

For example, the planner tests require a wall observation to update both
adjacent cells, and prevent movement through an unconfirmed passage.
See [architecture and tests](docs/architecture.md) for the individual checks.

## Navigation

The robot starts with its pose, maze dimensions, boundary, and goal. Wall observations update both sides of each passage. Flood-fill treats unseen passages as open when planning, but movement requires a confirmed opening. Distances are recalculated after sensing.

The Python explorer uses exact cell positions and wall readings. Its exploration route can be longer than the shortest route through the completed map.

## Replay

Use the live link above or open `visual_sim.html`. Play, step, change speed, or drag the slider to compare the discovered map with the actual maze.

After changing the maze, explorer, or page template:

```sh
python export_visual.py
```

The exporter records the Python run and generates `index.html` for GitHub Pages and an identical `visual_sim.html` for offline viewing.

## Corridor following

`python wall_following.py` compares feedback on and off in a simulated corridor
with unequal motor speeds. It also drops a sensor reading to check stop and
recovery behavior.

This model is separate from grid navigation. It assumes ideal wall ranges,
known heading, and instantaneous stops. The firmware has no heading sensor,
and uses PWM commands rather than the model's wheel speeds.

[Controller experiments](docs/controller-results.md) compare nine gain combinations and check the defaults with both drift directions and sensor dropout. Reproduce the tables with `python controller_experiment.py`.

## Firmware

The [Arduino sketch](firmware/README.md) targets a DRV8833 motor driver and three
ultrasonic sensors. It includes an 8×8 map, echo capture, and motor-control
states. Cell moves and turns use timers; wheel slip or changing battery voltage
can therefore leave the stored position wrong. Motion is disabled until the
timing constants have been measured and calibration is enabled.

See the firmware guide for build instructions and calibration, and
[design decisions](docs/design-decisions.md) for the planning and control choices.
