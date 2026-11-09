# Maze Robot

[Try the maze simulation](https://byronbradley.me/maze-robot/web/)

A Python simulation that finds a shortest route through a known maze,
converts it into turn and forward commands, and simulates a robot
following those commands.

## Run the simulation

From the project folder, with the virtual environment activated:

```bash
python software/main.py
```

## Run maze exploration

The robot starts with an unknown map, senses nearby squares, and
backtracks to explore other branches. It then finds and follows a
route to the goal using the map it discovered.

```bash
python software/exploration.py
```

## Run the tests

```bash
python software/test_movement.py
```

