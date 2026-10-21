import unittest
from wall_following import simulate, motor_commands


class WallFollowingTests(unittest.TestCase):
    def test_invalid_readings_stop_motors(self):
        for invalid in (None, float('nan'), float('inf'), -0.01):
            self.assertEqual(motor_commands(invalid, 0.10, 0), (0, 0))
            self.assertEqual(motor_commands(0.10, invalid, 0), (0, 0))

    def test_missing_heading_stops_then_recovers(self):
        for heading in (None, float('nan'), float('inf'), -float('inf')):
            with self.subTest(heading=heading):
                self.assertEqual(motor_commands(0.15, 0.15, heading), (0, 0))
        # A lost heading sample must not prevent the next valid update.
        self.assertEqual(motor_commands(0.15, 0.15, 0.0), (0.12, 0.12))

    def test_dropout_stops_position_and_resumes(self):
        history, hit = simulate(dropout_window=(2.0, 3.0))
        dropout = [row for row in history if 2.0 <= row['time'] < 3.0]
        self.assertEqual(len(dropout), 100)
        for row in dropout:
            self.assertEqual((row['left_command'], row['right_command']), (0, 0))
            self.assertEqual((row['x'], row['offset'], row['heading']),
                             (dropout[0]['x'], dropout[0]['offset'], dropout[0]['heading']))
        resumed = next(row for row in history if row['time'] >= 3.0)
        self.assertGreater(resumed['left_command'] + resumed['right_command'], 0)
        self.assertGreater(history[-1]['x'], resumed['x'])
        self.assertFalse(hit)

    def test_feedback_reduces_drift_and_avoids_contact(self):
        uncontrolled, hit = simulate(False)
        controlled, controlled_hit = simulate(True)
        self.assertTrue(hit)
        self.assertFalse(controlled_hit)
        self.assertLess(abs(controlled[-1]['offset']), 0.005)
        self.assertLess(abs(controlled[-1]['offset']), abs(uncontrolled[-1]['offset']))

    def test_centered_balanced_robot_stays_centered(self):
        history, hit = simulate(True, left_gain=1.0, initial_offset=0.0)
        self.assertFalse(hit)
        self.assertTrue(all(row['offset'] == 0.0 for row in history))

    def test_both_drift_directions_and_command_limits(self):
        for offset in (-0.06, 0.06):
            for left_gain, right_gain in ((0.94, 1.0), (1.0, 0.94)):
                history, hit = simulate(True, initial_offset=offset,
                                        left_gain=left_gain, right_gain=right_gain)
                self.assertFalse(hit)
                self.assertLess(abs(history[-1]['offset']), 0.005)
                for row in history:
                    self.assertTrue(0 <= row['left_command'] <= 0.20)
                    self.assertTrue(0 <= row['right_command'] <= 0.20)


if __name__ == '__main__':
    unittest.main()
