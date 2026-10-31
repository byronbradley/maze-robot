# Design notes

## Flood-fill rather than a fixed route

I used flood-fill because the robot learns where the walls are as it moves. A fixed route can lead into a wall it hasn't seen yet. Breadth-first search from the goal gives each reachable cell a move count, and the 8×8 grid is small enough to recalculate after each set of readings.

The planner treats unknown passages as open so it can explore. Before driving into one, the robot needs a reading that confirms it is open.

## Recording a wall from both sides

A wall belongs to both adjacent cells. Recording a wall east of one cell also records it west of the next. The tests check both sides; otherwise, a passage could look open from one direction and closed from the other.

## Choosing between equal routes

When two moves have the same distance to the goal, the planner prefers to keep going straight. Remaining ties use north/east/south/west, so repeated runs make the same choice. The Python/C++ comparison checks this rule on partial maps, including cases with no route to the goal.

## Controller terms

Distance error is right range minus left range. A positive error means the robot is nearer the left wall, so the controller increases left-wheel demand and decreases right-wheel demand. Heading feedback damps the resulting turn. It is state feedback, not a full PID controller.

Some gains finish near the center but oscillate for much of the run. That's why the [gain comparison](controller-results.md) records settling time and wall contact as well as final error. The simulation controls wheel speed and the firmware controls PWM duty, so their gains have different units and separate settings.

## Stopping after a fault

A missing echo could mean open space or a failed reading. The firmware stops because it can't tell which. A stop halfway through a move also leaves the stored cell position unreliable. After a latched fault, the robot must be returned to its starting cell and heading before resetting.

## Timed movement

The firmware uses timers for one-cell moves and quarter turns. I still need to measure those timings on the assembled robot. Motion is disabled until calibration is enabled. Timing can vary with battery voltage, load, and wheel slip. Encoder feedback could replace the timers later without changing the flood-fill planner.
