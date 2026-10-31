# Files and tests

## Python navigation

- `maze_sim.py`: example maze, known-map reference route, movement commands, and demo entry point.
- `exploration.py`: `SimulatedWorld` supplies wall readings; `DiscoveredMap` stores reciprocal edges; `explore()` senses, recalculates distances, turns, and advances.
- `wall_following.py`: differential-drive corridor model with unequal motor gains, side-distance/heading feedback, and sensor dropout.

The grid explorer uses exact cell positions and wall readings. The corridor model tracks position and heading continuously in a separate experiment; it does not drive the grid simulation.

## Browser replay

`export_visual.py` records observations and discovered maps from the Python explorer. It inserts the frames into `visual_template.html` to generate `index.html` and `visual_sim.html`.

The playback controls change how quickly the saved frames are shown. The actual-maze panel is there for comparison; the planner only sees passages it has discovered.

## Arduino

`firmware/maze_robot/Planner.h` stores an 8×8 map and calculates flood-fill distances using a fixed-size queue. The sketch captures ultrasonic echo edges with interrupts, schedules sensors sequentially, and drives the DRV8833 with signed PWM commands.

States are idle, settle, sense, turn, drive, goal, and fault. Turns and cell moves use configured durations that still need calibration on the assembled robot; timer completion updates the stored pose. Side-distance error corrects steering when both side walls are present. A held run button enables motion after calibration is enabled; sensor loss, insufficient front clearance, serial stop, or a driver fault disables it.

## Checks

`check_planner_parity.py` compares the Python and C++ planners on 200 partial maps generated with a fixed random seed. It checks whether they choose the same next move. Both prefer to continue straight when distances tie, then use north/east/south/west. The check adjusts the coordinates for the Python map's extra border row and column on each side.

To reproduce the cross-language check on a system with Python and g++:

```sh
g++ -std=c++11 -Wall -Wextra -Werror firmware/tests/planner_probe.cpp -o planner_probe
python check_planner_parity.py ./planner_probe
```

`controller_experiment.py` records final centering error, wall contact, and time to remain within 5 mm of center. It varies distance and heading-feedback gains, then checks both offset directions, motor mismatches, and sensor dropout. Results are saved in [controller-results.md](controller-results.md) and reproduced in CI.

- Python tests: reciprocal walls, unknown passages, initial headings, empty/unreachable mazes, seeded random mazes, drift correction, command limits, sensor dropout, timing, and invalid settings.
- C++ planner checks: boundaries, reciprocal walls, confirmed openings, an enclosed start, reset, and an open-grid route to the goal.
- GitHub Actions: runs both test sets, executes the Python demo, checks generated replay files, and compiles the sketch for Nano 33 BLE. C++ planner checks use address and undefined-behavior sanitizers.
