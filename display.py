from typing import Set, Tuple

from mazegen import DIRECTIONS, MazeGenerator
from output import write_output


# ANSI colour codes: text colours for walls, background colours for cells
WALL_COLORS = ["37", "34", "33", "35"]          # white, blue, yellow, magenta
PATTERN_COLORS = ["100", "44", "43", "45"]      # gray, blue, yellow, magenta
ENTRY_COLOR = "42"                              # green
EXIT_COLOR = "41"                               # red
PATH_COLOR = "46"                               # cyan

MENU = """
1. Re-generate a new maze
2. Show/Hide the shortest path
3. Change wall colour
4. Change 42 colour
5. Quit"""


def paint(text: str, color: str) -> str:
    """Return text with an ANSI colour."""
    return "\033[" + color + "m" + text + "\033[0m"


def get_path_cells(maze: MazeGenerator) -> Set[Tuple[int, int]]:
    """Return the cells visited by the solution, entry included."""
    x, y = maze.entry
    cells = set()
    cells.add((x, y))
    for letter in maze.solution:
        dx, dy, wall, neigh_wall = DIRECTIONS[letter]
        x += dx
        y += dy
        cells.add((x, y))
    return cells


def draw_cell(maze: MazeGenerator, x: int, y: int,
              path_cells: Set[Tuple[int, int]], pattern_color: str) -> str:
    """Return the inside of one cell, 3 characters wide."""
    if (x, y) == maze.entry:
        return paint("   ", ENTRY_COLOR)
    if (x, y) == maze.exit:
        return paint("   ", EXIT_COLOR)
    if (x, y) in maze.blocked_cells:
        return paint("   ", pattern_color)
    if (x, y) in path_cells:
        return paint("   ", PATH_COLOR)
    return "   "


def render(maze: MazeGenerator, show_path: bool,
           wall_color: str, pattern_color: str) -> str:
    """Draw the maze as text, two lines for each row of cells.

    The first line has the north walls (+---+), the second one the west
    walls (|) and the cells. The east and south borders are added at
    the end of each line and after the last row.
    """
    path_cells: Set[Tuple[int, int]] = set()
    if show_path:
        path_cells = get_path_cells(maze)

    lines = []
    for y in range(maze.height):
        top = ""
        middle = ""
        for x in range(maze.width):
            cell = maze.grid[y][x]
            top += paint("+", wall_color)
            if cell & 1:
                top += paint("---", wall_color)
            else:
                top += "   "
            if cell & 8:
                middle += paint("|", wall_color)
            else:
                middle += " "
            middle += draw_cell(maze, x, y, path_cells, pattern_color)
        top += paint("+", wall_color)
        middle += paint("|", wall_color)
        lines.append(top)
        lines.append(middle)

    bottom = ""
    for x in range(maze.width):
        bottom += paint("+---", wall_color)
    bottom += paint("+", wall_color)
    lines.append(bottom)

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
        print(render(maze, show_path, WALL_COLORS[wall_index],
                     PATTERN_COLORS[pattern_index]))
        print(MENU)
        if message != "":
            print("\n" + message)
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

        # clear the screen before drawing again. Not done before the first
        # drawing, so messages printed before (like the 42 error) stay
        print("\033[2J\033[H", end="")
