*This project has been created as part of the 42 curriculum by ynascime, luccaval.*

# A-Maze-ing

## Description

A-Maze-ing is a Python maze generator. Given a small configuration file, it
builds a grid maze cell by cell, guarantees it is solvable, and writes it to
an output file using a compact hexadecimal wall encoding.

Two generation modes are supported, chosen with the `PERFECT` key:

- **`PERFECT=True`** — a perfect maze: exactly one path between the entry
  and the exit, no loops at all. This is the classic "academic" maze.
- **`PERFECT=False`** (default) — a *playable board*, built on top of the
  same perfect maze but with extra walls knocked down afterwards so it is
  usable as a Pac-Man-like board: every corridor stays reachable, the four
  corners and the centre are open, there are at least two independent
  routes between them, and dead-ends are kept rare.

Every maze also hides a visible **"42"** pattern: a block of cells left
completely walled off (isolated) in the middle of the grid, the one
exception the subject allows to "no isolated cells."

The maze can be watched live in the terminal, in colour, with an
interactive menu to regenerate it, toggle the solution path, and cycle
wall colours. The generation logic itself lives in a separate, reusable,
pip-installable package (`mazegen`) so it can be dropped into a future
project (e.g. an actual Pac-Man game) without dragging along the CLI,
config parsing, or rendering code.

## Instructions

### Requirements

- Python 3.10+
- A terminal that supports ANSI 256-colour escape codes (most modern
  terminals do).

### Running the generator

```bash
make install   # installs the 'build' tool, used for packaging mazegen
make run       # equivalent to: python3 a_maze_ing.py config.txt
```

Or directly:

```bash
python3 a_maze_ing.py config.txt
```

`a_maze_ing.py` is the entry point and `config.txt` is the only argument:
a plain text configuration file (a different filename can be passed
instead).

Once launched, the maze is generated, solved, and written to the file
named by `OUTPUT_FILE`. The terminal then switches to an interactive menu:

```
=== A-Maze-ing ===
1. Re-generate a new maze
2. Show / Hide the shortest path
3. Rotate the wall colours
4. Quit
```

### Other Makefile targets

| Target        | Purpose                                                |
|---------------|---------------------------------------------------------|
| `make install`| Install the tooling needed to build the `mazegen` package. |
| `make run`    | Run `a_maze_ing.py` against `config.txt`.               |
| `make debug`  | Run the program under Python's `pdb` debugger.          |
| `make lint`   | Run `flake8` and `mypy --strict` over the project.      |
| `make build`  | Rebuild `mazegen-*.whl` from the `mazegen/` sources.    |
| `make clean`  | Remove caches, build artifacts, and the generated maze output. |

### Checking an output file

The subject-provided `maze_analyzer.py` can independently verify an
output file: it checks that every shared wall is encoded consistently by
both neighbouring cells, and reports whether the maze is perfect or a
valid playable board.

```bash
python3 maze_analyzer.py maze.txt
python3 maze_analyzer.py maze.txt --max-dead-ends 0   # check the no-dead-end bonus
```

### Using the reusable `mazegen` package

The maze generation logic lives entirely in `mazegen/generator.py`,
exposed as the `MazeGenerator` class, and is packaged separately from
the rest of the project so another project can install and import it
without pulling in the config parser, output writer, or terminal
renderer.

**Basic example:**

```python
from mazegen import MazeGenerator

maze = MazeGenerator(width=20, height=15, perfect=False, seed=42)

# The generated structure: one bitmask per cell (bit 0=N, 1=E, 2=S, 3=W;
# a set bit means that wall is closed). Not the same format as the
# output file written by output.py.
grid = maze.get_grid()

# At least one solution, as a list of "N"/"E"/"S"/"W" moves.
solution = maze.solve(start_x=0, start_y=0, end_x=19, end_y=14)
```

**Custom parameters:**

- `width`, `height` — maze dimensions, in cells.
- `perfect` — `True` for a single-path maze, `False` (default) for a
  playable board with loops.
- `seed` — optional `int`. Passing the same seed reproduces the exact
  same maze; omitting it (or passing `None`) generates a new random one.

**Building the package from source:**

```bash
python3 -m pip install build
python3 -m build --wheel --outdir .
```

This produces `mazegen-<version>-py3-none-any.whl` at the repository
root, ready to be installed elsewhere with
`pip install mazegen-<version>-py3-none-any.whl`. The reuse terms are
in [`LICENSE.md`](./LICENSE.md).

## Configuration file format

One `KEY=VALUE` pair per line. Lines starting with `#` are ignored.

| Key           | Required | Description                              | Example              |
|---------------|----------|-------------------------------------------|-----------------------|
| `WIDTH`       | yes      | Maze width, in cells                      | `WIDTH=20`            |
| `HEIGHT`      | yes      | Maze height, in cells                     | `HEIGHT=15`           |
| `ENTRY`       | yes      | Entry coordinates, `x,y`                  | `ENTRY=0,0`           |
| `EXIT`        | yes      | Exit coordinates, `x,y`                   | `EXIT=19,14`          |
| `OUTPUT_FILE` | yes      | Path of the file the maze is written to   | `OUTPUT_FILE=maze.txt`|
| `PERFECT`     | yes      | `True` for a single-path maze, `False` for a playable board | `PERFECT=False` |
| `SEED`        | no       | Integer seed for reproducible generation  | `SEED=42`             |

`WIDTH`/`HEIGHT` must be positive integers; `ENTRY`/`EXIT` must be
distinct and inside the grid. Any violation is reported with a clear
error message instead of crashing.

A default configuration file is provided at [`config.txt`](./config.txt).

## Maze generation algorithm

The base maze is carved with a **recursive backtracker** (iterative
depth-first search with an explicit stack): starting from `(0, 0)`, at
each step a random unvisited neighbour is picked, the wall between the
two cells is knocked down, and the walk continues, backtracking when a
cell has no unvisited neighbour left. Cells belonging to the "42" pattern
are pre-marked as visited before the walk starts, so the walk never
enters them and they stay fully walled off.

This produces a **perfect maze** by construction (a spanning tree over
the grid graph — connected, with no cycles). If `PERFECT=True`, that
maze is the final result.

If `PERFECT=False`, a second pass (`_make_playable_board`) turns that
perfect maze into a Pac-Man-style board: any true dead-end (a cell
closed on three sides) has one of its remaining walls knocked down, and
the four corners plus the centre cell have walls removed until each is
an open through-cell, which introduces the loops a chased player needs.

**Why this algorithm:** the recursive backtracker was chosen because it
naturally guarantees full connectivity and coherent, one-shared-wall-
per-pair data without any extra bookkeeping, its long, winding corridors
match the "42" pattern requirement (a perfect maze that never touches a
few pre-blocked cells), and adding loops afterwards is far simpler than
generating loops directly, since it only means selectively removing
walls from an already-guaranteed-connected result rather than
constructing connectivity and cycles at the same time.

## Output file format

One hexadecimal digit per cell (row by row), where each bit marks a
*closed* wall: bit 0 = North, bit 1 = East, bit 2 = South, bit 3 = West.
After a blank line: the entry coordinates, the exit coordinates, and the
shortest path from entry to exit as a string of `N`/`E`/`S`/`W` letters.

## What is reusable, and how

Only `mazegen/` (the `MazeGenerator` class and its `__init__.py`) is
built into the standalone `mazegen` package — the part meant to outlive
this project. Everything else (`a_maze_ing.py`, `parse_config.py`,
`output.py`, `visualizer.py`, `menu.py`) is this project's own CLI:
config parsing, the hex output writer, and the interactive terminal
renderer, none of which a future project would need if it just wants a
maze to build on top of.

## Team and project management

- **Roles:** luccaval worked on the maze generation core (`mazegen`,
  the recursive backtracker, the playable-board pass, and the BFS
  solver); ynascime worked on the output file writer and the packaging/licensing
  setup and the config parser. The interactive terminal
  menu and coloured visualizer were built together, iterating from a
  plain `+---+` ASCII rendering to the current block-style coloured
  one.
- **Planning:** we started from the mandatory part end to end
  (config → generation → output file) before touching the visual, so
  we always had something the `maze_analyzer.py` could check
  first. The interactive menu and the colour rendering were added once
  the generator itself was validated, and packaging/licensing was
  handled last.
- **What worked well:** separating maze generation from
  everything else early on made the `mazegen` package trivial to
  extract afterwards, no rewrites needed.
- **What could be improved:** the loop/dead-end guarantees for the
  non-perfect board are enforced with targeted wall-breaking rather
  than a formal loop count, so `maze_analyzer.py` was used repeatedly
  during development to catch cases that didn't meet the minimum.
- **Tools used:** `flake8` and `mypy --strict` (via `make lint`),
  `python -m build` for packaging, and `maze_analyzer.py` for
  validating output files.

## Resources

- [Recursive backtracker maze algorithm — Wikipedia, "Maze generation algorithm"](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [Wall Follower & spanning-tree relationship for perfect mazes](https://en.wikipedia.org/wiki/Spanning_tree)
- [Python `typing` module documentation](https://docs.python.org/3/library/typing.html)
- [Packaging Python Projects — Python Packaging User Guide](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
- [ANSI escape codes (256-colour terminal backgrounds)](https://en.wikipedia.org/wiki/ANSI_escape_code)

### AI Usage

AI (Claude by Anthropic) was used during this project in the following ways:

- **Algorithm conceptualisation** — Asking conceptual questions about how algorithms works — without asking for direct code.
- **No source code was generated by AI.** All `.py` files were written manually to comply with flake8, type hints and meet the pedagogical intent of the project.
