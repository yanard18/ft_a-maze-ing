from mazegen import MazeGenerator
from output import write_output

if __name__ == "__main__":
    maze = MazeGenerator(20, 15, seed=42)
    maze.generate_maze()
    write_output("maze.txt", maze)
