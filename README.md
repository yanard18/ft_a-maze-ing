```mermaid
flowchart TD
    Start([python3 a_maze_ing.py<br>config.txt])
    Parser{parse config.txt}
    Error1[print error & exit program]
    GridInit[initialize 2d grid & set bounds]
    Check42{can 42 pattern fit?}
    Error2[print error: grid too small]
    GenMode{check PERFECT flag}
    PerfMaze[generate perfect maze]
    PlayMaze[generate playable maze]
    Embed42[embed 42 pattern]
    Solver[run pathfinding solver]
    HexEncode[encode walls to xexadecimal]
    WriteFile[write to output_file]
    VisualRender[launch visual interface]
    Interaction{user interactions}
    ReGen[generate new maze]
    VisPath[show/hide shortest path]
    VisColor[update wall colors]
    EndNode([exit program])

    Start --> Parser
    
    Parser -->|invalid / missing| Error1
    Parser -->|valid data| GridInit
    
    GridInit --> Check42
    
    Check42 -->|no| Error2
    Check42 -->|yes| GenMode
    
    GenMode -->|PERFECT=True| PerfMaze
    GenMode -->|PERFECT=False| PlayMaze
    
    PerfMaze --> Embed42
    PlayMaze --> Embed42
    
    Embed42 --> Solver
    Solver --> HexEncode
    HexEncode --> WriteFile
    WriteFile --> Interaction
    
    Interaction --> ReGen
    ReGen --> GenMode
    
    Interaction --> VisPath
    VisPath --> VisualRender
    
    Interaction --> VisColor
    VisColor --> VisualRender
    
    Interaction --> EndNode

    class Start,EndNode startEnd;
    class Error1,Error2 errorNode;
    class GridInit,PerfMaze,PlayMaze,Embed42,Solver,HexEncode,WriteFile,VisualRender,ReGen,VisPath,VisColor processNode;
    class Parser,Check42,GenMode,Interaction decisionNode;
```


# GUIDE

"Interestingly, perfect mazes (with one unique path between any two points) are directly related to spanning trees in graph theory."

"Some famous algorithms used for maze generation, like Prim’s, Kruskal’s, or
the recursive backtracker,"

# GUIDELINES

- Python 3.10 or later
- Handle potential errors (use try-except)
- Prefer Context Managers (https://www.geeksforgeeks.org/python/context-manager-in-python)


The purpose of the A-Maze-ing project ia to create our own maze generator and display its result. Beyond just generating a maze, the project serves some of educational goals including but not limited to:
- randomness
- graph theory
- code reusability and packaging: one of the major structural purpose of the project is to teach us how to write modular code. 


# TODO

## Guidelines

- [ ] set up a virtual environment
- [ ] include a Makefile with the following rules: install, run, debug, clean, lint, lint-strict
- [ ] use pytest or unittest frameworks for test purposes 
- [ ] include .gitignore
- [ ] handle all possible exceptions


- [ ] create config.txt file thst defines the maze generation options. (means that we need a parser to parse "=", "#" etc.)


### maze
- [ ] create a standalone module containing a MazeGenerator class
- [ ] implement ranodm maze generation that supports reproducibility via a seed is provided
- [ ] ensure cells have 0 to 4 walls
- [ ] ensure entry and exit exist
- [ ] ensure enttru and exit are different
- [ ] ensure entry and exit points are inside maze bound
- [ ] no dead-end 
- [ ] two neighbor cells must share the same wall if any
- [ ] 2x3 open area at most
- [ ] 42 pattern (can be tolerated if the maze size doesn't allow -> print an error message in case)
- [ ] default mode: PERFECT=False - no/rare dead-ends, open corners, center, at least two independent loops
- [ ] PERFECT=True - ensure exactly one path between entry and exit 


### output
- [ ] encode each cell as a single hexadecimal digit representing closed walls

### documentation & packaging
- [ ] implement the maze generation as a class (MazeGenerator) for a later installation by pip
- [ ] documentatation
- [ ] add LICENSE.md for software licensing. needed 


### user interactions
- [ ] re-generate a new maze and display it
- [ ] show/hide a valif shortest path (entry -> exit)
- [ ] change maze wall colors
- [ ] set colors of 42 pattern (opt)


# DFS (Depth-First Search):
- Behavior: Selects a direction and goes as deep as possible along a branch until it hits a wall/dead-end before turning back. (backtracing)
- Data structure: stack (LIFO) or recursion
- Complexity: o(n) (since each node is visited just for once)

1. pick a starting cell and mark it as visited. (push its coordinates onto a stack)
2. check all four directions (N, E, S, W). Filter out any cells that are out of bounds, already visited or blocked (42 pattern, walls, boundaries of the maze etc.)
3. if valid unvisited neighbors exist, pick one randomly. knock down the shared wall between the current cell and the chosen neighbor.
4. step into the new cell, mark as visited and push it to the stack
5. if a cell does not have any valid unvisited neighbors, turn around. remove the current cell from the stack to track back into the previous cell and repeat the second step

algorithm visualizer: https://algorithm-visualizer.org/brute-force/depth-first-search
visualgo: https://visualgo.net/en/dfsbfs
geeksforgeeks: https://www.geeksforgeeks.org/dsa/depth-first-search-or-dfs-for-a-graph/
LeetCode:
    - Problem 200: Number of Islands
    - Problem 733: Flood Fill (exam rank 02 level 4)