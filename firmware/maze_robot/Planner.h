#pragma once
#include <stdint.h>

// North, east, south, west. Unknown interior passages are open for planning.
class Planner {
 public:
  static constexpr uint8_t SIZE = 8;
  static constexpr uint16_t INF = 0xffff;
  int8_t row = 7, col = 0;
  uint8_t heading = 0;
  uint8_t goalRow = 0, goalCol = 7;

  void reset() {
    row = 7; col = 0; heading = 0;
    for (uint8_t r = 0; r < SIZE; ++r)
      for (uint8_t c = 0; c < SIZE; ++c) {
        known[r][c] = walls[r][c] = 0;
      }
    for (uint8_t r = 0; r < SIZE; ++r)
      for (uint8_t c = 0; c < SIZE; ++c)
        for (uint8_t d = 0; d < 4; ++d)
          if (!inside(r + dr(d), c + dc(d))) record(r, c, d, true);
  }

  static int8_t dr(uint8_t d) { return d == 0 ? -1 : d == 2 ? 1 : 0; }
  static int8_t dc(uint8_t d) { return d == 1 ? 1 : d == 3 ? -1 : 0; }
  static bool inside(int r, int c) { return r >= 0 && c >= 0 && r < SIZE && c < SIZE; }
  bool atGoal() const { return row == goalRow && col == goalCol; }

  void observe(uint8_t direction, bool wall) { record(row, col, direction, wall); }
  bool blocked(int r, int c, uint8_t d) const {
    return !inside(r + dr(d), c + dc(d)) || (walls[r][c] & (1u << d));
  }
  bool confirmedOpen(uint8_t d) const {
    return (known[row][col] & (1u << d)) && !blocked(row, col, d);
  }

  int nextDirection() {
    uint8_t queue[SIZE * SIZE];
    uint8_t head = 0, tail = 0;
    for (uint8_t r = 0; r < SIZE; ++r)
      for (uint8_t c = 0; c < SIZE; ++c) distance[r][c] = INF;
    distance[goalRow][goalCol] = 0;
    queue[tail++] = goalRow * SIZE + goalCol;
    while (head < tail) {
      uint8_t cell = queue[head++], r = cell / SIZE, c = cell % SIZE;
      for (uint8_t d = 0; d < 4; ++d) {
        int nr = r + dr(d), nc = c + dc(d);
        if (!blocked(r, c, d) && distance[nr][nc] == INF) {
          distance[nr][nc] = distance[r][c] + 1;
          queue[tail++] = nr * SIZE + nc;
        }
      }
    }
    if (distance[row][col] == INF || atGoal()) return -1;
    // Match Python: straight first, then north/east/south/west.
    for (uint8_t i = 0; i < 5; ++i) {
      uint8_t d = i == 0 ? heading : i - 1;
      if (!blocked(row, col, d) &&
          distance[row + dr(d)][col + dc(d)] < distance[row][col]) return d;
    }
    return -1;
  }

  void arrived() { row += dr(heading); col += dc(heading); }

 private:
  uint8_t known[SIZE][SIZE] = {}, walls[SIZE][SIZE] = {};
  uint16_t distance[SIZE][SIZE] = {};
  void record(int r, int c, uint8_t d, bool wall) {
    if (!inside(r, c)) return;
    setEdge(r, c, d, wall);
    int nr = r + dr(d), nc = c + dc(d);
    if (inside(nr, nc)) setEdge(nr, nc, (d + 2) % 4, wall);
  }
  void setEdge(int r, int c, uint8_t d, bool wall) {
    known[r][c] |= 1u << d;
    if (wall) walls[r][c] |= 1u << d;
    else walls[r][c] &= ~(1u << d);
  }
};
