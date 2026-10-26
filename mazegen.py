from collections import deque
from typing import Dict, List, Optional, Set, Tuple
import random


Cell = Tuple[int, int]

# letter: (dx, dy, wall of the current cell, wall of the neighbour)
DIRECTIONS = {
    'N': (0, -1, 1, 4),
    'E': (1, 0, 2, 8),
    'S': (0, 1, 4, 1),
    'W': (-1, 0, 8, 2)
}

# cells of the "42" drawing, as (dx, dy) from its top-left corner
PATTERN_42 = [
    (0, 0), (0, 1), (0, 2),
    (1, 2), (2, 0), (2, 1),
    (2, 2), (2, 3), (2, 4),
    (4, 0), (5, 0), (6, 0),
    (6, 1), (4, 2), (5, 2),
    (6, 2), (4, 3), (4, 4),
    (5, 4), (6, 4)
]
PATTERN_WIDTH = 7
PATTERN_HEIGHT = 5


class MazeGenerator:
    """Random maze generator.

    The maze is a grid of ints, one per cell, where each set bit is a
    closed wall: 1 = North, 2 = East, 4 = South, 8 = West.
    grid[y][x] is the cell at column x, row y.

    Example:
        maze = MazeGenerator(20, 15, entry=(0, 0), exit=(19, 14), seed=42)
        maze.generate_maze()
        print(maze.grid[0][0], maze.solution)
    """

    def __init__(self, width: int, height: int,
                 entry: Cell = (0, 0),
                 exit: Optional[Cell] = None,
                 perfect: bool = True,
                 seed: Optional[int] = None) -> None:
        """Set up an empty maze.

        Args:
            width: Number of columns.
            height: Number of rows.
            entry: Entry cell as (x, y).
            exit: Exit cell as (x, y). Defaults to the bottom-right cell.
            perfect: True for a single path between entry and exit,
                False for a maze with loops and almost no dead-ends.
            seed: Seed for the random generator, None for a random one.

        Raises:
            ValueError: If the size, entry or exit are not valid.
        """
        if width < 1 or height < 1:
            raise ValueError("width and height must be at least 1")
        if exit is None:
            exit = (width - 1, height - 1)

        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.perfect = perfect
        self.rng = random.Random(seed)

        self.grid: List[List[int]] = []
        self.blocked_cells: Set[Cell] = set()
        self.solution = ""

        for name, (x, y) in (("entry", entry), ("exit", exit)):
            if not self.in_bounds(x, y):
                raise ValueError(f"{name} {x},{y} is outside the maze")
        if entry == exit:
            raise ValueError("entry and exit must be different")

        self.embed_42_pattern()
        for name, cell in (("entry", entry), ("exit", exit)):
            if cell in self.blocked_cells:
                raise ValueError(f"{name} {cell[0]},{cell[1]} is on the "
                                 f"42 pattern")

    def in_bounds(self, x: int, y: int) -> bool:
        """Tell if (x, y) is inside the maze."""
        return 0 <= x < self.width and 0 <= y < self.height

    def is_free(self, x: int, y: int) -> bool:
        """Tell if (x, y) is inside the maze and not part of the 42."""
        return self.in_bounds(x, y) and (x, y) not in self.blocked_cells

    def embed_42_pattern(self) -> None:
        """Mark the cells of the centred "42" as blocked.

        The pattern needs a free cell all around it, otherwise it could
        cut the maze in parts. If the maze is too small, an error is
        printed and the maze is made without it.
        """
        if (self.width < PATTERN_WIDTH + 2
                or self.height < PATTERN_HEIGHT + 2):
            print("Error: maze is too small to draw the 42 pattern, "
                  "generating it without")
            return

        start_x = (self.width - PATTERN_WIDTH) // 2
        start_y = (self.height - PATTERN_HEIGHT) // 2
        for dx, dy in PATTERN_42:
            self.blocked_cells.add((start_x + dx, start_y + dy))

    def generate_maze(self) -> None:
        """Generate a new maze and its solution.

        Calling it again gives a different maze, but the sequence of
        mazes is the same for a given seed.

        Raises:
            ValueError: If a non-perfect maze can't fit in this size.
        """
        self.grid = []
        for _ in range(self.height):
            row: List[int] = []
            for _ in range(self.width):
                row.append(15)
            self.grid.append(row)

        self.carve_paths()
        if not self.perfect:
            self.remove_dead_ends()
            self.add_loops(2)
        self.solution = self.solve()

    def carve_paths(self) -> None:
        """Carve a perfect maze with a randomized DFS from the entry."""
        start = self.entry
        visited: Set[Cell] = {start}
        stack: List[Cell] = [start]

        while len(stack) > 0:
            curr_x, curr_y = stack[-1]
            unvisited_neighbors = []

            for (dx, dy, curr_wall, neigh_wall) in DIRECTIONS.values():
                neigh_x, neigh_y = curr_x + dx, curr_y + dy
                if (self.is_free(neigh_x, neigh_y)
                        and (neigh_x, neigh_y) not in visited):
                    unvisited_neighbors.append(
                        (neigh_x, neigh_y, curr_wall, neigh_wall))

            if len(unvisited_neighbors) > 0:
                neigh_x, neigh_y, curr_wall, neigh_wall = self.rng.choice(
                    unvisited_neighbors)

                self.grid[curr_y][curr_x] &= ~curr_wall
                self.grid[neigh_y][neigh_x] &= ~neigh_wall

                visited.add((neigh_x, neigh_y))
                stack.append((neigh_x, neigh_y))
            else:
                stack.pop()

    def remove_dead_ends(self) -> None:
        """Open one more wall in each dead-end, where possible.

        A wall is not opened if it would make a 3x3 open area.
        """
        cells = []
        for y in range(self.height):
            for x in range(self.width):
                if self.is_free(x, y):
                    cells.append((x, y))
        self.rng.shuffle(cells)

        for x, y in cells:
            if self.count_open_walls(x, y) != 1:
                continue
            letters = list(DIRECTIONS.keys())
            self.rng.shuffle(letters)
            for letter in letters:
                if self.open_wall(x, y, letter):
                    break

    def add_loops(self, min_loops: int) -> None:
        """Open random walls until the maze has at least min_loops loops.

        Raises:
            ValueError: If the maze is too small to get enough loops.
        """
        loops = self.count_loops()
        if loops >= min_loops:
            return

        walls = []
        for y in range(self.height):
            for x in range(self.width):
                if self.is_free(x, y):
                    walls.append((x, y, 'E'))
                    walls.append((x, y, 'S'))
        self.rng.shuffle(walls)

        for x, y, letter in walls:
            if self.open_wall(x, y, letter):
                loops += 1
                if loops >= min_loops:
                    return
        raise ValueError("maze is too small to be non-perfect, "
                         "try a bigger size or PERFECT=True")

    def open_wall(self, x: int, y: int, letter: str) -> bool:
        """Open the wall of (x, y) in the given direction.

        The wall stays closed if it is already open, if it is on the
        border or the 42, or if opening it makes a 3x3 open area.

        Returns:
            True if the wall was opened.
        """
        dx, dy, curr_wall, neigh_wall = DIRECTIONS[letter]
        neigh_x, neigh_y = x + dx, y + dy
        if not self.is_free(neigh_x, neigh_y):
            return False
        if not self.grid[y][x] & curr_wall:
            return False

        self.grid[y][x] &= ~curr_wall
        self.grid[neigh_y][neigh_x] &= ~neigh_wall

        if self.has_open_area(x, y):
            self.grid[y][x] |= curr_wall
            self.grid[neigh_y][neigh_x] |= neigh_wall
            return False
        return True

    def has_open_area(self, x: int, y: int) -> bool:
        """Tell if (x, y) is part of a 3x3 area with no walls inside."""
        for top in range(y - 2, y + 1):
            for left in range(x - 2, x + 1):
                if self.is_open_area(left, top):
                    return True
        return False

    def is_open_area(self, left: int, top: int) -> bool:
        """Tell if the 3x3 square starting at (left, top) is all open."""
        if not (self.in_bounds(left, top)
                and self.in_bounds(left + 2, top + 2)):
            return False
        for y in range(top, top + 3):
            for x in range(left, left + 3):
                if x < left + 2 and self.grid[y][x] & 2:
                    return False
                if y < top + 2 and self.grid[y][x] & 4:
                    return False
        return True

    def count_open_walls(self, x: int, y: int) -> int:
        """Count the open sides of the cell (x, y)."""
        count = 0
        for (_, _, wall, _) in DIRECTIONS.values():
            if not self.grid[y][x] & wall:
                count += 1
        return count

    def count_loops(self) -> int:
        """Count the independent loops: passages - cells + 1."""
        cells = 0
        passages = 0
        for y in range(self.height):
            for x in range(self.width):
                if not self.is_free(x, y):
                    continue
                cells += 1
                if not self.grid[y][x] & 2:
                    passages += 1
                if not self.grid[y][x] & 4:
                    passages += 1
        return passages - cells + 1

    def solve(self) -> str:
        """Find the shortest path from entry to exit with a BFS.

        Returns:
            The path as a string of 'N', 'E', 'S', 'W' moves,
            or an empty string if the exit can't be reached.
        """
        parent: Dict[Cell, Cell] = {}
        move: Dict[Cell, str] = {}
        visited: Set[Cell] = {self.entry}
        queue = deque([self.entry])

        while len(queue) > 0:
            curr_x, curr_y = queue.popleft()
            if (curr_x, curr_y) == self.exit:
                break
            for letter, (dx, dy, wall, _) in DIRECTIONS.items():
                if self.grid[curr_y][curr_x] & wall:
                    continue
                neigh = (curr_x + dx, curr_y + dy)
                if neigh not in visited:
                    visited.add(neigh)
                    parent[neigh] = (curr_x, curr_y)
                    move[neigh] = letter
                    queue.append(neigh)

        if self.exit not in visited:
            return ""
        path = []
        cell = self.exit
        while cell != self.entry:
            path.append(move[cell])
            cell = parent[cell]
        path.reverse()
        return "".join(path)

    def to_hex(self) -> List[str]:
        """Return the maze as rows of hex digits, one digit per cell."""
        lines = []
        for row in self.grid:
            line = ""
            for cell in row:
                line += format(cell, 'X')
            lines.append(line)
        return lines
