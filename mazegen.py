from typing import List


class MazeGenerator:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height

        self.grid: List[List[int]] = []

        for _ in range(height):
            row: List[int] = []
            for _ in range(width):
                row.append(15)
            self.grid.append(row)

    def print_hex_grid(self) -> None:
        for row in self.grid:
            for cell in row:
                print(cell, end=" ")
            print()
