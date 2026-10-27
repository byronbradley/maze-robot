# Maze robot

IEEE, University at Buffalo | Fall 2026.

[Open the replay](https://byronbradley.github.io/maze-robot/)

[![Tests](https://github.com/byronbradley/maze-robot/actions/workflows/tests.yml/badge.svg)](https://github.com/byronbradley/maze-robot/actions/workflows/tests.yml)

![The robot's map beside the actual maze](docs/simulation-preview.png)

This project simulates a robot exploring a maze and following corridor walls. The code has not been tested on a physical robot.

It includes a flood-fill planner, wall sensing, turn and forward commands, a browser replay, and a separate test of corridor following. [How the code fits together](docs/architecture.md) covers the files and their limits.

## Run it

Use Python 3.12. No extra packages are needed.

```sh
python maze_sim.py
python -m unittest discover -v
```

The demo first solves the maze with the full map available. It then explores the same maze using wall readings and finishes with the corridor test.

## Maze exploration

The robot starts with the maze dimensions, outer boundary, starting position and heading, and goal coordinates. It reads walls in front, to the left, and to the right. Each reading updates the passage from both neighboring cells.

The planner treats unseen passages as open. Before moving, the robot turns and checks that the next passage is clear. It recalculates distances after each reading and stops with an error if the goal is unreachable. Question marks in the final map show what it never saw.

Positions, turns, and wall readings are exact in this model. There is no sensor noise, wheel slip, or motor feedback. The route found while exploring is not always the shortest route through the actual maze.

## Browser replay

Open `visual_sim.html` in a browser, or use the link above. You can play, pause, step, reset, change speed, and drag the slider through the run. The two panels show the robot's map and the actual maze. The robot only uses its own map.

The replay uses frames recorded by the Python explorer. After changing the maze, explorer, or page template, rebuild it with:

```sh
python export_visual.py
```

This writes `visual_sim.html` and `index.html` from `visual_template.html`. Both files work offline. GitHub's file viewer shows the HTML source, so download or clone the repo to open them locally.

## Corridor experiment

Run `python wall_following.py` to compare driving with and without feedback. A 10 cm wide robot starts 3 cm left of center in a 30 cm corridor. Its left motor runs at 94% of the requested speed. The model updates position and heading, limits wheel speeds, and checks for side-wall contact.

The controller uses the difference between left and right wall distances to steer toward the center. Heading feedback reduces the back-and-forth motion. Commands are wheel speeds in meters per second. Real hardware would need a way to measure heading and convert those speeds to PWM.

Missing or invalid distance or heading readings stop the wheel commands. The demo drops the left sensor for one second, then resumes when readings return. Stopping is instant in this model. The feedback-off run ignores sensor readings.

This test runs separately from maze navigation. It leaves out intersections, range noise, wheel slip, motor response delays, and braking distance. Wall distances are measured perpendicular to the corridor, rather than along a turned sensor's beam.

## Still to do

- Connect maze navigation to movement feedback and controlled turns.
- Verify the firmware, wiring, sensors, and motor driver on real hardware.
- Measure wheel speed, stopping distance, and sensor errors.
- Test the robot in a physical maze and save the results.

Possible parts include an Arduino Nano 33 BLE, a DRV8833 driver, two geared DC motors, wall-distance sensors, a chassis, and a battery. This is a parts plan; the assembly and electrical compatibility have not been checked here.
