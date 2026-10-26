from mazegen import MazeGenerator

if __name__ == "__main__":
    maze = MazeGenerator(20, 15, seed=42)
    maze.generate_maze()
    for line in maze.to_hex():
        print(line)
    print(maze.solution)
