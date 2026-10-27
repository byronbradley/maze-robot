# How the code fits together

## Navigation

`maze_sim.py` holds the example maze. It first solves it with the full map, then runs the explorer with only wall readings. The explorer lives in `exploration.py`:

- `SimulatedWorld` reads the actual maze and returns front, left, and right wall readings. It blocks moves into walls.
- `DiscoveredMap` stores what the robot has seen. It starts with the maze dimensions and outer boundary. Each wall reading updates both sides of a passage.
- `explore()` records readings, recalculates distances, and picks a turn or forward move. After turning, it checks the sensors again before moving.

Planning treats unknown passages as open, but the robot must check before entering one. The starting position, heading, and goal are supplied. Position and wall readings are exact.

## Browser replay

`export_visual.py` records the explorer's readings and maps, then puts those frames into `visual_template.html`. It writes the same page to `index.html` and `visual_sim.html`. GitHub Pages serves `index.html`; either file can be opened offline.

The browser plays back that recording. Changing playback speed only changes how fast frames appear. The actual-maze panel lets the viewer compare maps; the planner cannot read it.

## Corridor feedback

`wall_following.py` tests a robot driving down a straight corridor. Each motor can run at a different fraction of the requested speed. Those wheel speeds update the robot's position and heading. The controller adjusts the commands using left/right wall distances and heading feedback. Missing or invalid feedback stops the wheel commands.

The maze explorer still moves one cell at a time. Connecting it to this model would need a way to detect arrival at a cell, control turns, stop for front walls, and handle intersections.

## Tests and limits

`test_exploration.py` checks wall storage in both directions, unseen passages, starting headings, empty mazes, unreachable goals, and travel through random mazes with a fixed seed. `test_wall_following.py` checks drift correction, wheel-speed limits, sensor dropout, simulation timing, and invalid settings.

GitHub Actions runs the tests and full demo, then rebuilds the replay to check that the saved HTML matches the Python source and template.

These tests cover the simulation. There are no physical robot measurements, ultrasonic noise or wheel-slip models, encoder integration, or Arduino firmware here.
