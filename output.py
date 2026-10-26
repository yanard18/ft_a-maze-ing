from mazegen import MazeGenerator


def write_output(filepath: str, maze: MazeGenerator) -> None:
    """Write the maze to a file in the subject's format.

    The file has one row of hex digits per maze row, an empty line,
    then the entry "x,y", the exit "x,y" and the shortest path.
    Every line ends with '\\n', also on Windows.

    Args:
        filepath: Path of the output file.
        maze: A maze where generate_maze() was already called.

    Raises:
        OSError: If the file can't be written.
    """
    entry_x, entry_y = maze.entry
    exit_x, exit_y = maze.exit

    with open(filepath, 'w', encoding='utf-8', newline='\n') as f:
        for line in maze.to_hex():
            f.write(line + "\n")
        f.write("\n")
        f.write(f"{entry_x},{entry_y}\n")
        f.write(f"{exit_x},{exit_y}\n")
        f.write(maze.solution + "\n")
