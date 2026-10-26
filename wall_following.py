"""Simplified differential-drive corridor model, in meters and seconds.

Positive lateral offset is toward the left wall. Positive heading points left.
This is a separate continuous-motion experiment, not the grid explorer's physics.
"""
import math


def motor_commands(left_distance, right_distance, heading):
    """Return bounded wheel speeds; stop on missing ranges or heading."""
    if any(value is None or not math.isfinite(value) or value < 0
           for value in (left_distance, right_distance)):
        return 0.0, 0.0
    if heading is None or not math.isfinite(heading):
        return 0.0, 0.0
    base_speed, max_speed = 0.12, 0.20
    kp, kd = 2.0, 0.6
    error = right_distance - left_distance
    correction = kp * error + kd * heading
    return (max(0.0, min(max_speed, base_speed + correction)),
            max(0.0, min(max_speed, base_speed - correction)))


def simulate(wall_following=True, duration=8.0, dt=0.01,
             left_gain=0.94, right_gain=1.0, initial_offset=0.03,
             corridor_width=0.30, robot_width=0.10, dropout_window=None):
    for name, value in (('duration', duration), ('dt', dt),
                        ('left_gain', left_gain), ('right_gain', right_gain),
                        ('initial_offset', initial_offset),
                        ('corridor_width', corridor_width), ('robot_width', robot_width)):
        if not math.isfinite(value):
            raise ValueError(f'{name} must be finite')
    if dt <= 0 or duration <= 0:
        raise ValueError('duration and dt must be positive')
    if robot_width <= 0 or corridor_width <= robot_width:
        raise ValueError('Corridor width must exceed a positive robot width')
    wheelbase = 0.10
    base_speed = 0.12
    x, offset, heading = 0.0, initial_offset, 0.0
    history, collision = [], False
    clearance_limit = (corridor_width - robot_width) / 2
    for step in range(math.ceil(duration / dt) + 1):
        elapsed = min(step * dt, duration)
        left_distance = corridor_width / 2 - offset
        right_distance = corridor_width / 2 + offset
        # A half-open time interval simulates loss of the left sensor.
        if dropout_window is not None and dropout_window[0] <= elapsed < dropout_window[1]:
            left_distance = None
        if wall_following:
            left_command, right_command = motor_commands(left_distance, right_distance, heading)
        else:
            left_command = right_command = base_speed
        history.append(dict(time=elapsed, x=x, offset=offset, heading=heading,
                            left_distance=left_distance, right_distance=right_distance,
                            left_command=left_command, right_command=right_command))
        if abs(offset) >= clearance_limit:
            collision = True
            break
        if elapsed >= duration:
            break
        # The last step may be shorter than dt.
        step_dt = min(dt, duration - elapsed)
        left_speed = left_command * left_gain
        right_speed = right_command * right_gain
        speed = (left_speed + right_speed) / 2
        angular_speed = (right_speed - left_speed) / wheelbase
        x += speed * math.cos(heading) * step_dt
        offset += speed * math.sin(heading) * step_dt
        heading += angular_speed * step_dt
    return history, collision


def demo():
    print("\nCORRIDOR DRIFT EXPERIMENT")
    print("30 cm corridor; 10 cm robot; starts 3 cm left of center.")
    print("Left motor produces 94% of commanded speed; right produces 100%.")
    print("Controller uses ideal wall ranges plus heading feedback for damping.")
    for enabled in (False, True):
        history, collision = simulate(wall_following=enabled)
        last = history[-1]
        print(f"\nWall following {'ON' if enabled else 'OFF'}:")
        print(f"  Elapsed: {last['time']:.2f} s; forward position: {last['x']:.3f} m")
        print(f"  Final offset: {last['offset'] * 100:.2f} cm left of center")
        print(f"  Wall contact: {'yes' if collision else 'no'}")
        if enabled:
            print("  Time(s)   Offset(cm)   Left command(m/s)   Right command(m/s)")
            for row in history[::100]:
                print(f"  {row['time']:6.2f}   {row['offset']*100:10.2f}"
                      f"   {row['left_command']:17.3f}   {row['right_command']:18.3f}")
    print("Model excludes intersections, range noise, wheel slip, and motor dynamics.")
    history, collision = simulate(dropout_window=(2.0, 3.0))
    stopped = [row for row in history if row['left_distance'] is None]
    print(f"\nSENSOR DROPOUT: left sensor unavailable from 2.0 to 3.0 seconds.")
    print(f"  Stopped for {len(stopped)} updates; resumed when readings returned.")
    print(f"  Final offset: {history[-1]['offset'] * 100:.2f} cm; wall contact: {collision}")


if __name__ == '__main__':
    demo()
