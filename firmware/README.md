# Nano 33 BLE firmware

The sketch is compiled in CI. The physical build and bench testing are planned;
the motion constants still need measurement on the assembled robot.

Open `maze_robot/maze_robot.ino` with **Arduino Nano 33 BLE** selected. The sketch uses a DRV8833 carrier, two DC motors, and three HC-SR04P sensors powered at 3.3 V. The selected controller is Nano 33 BLE Sense Rev2 (ABX00070); its onboard sensors are not used. [Wiring and pin assignments](../hardware/wiring.md).

## Build

Install **Arduino Mbed OS Nano Boards 4.6.0** in Arduino IDE, or use Arduino CLI from the repository root:

```sh
arduino-cli core install arduino:mbed_nano@4.6.0
arduino-cli compile --fqbn arduino:mbed_nano:nano33ble firmware/maze_robot
```

GitHub Actions compiles the sketch and runs native C++ planner tests.

## Controls

Serial Monitor: **115200 baud**.

| Command | Action |
|---|---|
| `p` | Print front, left, and right ranges |
| `g` | Start when calibration is enabled, the run button is held, and readings are valid |
| `s` | Disable the driver and latch a stop |
| `r` | Disable the driver and reset map/pose |

Releasing the run button also latches a stop. Return the robot to its starting cell and heading before `r`; an interrupted move can leave its position between cells.

## Configuration

- Map: 8×8; start `(7, 0)` facing north; goal `(0, 7)`. Change these in `Planner.h` for the maze.
- `CELL_MS` and `QUARTER_TURN_MS`: time to travel one cell and turn 90°. Motion uses timers rather than encoders or an IMU.
- `DRIVE_PWM`, `TURN_PWM`, and motor inversion flags: tune speed and direction for the chassis.
- `WALL_CM`, `FRONT_STOP_CM`, and `SIDE_KP`: wall classification, minimum front clearance, and side-distance correction.
- `MOTION_CALIBRATED`: defaults to `false`. Measure and set the motion constants before enabling it.

## Sensing and movement

Sensors transmit one at a time, 65 ms apart. Interrupts capture echo pulse widths. Missing echoes and readings older than 260 ms are invalid. Each turn is followed by a settling interval and a new scan; forward movement requires a confirmed opening.

Side-wall correction runs only when both side walls are detected. Invalid readings, a driver fault, or front clearance below the threshold latch a stop. The driver coasts when disabled, so set speed and clearance to allow stopping distance. A missing echo stops navigation even if it came from an open space beyond sensor range.
