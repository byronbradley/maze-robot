import unittest
from wall_following import simulate


class WallFollowingTests(unittest.TestCase):
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
