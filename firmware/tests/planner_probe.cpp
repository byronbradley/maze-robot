#include <iostream>
#include "../maze_robot/Planner.h"

// One fixture: start row/column/heading, goal row/column, then 64 edge masks.
// Bits 0..3 mark known walls; bits 4..7 mark known open passages.
int main() {
  int count;
  if (!(std::cin >> count)) return 1;
  for (int caseIndex = 0; caseIndex < count; ++caseIndex) {
    Planner p;
    p.reset();
    int sr, sc, heading, gr, gc;
    std::cin >> sr >> sc >> heading >> gr >> gc;
    p.goalRow = gr; p.goalCol = gc;
    for (int r = 0; r < 8; ++r) {
      for (int c = 0; c < 8; ++c) {
        int mask;
        std::cin >> mask;
        p.row = r; p.col = c;
        for (int d = 0; d < 4; ++d) {
          if (mask & (1 << d)) p.observe(d, true);
          else if (mask & (1 << (d + 4))) p.observe(d, false);
        }
      }
    }
    p.row = sr; p.col = sc; p.heading = heading;
    std::cout << p.nextDirection() << '\n';
  }
}
