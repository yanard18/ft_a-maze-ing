from typing import List, Set, Tuple


class MazeGenerator:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height

        self.grid: List[List[int]] = []
        self.blocked_cells: Set[Tuple[int, int]] = set()

        for _ in range(height):
            row: List[int] = []
            for _ in range(width):
                row.append(15)
            self.grid.append(row)

    def embed_42_pattern(self) -> None:
        start_x = round((self.width - 7) / 2)
        start_y = round((self.height - 5) / 2)

        pattern = [
            (0, 0), (0, 1), (0, 2),
            (1, 2), (2, 0), (2, 1),
            (2, 2), (2, 3), (2, 4),
            (4, 0), (5, 0), (6, 0),
            (6, 1), (4, 2), (5, 2),
            (6, 2), (4, 3), (4, 4),
            (5, 4), (6, 4)
        ]

        for dx, dy in pattern:
            self.blocked_cells.add((start_x + dx, start_y + dy))


    def print_hex_maze(self) -> None:
        for y in range(self.height):
            line = ""
            for x in range(self.width):
                cell = self.grid[y][x]

                if (x, y) in self.blocked_cells:
                    line += "🟥"
                elif cell == 15:
                    line += "⬜️"
                else:
                    line += " "
            print(line)

