from mazegen import MazeGenerator

if __name__ == "__main__":
    maze = MazeGenerator(10, 10)
    maze.print_hex_maze()
    maze.embed_42_pattern()
    print()
    maze.print_hex_maze()