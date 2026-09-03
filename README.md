# Autonomous Maze-Solving Robot

IEEE, University at Buffalo | Fall 2026.

A step-by-step project for learning how a two-wheel robot senses walls and navigates a maze.

## Current status

This repository reconstructs and documents an earlier robot project. The original code and test data are unavailable. It currently contains a learning plan; reconstructed hardware integration and maze navigation have not been implemented or verified here.

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
