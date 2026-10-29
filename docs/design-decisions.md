# Design decisions

## Flood-fill rather than a fixed route

The robot discovers walls during exploration, so a route calculated before sensing can become blocked. Breadth-first search from the goal gives every reachable cell a move count. Recalculating after observations is inexpensive on an 8×8 grid and avoids storing routes that immediately become stale.

Unknown passages remain open in the planning graph to encourage exploration. The motion layer requires a confirmed opening before driving. This separates a tentative route from permission to move.

## Reciprocal edges

A wall belongs to both adjacent cells. Recording east of one cell also records west of the next. The planner tests this invariant because inconsistent edges can make a route appear passable in only one direction.

## Straight-first tie-breaking

Equal-distance choices prefer the current heading to avoid an unnecessary turn. Remaining ties use north/east/south/west so runs are deterministic. The Python/C++ parity check verifies the shared rule on partial maps, including unreachable states.

## Controller terms

Distance error is right range minus left range. A positive error means the robot is nearer the left wall, so the controller increases left-wheel demand and decreases right-wheel demand. Heading feedback damps the resulting turn. It is state feedback, not a full PID controller.

The [gain comparison](controller-results.md) shows why a final error alone is insufficient: some gains finish near center but oscillate until late in the run. The report also records settling time and wall contact. Simulation wheel-speed gains and firmware PWM gains have different units and are configured independently.

## Explicit stop and reset

A missing echo is ambiguous, so the firmware stops rather than treating it as free space. Interrupted motion can leave the chassis between mapped cells. A latched fault therefore requires returning to the starting pose and resetting, rather than resuming from a guessed cell.

## Why timed firmware movement

The pin map allocates signals to three ultrasonic sensors and the motor driver. The current motion interface uses one-cell and quarter-turn durations; encoder arrival detection can replace those timers without changing flood-fill. Timing is sensitive to battery voltage, load, and wheel slip, which is why calibration belongs in the firmware configuration rather than the route planner.
