# Architecture

## Python navigation

- `maze_sim.py`: example maze, known-map reference route, movement commands, and demo entry point.
- `exploration.py`: `SimulatedWorld` supplies wall readings; `DiscoveredMap` stores reciprocal edges; `explore()` senses, recalculates distances, turns, and advances.
- `wall_following.py`: differential-drive corridor model with unequal motor gains, side-distance/heading feedback, and sensor dropout.

The grid explorer uses exact cells and readings. The corridor model updates continuous position and heading separately; it is not the grid robot's movement engine.

## Browser replay

`export_visual.py` records observations and discovered maps from the Python explorer. It inserts the frames into `visual_template.html` to generate `index.html` and `visual_sim.html`.

Playback controls change frame timing. The actual-maze panel is an observer view; navigation uses only discovered edges.

## Arduino

`firmware/maze_robot/Planner.h` stores an 8×8 map and calculates flood-fill distances using a fixed-size queue. The sketch captures ultrasonic echo edges with interrupts, schedules sensors sequentially, and drives the DRV8833 with signed PWM commands.

States are idle, settle, sense, turn, drive, goal, and fault. Turns and cell moves use calibrated durations; timer completion updates the stored pose. Side-distance error corrects steering when both side walls are present. A held run button enables motion; sensor loss, insufficient front clearance, serial stop, or a driver fault disables it.

## Checks

`check_planner_parity.py` sends 200 seeded partial maps to a compiled C++ probe and compares its next-direction decisions with the Python map planner. Both use the same tie-break: continue straight when possible, otherwise north/east/south/west. Map coordinates differ by the Python representation's one-cell outer border; the check translates them explicitly.

`controller_experiment.py` records final centering error, wall contact, and time to remain within 5 mm of center. It varies distance and heading-feedback gains, then checks both offset directions, motor mismatches, and sensor dropout. Results are saved in [controller-results.md](controller-results.md) and reproduced in CI.

- Python tests: reciprocal walls, unknown passages, initial headings, empty/unreachable mazes, seeded random mazes, drift correction, command limits, sensor dropout, timing, and invalid settings.
- C++ planner checks: boundaries, reciprocal walls, confirmed openings, an enclosed start, reset, and an open-grid route to the goal.
- GitHub Actions: runs both test sets, executes the Python demo, checks generated replay files, and compiles the sketch for Nano 33 BLE. C++ planner checks use address and undefined-behavior sanitizers.
