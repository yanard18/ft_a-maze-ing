# mazegen

A small random maze generator, made as part of the 42 project A-Maze-ing.
It builds a maze on a grid, can draw a "42" in the middle with closed
cells, and gives the shortest path from the entry to the exit.

## Install

```
pip install mazegen-1.0.0-py3-none-any.whl
```

## Basic example

```python
from mazegen import MazeGenerator

maze = MazeGenerator(20, 15)
maze.generate_maze()

print(maze.solution)
```

## Custom parameters

```python
maze = MazeGenerator(
    30, 20,            # width, height (number of cells)
    entry=(0, 0),      # (x, y) of the entry
    exit=(29, 19),     # (x, y) of the exit, default is bottom-right
    perfect=False,     # False = loops and almost no dead-ends
    seed=42,           # same seed = same maze, None = random
)
maze.generate_maze()
```

Calling `generate_maze()` again gives a new maze. With a seed, the
sequence of mazes is always the same.

A `ValueError` is raised if the size, entry or exit are not valid
(outside the maze, same cell, on the "42"), or if a non-perfect maze
is asked on a grid smaller than 9x7. A perfect maze can be any size:
below 9x7 the "42" is skipped and a message is printed.

The generator uses Python's `random` module, so `seed` also sets the
global random state.

## Accessing the maze

- `maze.grid[y][x]` is the cell at column `x`, row `y`. It is an int
  where each set bit is a closed wall: `1` = North, `2` = East,
  `4` = South, `8` = West. So `15` is a fully closed cell.
- `maze.solution` is the shortest path from entry to exit, as a string
  of `N`, `E`, `S`, `W` moves.
- `maze.solve()` computes this path again from the current grid.
- `maze.blocked_cells` is the set of `(x, y)` cells drawing the "42".
- `maze.to_hex()` returns the grid as rows of hex digits, one per cell.

```python
maze = MazeGenerator(10, 10, seed=1)
maze.generate_maze()

cell = maze.grid[0][0]
if cell & 2:
    print("east wall of (0, 0) is closed")

for line in maze.to_hex():
    print(line)
```

## License

MIT, see LICENSE.md.
