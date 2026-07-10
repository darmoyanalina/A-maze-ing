*This project has been created as part of the 42 curriculum by anhambar adarmoya.*

# A-Maze-ing

## Description

**A-Maze-ing** is a Python maze generator and visualizer. From a simple text
configuration file, it builds a rectangular maze, encodes it as a grid of
hexadecimal digits (one digit per cell, one bit per wall), and writes the
result — together with the entry/exit coordinates and the shortest solving
path — to an output file.

The generator supports two modes:

- **`PERFECT=True`** — a *perfect* maze: exactly one path between the entry
  and the exit, no loops.
- **`PERFECT=False`** (default) — a *playable board*, directly usable by a
  Pac-Man-like game: fully connected, open corners and centre, at least two
  independent routes between any two points, and as few dead-ends as
  possible.

Both modes always contain a hidden **“42”** shape carved into the maze
(unless the grid is too small to fit it), and the maze can be watched live
and interacted with in the terminal: regenerate, show/hide the solution
path, and cycle through wall colours.

## Instructions

### Requirements

- Python 3.10+
- [Poetry](https://python-poetry.org/) (dependency management / build backend)
- Dependencies: `numpy`, `pydantic` (see `pyproject.toml`)

### Installation

```bash
make install
```

This installs the project dependencies through Poetry.

### Running the project

```bash
python3 a_maze_ing.py config.txt
```

or, via the Makefile:

```bash
make run
```

`config.txt` is the only argument, and can be replaced by any other
configuration file following the format described below. A default
`config.txt` is provided at the root of the repository.

### Makefile targets

| Target        | Description                                                        |
|---------------|---------------------------------------------------------------------|
| `install`     | Installs dependencies with Poetry.                                  |
| `run`         | Runs `a_maze_ing.py` on the default configuration.                   |
| `debug`       | Runs the program under `pdb`.                                       |
| `clean`       | Removes `__pycache__`, `.mypy_cache`, `.pytest_cache`.                |
| `lint`        | Runs `flake8` and `mypy` with the mandatory flags.                   |
| `lint-strict` | Runs `flake8` and `mypy --strict`.                                   |

### Interactive menu

Once a maze is generated, the following actions are available:

1. Re-generate a new maze.
2. Show / hide the shortest path between entry and exit.
3. Rotate the wall colours.
4. Quit.

## Configuration file format

The configuration file is a plain text file with one `KEY=VALUE` pair per
line. Lines starting with `#` are treated as comments and ignored.

| Key           | Description                              | Example              |
|---------------|-------------------------------------------|----------------------|
| `WIDTH`       | Maze width, in cells                       | `WIDTH=10`           |
| `HEIGHT`      | Maze height, in cells                      | `HEIGHT=10`          |
| `ENTRY`       | Entry coordinates `x,y`                    | `ENTRY=1,0`          |
| `EXIT`        | Exit coordinates `x,y`                     | `EXIT=9,9`           |
| `OUTPUT_FILE` | Path of the generated output file          | `OUTPUT_FILE=output.txt` |
| `PERFECT`     | `True` for a perfect (single-path) maze, `False` for a playable board | `PERFECT=False` |
| `SEED`        | *(optional)* integer seed for reproducibility | `SEED=2` |

Example (`config.txt`):

```
WIDTH=10
HEIGHT=10
ENTRY=1,0
EXIT=9,9
OUTPUT_FILE=output.txt
PERFECT=False
#SEED=2
```

Target Description package Builds the mazegen dist with Poetry and copies them to the repo root.

### Output file format

The maze is written using one hexadecimal digit per cell (row by row), each
bit of the digit encoding a closed wall:

| Bit (LSB → MSB) | Direction |
|---|---|
| 0 | North |
| 1 | East  |
| 2 | South |
| 3 | West  |

After an empty line, three more lines are appended: the entry coordinates,
the exit coordinates, and the shortest path from entry to exit as a string
of `N` / `E` / `S` / `W` letters.

## Maze generation algorithm

The maze is generated with a **randomized depth-first search / recursive
backtracker**, implemented iteratively with an explicit stack (rather than
recursive function calls) to avoid Python's recursion-depth limits on large
grids:

1. Start from a random unvisited cell.
2. Look at its unvisited neighbours; if there is at least one, pick one at
   random, break the wall between the two cells, push the current cell on
   the stack, and move to the neighbour.
3. If there is no unvisited neighbour, backtrack by popping the last cell
   from the stack.
4. Repeat until the stack is empty — every cell has then been visited
   exactly once, producing a **perfect maze** (a spanning tree of the grid).

When `PERFECT=False`, an extra pass (`_imperfectiate`) walks the remaining
unvisited cells and randomly removes additional walls toward the maze, in
order to open loops and turn the perfect maze into a Pac-Man-style,
fully-connected playable board.

The shortest path between entry and exit is then computed with a
**breadth-first search**, which is guaranteed to find the shortest route in
an unweighted grid such as this one.

**Why this algorithm:** the recursive backtracker was chosen because it is
simple to reason about and implement iteratively, it naturally produces
long, winding corridors with few short dead-ends (a look considered more
interesting than, e.g., Kruskal's algorithm), and — since it always visits
every cell exactly once — it guarantees a perfect maze "for free," which is
then reused as the base structure for the non-perfect / Pac-Man mode by
selectively breaking a few extra walls.

## Reusable module

The maze engine is implemented as a standalone `MazeGenerator` class (with
its companion `Config` model), independent from the terminal
menu/interaction logic in `a_maze_ing.py`, so it can be imported and reused
in another project.

Basic usage:

```python
from mazegen.amazing_class import Config, MazeGenerator

# 1. Build (and validate) the configuration
conf = Config(
    WIDTH=10,
    HEIGHT=10,
    ENTRY=(1, 0),
    EXIT=(9, 9),
    OUTPUT_FILE="maze.txt",
    PERFECT=False,
    SEED=42,        # optional, for reproducibility
)

# 2. Instantiate and generate
maze = MazeGenerator(conf)
maze.generate()

# 3. Access the generated structure
maze.maze          # numpy array of hex-digit strings, one per cell (walls)
maze.cells          # 2D grid of Cell objects (x, y, visited)

# 4. Compute and access a solution
path = maze.find_path()   # list[Cell] from entry to exit
```

Note that the structure exposed by `maze.maze` / `maze.cells` is the
in-memory representation used during generation, and is **not** necessarily
identical to the on-disk output file format described above.

This reusable module (code + this documentation) is also packaged as a
standalone, `pip`-installable distribution named `mazegen-*` (`.whl` /
`.tar.gz`), available at the root of this repository, and buildable from
source with Poetry (`poetry build`).

## Team & project management

- **Team members and roles:** <TODO — list each member and their
  responsibilities, e.g. generation algorithm, visualization, packaging,
  documentation>.
- **Planning:** <TODO — describe the initial plan and how it evolved>.
- **What worked well / what could be improved:** <TODO>.
- **Tools used:** Poetry, flake8, mypy, pytest/unittest (edit to match what
  was actually used).

## Resources

- [Maze generation algorithms — Wikipedia](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [Recursive backtracker explanation — Jamis Buck, "Buckblog"](https://weblog.jamisbuck.org/2010/12/27/maze-generation-recursive-backtracking)
- [Breadth-first search — Wikipedia](https://en.wikipedia.org/wiki/Breadth-first_search)
- [Pydantic documentation](https://docs.pydantic.dev/)
- [NumPy documentation](https://numpy.org/doc/)

**AI usage:** an AI assistant was used to <TODO — describe honestly and
precisely which parts of the project AI helped with, e.g. drafting
docstrings, explaining the recursive-backtracker algorithm, reviewing code
for flake8/mypy issues, generating this README>. All AI-assisted code was
read, tested, and understood before being kept in the final submission, and
was reviewed with peers as recommended by the subject.
