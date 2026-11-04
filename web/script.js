let maze = [
    [0, 0, 1, 0, 0],
    [1, 0, 1, 0, 1],
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 1, 0]
];

let path = [];
let step = 0;
let timer = null;

const mazeElement = document.getElementById("maze");
const statusElement = document.getElementById("status");
const stepButton = document.getElementById("step-button");
const playButton = document.getElementById("play-button");
const resetButton = document.getElementById("reset-button");
const randomButton = document.getElementById("random-button");

function findPath() {
    const queue = [[[0, 0]]];
    const visited = new Set(["0,0"]);

    while (queue.length > 0) {
        const route = queue.shift();
        const [row, column] = route[route.length - 1];
        if (row === 4 && column === 4) return route;

        const neighbors = [
            [row, column + 1], [row, column - 1],
            [row + 1, column], [row - 1, column]
        ];

        for (const [r, c] of neighbors) {
            const key = `${r},${c}`;
            if (r < 0 || r >= 5 || c < 0 || c >= 5) continue;
            if (maze[r][c] === 1 || visited.has(key)) continue;
            visited.add(key);
            queue.push([...route, [r, c]]);
        }
    }
    return [];
}

function drawMaze() {
    const [robotRow, robotColumn] = path[step] || [0, 0];
    mazeElement.innerHTML = "";
    mazeElement.style.gridTemplateColumns = "repeat(5, 40px)";

    for (let row = 0; row < 5; row++) {
        for (let column = 0; column < 5; column++) {
            const square = document.createElement("div");
            square.classList.add("cell");
            if (maze[row][column] === 1) square.classList.add("wall");
            if (row === 4 && column === 4) square.classList.add("goal");
            if (row === robotRow && column === robotColumn) {
                square.classList.add("robot");
            }
            mazeElement.appendChild(square);
        }
    }
}

function stopPlaying() {
    clearInterval(timer);
    timer = null;
    playButton.textContent = "Play";
}

function takeStep() {
    if (path.length === 0) return;
    if (step < path.length - 1) step++;
    drawMaze();
    statusElement.textContent = `Move ${step} of ${path.length - 1}`;

    if (step === path.length - 1) {
        stopPlaying();
        statusElement.textContent = `Goal reached in ${step} moves.`;
    }
}

function resetRobot() {
    stopPlaying();
    step = 0;
    path = findPath();
    drawMaze();
    statusElement.textContent = path.length
        ? "Ready"
        : "No route to the goal.";
}

function makeRandomMaze() {
    stopPlaying();
    const previousMaze = maze;

    for (let attempt = 0; attempt < 100; attempt++) {
        maze = [];
        for (let row = 0; row < 5; row++) {
            const cells = [];
            for (let column = 0; column < 5; column++) {
                cells.push(Math.random() < 0.3 ? 1 : 0);
            }
            maze.push(cells);
        }
        maze[0][0] = 0;
        maze[4][4] = 0;
        if (findPath().length > 0) {
            resetRobot();
            return;
        }
    }
    maze = previousMaze;
    statusElement.textContent = "Could not generate a maze. Try again.";
}

stepButton.onclick = function () {
    stopPlaying();
    takeStep();
};

playButton.onclick = function () {
    if (timer !== null) {
        stopPlaying();
    } else if (path.length > 0 && step < path.length - 1) {
        playButton.textContent = "Pause";
        timer = setInterval(takeStep, 350);
    }
};

resetButton.onclick = resetRobot;
randomButton.onclick = makeRandomMaze;
resetRobot();
