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

## Run the tests

```bash
python software/test_movement.py
```

## Run the browser simulation

Open `web/index.html` in a browser. No server or installation is needed.
The webpage uses a JavaScript version of the maze solver.
