from typing import List, Set, Tuple

from mazegen import DIRECTIONS, MazeGenerator
from output import write_output


# ANSI background colours
COLORS = {
    "white": "47",
    "blue": "44",
    "yellow": "43",
    "magenta": "45",
    "gray": "100",
    "green": "42",
    "red": "41",
    "cyan": "46",
}
WALL_COLORS = ["white", "blue", "yellow", "magenta"]
PATTERN_COLORS = ["gray", "blue", "yellow", "magenta", "white"]
ENTRY_COLOR = "green"
EXIT_COLOR = "red"
PATH_COLOR = "cyan"

CLEAR_SCREEN = "\033[2J\033[H"
MENU = """
1. Re-generate a new maze
2. Show/Hide the shortest path
3. Change wall colour
4. Change 42 colour
5. Quit"""


def block(color: str) -> str:
    """Return one square of the drawing, two spaces wide."""
    if color == "":
        return "  "
    return f"\033[{COLORS[color]}m  \033[0m"


def get_path_squares(maze: MazeGenerator) -> Set[Tuple[int, int]]:
    """Return the drawing squares covered by the solution path.

    The drawing is (2 * width + 1) x (2 * height + 1) squares: the cell
    (x, y) is the square (2x + 1, 2y + 1) and walls are in between.
    """
    x, y = maze.entry
    squares = {(2 * x + 1, 2 * y + 1)}
    for letter in maze.solution:
        dx, dy, _, _ = DIRECTIONS[letter]
        squares.add((2 * x + 1 + dx, 2 * y + 1 + dy))
        x, y = x + dx, y + dy
        squares.add((2 * x + 1, 2 * y + 1))
    return squares


def is_wall(maze: MazeGenerator, sx: int, sy: int) -> bool:
    """Tell if the drawing square (sx, sy) is a closed wall."""
    if sx % 2 == 0 and sy % 2 == 0:
        return True
    x, y = sx // 2, sy // 2
    if sx % 2 == 0:
        if x < maze.width:
            return bool(maze.grid[y][x] & 8)
        return bool(maze.grid[y][x - 1] & 2)
    if y < maze.height:
        return bool(maze.grid[y][x] & 1)
    return bool(maze.grid[y - 1][x] & 4)


def render(maze: MazeGenerator, show_path: bool,
           wall_color: str, pattern_color: str) -> str:
    """Draw the whole maze as a coloured string.

    Args:
        maze: A generated maze.
        show_path: If True, the shortest path is drawn.
        wall_color: Colour name for the walls.
        pattern_color: Colour name for the 42 cells.

    Returns:
        The drawing, one line per row of squares.
    """
    path_squares = get_path_squares(maze) if show_path else set()
    lines: List[str] = []

    for sy in range(2 * maze.height + 1):
        line = ""
        for sx in range(2 * maze.width + 1):
            cell = (sx // 2, sy // 2)
            if sx % 2 == 1 and sy % 2 == 1:
                if cell == maze.entry:
                    color = ENTRY_COLOR
                elif cell == maze.exit:
                    color = EXIT_COLOR
                elif cell in maze.blocked_cells:
                    color = pattern_color
                elif (sx, sy) in path_squares:
                    color = PATH_COLOR
                else:
                    color = ""
            elif is_wall(maze, sx, sy):
                color = wall_color
            elif (sx, sy) in path_squares:
                color = PATH_COLOR
            else:
                color = ""
            line += block(color)
        lines.append(line)

    return "\n".join(lines)


def run_display(maze: MazeGenerator, output_file: str) -> None:
    """Show the maze and handle the user's choices until they quit.

    Each re-generated maze is also written to output_file.

    Args:
        maze: A generated maze.
        output_file: File where new mazes are saved.
    """
    show_path = False
    wall_index = 0
    pattern_index = 0
    message = ""

    while True:
        print(CLEAR_SCREEN, end="")
        print(render(maze, show_path, WALL_COLORS[wall_index],
                     PATTERN_COLORS[pattern_index]))
        print(f"\n{block(ENTRY_COLOR)} entry   {block(EXIT_COLOR)} exit   "
              f"{block(PATH_COLOR)} path")
        print(MENU)
        if message != "":
            print(f"\n{message}")
            message = ""

        try:
            choice = input("\nChoice (1-5): ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return

        if choice == "1":
            maze.generate_maze()
            try:
                write_output(output_file, maze)
            except OSError as e:
                message = f"Error: can't write {output_file}: {e.strerror}"
        elif choice == "2":
            show_path = not show_path
        elif choice == "3":
            wall_index = (wall_index + 1) % len(WALL_COLORS)
        elif choice == "4":
            pattern_index = (pattern_index + 1) % len(PATTERN_COLORS)
        elif choice == "5":
            return
        else:
            message = f"Unknown choice '{choice}', type a number from 1 to 5"
