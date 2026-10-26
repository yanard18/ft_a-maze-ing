import sys

from display import run_display
from mazegen import MazeGenerator
from output import write_output
from parser import ConfigError, parse_config


def main() -> int:
    """Read the config, generate the maze, save it and show it.

    Returns:
        0 on success, 1 on any error.
    """
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        return 1

    try:
        config = parse_config(sys.argv[1])
    except ConfigError as e:
        print(f"Error: {e}")
        return 1

    try:
        maze = MazeGenerator(config.width, config.height,
                             entry=config.entry,
                             exit=config.exit,
                             perfect=config.perfect,
                             seed=config.seed)
        maze.generate_maze()
    except ValueError as e:
        print(f"Error: {e}")
        return 1

    try:
        write_output(config.output_file, maze)
    except OSError as e:
        print(f"Error: can't write {config.output_file}: {e.strerror}")
        return 1

    run_display(maze, config.output_file)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print()
        sys.exit(1)
