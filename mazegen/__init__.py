"""mazegen - a reusable random maze generator.

Basic usage:

    from mazegen import MazeGenerator

    maze = MazeGenerator(20, 15, entry=(0, 0), exit=(19, 14),
                         perfect=True, seed=42)
    maze.generate_maze()
    print(maze.grid)       # list of rows, one int per cell (wall bits)
    print(maze.solution)   # shortest path, e.g. "EESSWS..."

See README.md for the full documentation.
"""

from mazegen.generator import DIRECTIONS, MazeGenerator

__all__ = ["DIRECTIONS", "MazeGenerator"]
__version__ = "1.0.0"
