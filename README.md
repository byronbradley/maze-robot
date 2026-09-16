# Autonomous Maze-Solving Robot

IEEE, University at Buffalo | Fall 2026.

A step-by-step project for learning how a two-wheel robot senses walls and navigates a maze.

## Current status

This repository reconstructs and documents an earlier robot project. The original code and test data are unavailable. It includes a runnable Python demonstration of flood-fill route planning and heading-based movement commands. Hardware integration and physical navigation have not been verified here.

## Run the simulation

With Python 3 installed, run `python maze_sim.py`.

The program first prints a known-map reference route and movement commands. It then runs unknown-maze exploration with a separate discovered map. Only maze dimensions, the closed boundary, the starting pose, and goal coordinates are initially known to the robot.

Ideal front/left/right sensors report whether adjacent passages are blocked. Observations update both sides of each passage. Unknown passages are tentatively open for flood-fill planning, but the robot turns and senses before entering one. It recalculates distances after sensing and stops with an error if the goal becomes unreachable. The final discovered map retains question marks for unseen passages and cells.

The simulator assumes perfect cell positioning, turns, and wall detection. It does not model ultrasonic echo times, sensor noise, motor physics, or physical movement feedback. An exploration route is not guaranteed to be the true shortest route.

Run checks with `python -m unittest test_exploration.py`.

## Learning plan

1. Understand differential-drive movement: straight motion, curves, and turns.
2. Learn motor direction control with an H-bridge and speed control with PWM.
3. Measure wall distance and handle invalid sensor readings.
4. Implement and test stopping and corridor following.
5. Represent maze cells and walls in software.
6. Implement flood-fill route planning in a simulation.
7. Integrate with hardware and document measured results.

## Hardware planning

Potential components include an Arduino Nano 33 BLE, a DRV8833 motor driver, two geared DC motors, wall-distance sensors, a chassis, and a suitable battery. These are planned components, not a record of completed assembly. Exact electrical compatibility and wiring must be checked before powering hardware.

## Documentation standard

Record what was built, what was tested, the observed results, and remaining limitations. Identify simulations separately from physical robot tests. If earlier project files are added, describe their source and original dates accurately.
