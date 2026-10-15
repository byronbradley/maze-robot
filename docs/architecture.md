# How the simulation fits together

## Navigation

`maze_sim.py` defines the example maze and runs both a known-map reference and unknown-map exploration. `exploration.py` separates the simulated environment from the robot's knowledge:

- `SimulatedWorld` reads the actual maze to produce ideal front, left, and right wall observations. It rejects moves into a wall.
- `DiscoveredMap` starts with known dimensions and boundary walls. Interior passages are unknown until observed. Each observation updates the two neighboring cells consistently.
- `explore()` records observations, recalculates flood-fill distances, chooses an adjacent cell toward the goal, and issues a discrete turn or forward move. It senses again after turning before proceeding.

Unknown edges are tentatively open during planning. Movement requires a confirmed open passage. The goal's location and robot's starting pose are supplied; the robot does not have to discover or estimate them.

## Browser replay

`export_visual.py` records the same explorer's observations and map states. It embeds those frames into `visual_template.html`, producing identical `index.html` and `visual_sim.html` files. GitHub Pages serves `index.html`.

The browser plays a recorded trace. Playback speed changes the display timing, not the Python controller or robot dynamics. The true-map panel is for the observer; the planner uses the discovered map only.

## Corridor feedback

`wall_following.py` is a separate continuous-motion experiment. Requested wheel speeds pass through unequal motor gains. Differential-drive equations update heading and position. Side-distance error and heading feedback adjust wheel commands, with output limits. Missing or invalid ranges request zero speed.

The grid explorer does not use these physical positions. Connecting corridor dynamics to maze exploration would require cell-arrival detection, turn control, front-wall braking, and behavior changes at intersections.

## Verification and limits

`test_exploration.py` checks reciprocal wall storage, unknown passages, different initial headings, unreachable goals, and collision-free travel through seeded generated mazes. `test_wall_following.py` checks centering, unequal motors, command limits, and stop/resume behavior during sensor dropout.

GitHub Actions runs the tests, executes the full demo, and checks that generated browser files match their source. These checks verify this simplified software model, not hardware performance.

No physical robot results, ultrasonic noise model, wheel slip model, encoder integration, or Arduino firmware are included. The original project files are unavailable; this repository documents a reconstruction.
