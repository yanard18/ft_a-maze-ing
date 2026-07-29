from typing import List, Set, Tuple
import random


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


    def generate_maze(self):
        self.embed_42_pattern()
        self.start_x = 0
        self.start_y = 0

        visited: Set[Tuple[int, int]] = set()
        visited.add((self.start_x, self.start_y))
        stack: List[Tuple[int, int]] = [(self.start_x, self.start_y)]

        directions = {
            'N': (0, -1, 1, 4),
            'E': (1, 0, 2, 8),
            'S': (0, 1, 4, 1),
            'W': (-1, 0, 8, 2)
        }

        while len(stack) > 0:
            curr_x, curr_y = stack[-1]
            unvisited_neighbors = []

            for (dx, dy, curr_wall, neigh_wall) in directions.values():
                neigh_x, neigh_y = curr_x + dx, curr_y + dy

                if (0 <= neigh_x and self.width > neigh_x) and (0 <= neigh_y and self.height > neigh_y):
                    if (neigh_x, neigh_y) not in visited and (neigh_x, neigh_y) not in self.blocked_cells:
                        unvisited_neighbors.append((neigh_x, neigh_y, curr_wall, neigh_wall))

            if len(unvisited_neighbors) > 0:
                neigh_x, neigh_y, curr_wall, neigh_wall = random.choice(unvisited_neighbors)

                self.grid[curr_y][curr_x] &= ~curr_wall
                self.grid[neigh_y][neigh_x] &= ~neigh_wall

                visited.add((neigh_x, neigh_y))
                stack.append((neigh_x, neigh_y))
            else:
                stack.pop()


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
                    line += "⬛️"
            print(line)

