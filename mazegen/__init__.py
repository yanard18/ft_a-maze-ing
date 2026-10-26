"""mazegen - a reusable random maze generator.

    from mazegen import MazeGenerator

    maze = MazeGenerator(20, 15, seed=42)
    maze.generate_maze()
    print(maze.solution)

See README.md for the full documentation.
"""

from mazegen.generator import DIRECTIONS, MazeGenerator

# names that "from mazegen import ..." gives to other files
__all__ = ["DIRECTIONS", "MazeGenerator"]
