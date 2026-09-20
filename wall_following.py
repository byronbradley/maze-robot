"""Simplified differential-drive corridor model, in meters and seconds.

Positive lateral offset is toward the left wall. Positive heading points left.
This is a separate continuous-motion experiment, not the grid explorer's physics.
"""
import math


def simulate(wall_following=True, duration=8.0, dt=0.01,
             left_gain=0.94, right_gain=1.0, initial_offset=0.03,
             corridor_width=0.30, robot_width=0.10):
    wheelbase = 0.10
    base_speed, max_speed = 0.12, 0.20
    # Heading feedback damps oscillation; side-distance feedback centers the robot.
    kp, kd = 2.0, 0.6
    x, offset, heading = 0.0, initial_offset, 0.0
    history, collision = [], False
    clearance_limit = (corridor_width - robot_width) / 2
    if dt <= 0 or duration <= 0 or clearance_limit <= 0:
        raise ValueError("Time and corridor clearance must be positive")
    for step in range(math.ceil(duration / dt) + 1):
        left_distance = corridor_width / 2 - offset
        right_distance = corridor_width / 2 + offset
        # Ideal side ranges are measured normal to the corridor walls.
        error = right_distance - left_distance
        correction = kp * error + kd * heading if wall_following else 0.0
        left_command = max(0.0, min(max_speed, base_speed + correction))
        right_command = max(0.0, min(max_speed, base_speed - correction))
        history.append(dict(time=step * dt, x=x, offset=offset, heading=heading,
                            left_distance=left_distance, right_distance=right_distance,
                            left_command=left_command, right_command=right_command))
        if abs(offset) >= clearance_limit:
            collision = True
            break
        if step == math.ceil(duration / dt):
            break
        left_speed = left_command * left_gain
        right_speed = right_command * right_gain
        speed = (left_speed + right_speed) / 2
        angular_speed = (right_speed - left_speed) / wheelbase
        x += speed * math.cos(heading) * dt
        offset += speed * math.sin(heading) * dt
        heading += angular_speed * dt
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


if __name__ == '__main__':
    demo()
