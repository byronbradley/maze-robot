#include <cassert>
#include "../maze_robot/Planner.h"

int main() {
  Planner p;
  p.reset();
  assert(p.row == 7 && p.col == 0 && p.heading == 0);
  assert(p.blocked(7, 0, 2) && p.blocked(7, 0, 3));
  assert(!p.confirmedOpen(0));
  assert(p.nextDirection() == 0);
  p.observe(0, false);
  assert(p.confirmedOpen(0));
  p.observe(0, true);
  assert(p.blocked(6, 0, 2));  // reciprocal wall
  p.observe(1, true);
  assert(p.nextDirection() == -1);  // enclosed start
  p.reset();
  assert(!p.blocked(7, 0, 0));
  // Entire open grid: observe every candidate, then reach the supplied goal.
  int moves = 0;
  while (!p.atGoal() && moves < 64) {
    for (uint8_t d = 0; d < 4; ++d)
      p.observe(d, !Planner::inside(p.row + Planner::dr(d), p.col + Planner::dc(d)));
    int direction = p.nextDirection();
    assert(direction >= 0 && p.confirmedOpen(direction));
    p.heading = direction;
    p.arrived();
    ++moves;
  }
  assert(p.atGoal() && moves == 14);
  assert(p.nextDirection() == -1);
}
