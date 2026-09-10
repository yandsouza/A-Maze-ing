from __future__ import annotations
from mazegen import MazeGenerator

RESET = "\033[0m"

WALL_COLOR_PALETTES: list[tuple[str, str]] = [
    ("232", "252"),
    ("52", "223"),
    ("22", "194"),
    ("17", "159"),
]

ENTRY_COLOR = "201"
EXIT_COLOR = "196"
PATTERN_COLOR = "246"
PATH_COLOR = "51"

PIXEL = "  "


def _bg(color_code: str) -> str:
    return f"\033[48;5;{color_code}m"


def get_path_cells(
    entry: tuple[int, int],
    path: list[str],
) -> set[tuple[int, int]]:
    x, y = entry
    cells = {(x, y)}

    moves = {
        "N": (0, -1),
        "E": (1, 0),
        "S": (0, 1),
        "W": (-1, 0),
    }

    for move in path:
        dx, dy = moves[move]
        x += dx
        y += dy
        cells.add((x, y))

    return cells


def _build_canvas(
    maze: MazeGenerator,
    entry: tuple[int, int],
    exit_: tuple[int, int],
    path: list[str],
    wall_color: str,
    floor_color: str,
) -> list[list[str]]:
    canvas_width = 2 * maze.width + 1
    canvas_height = 2 * maze.height + 1

    canvas = [
        [wall_color for _ in range(canvas_width)]
        for _ in range(canvas_height)
    ]

    for y in range(maze.height):
        for x in range(maze.width):
            cell = maze.grid[y][x]
            cx, cy = 2 * x + 1, 2 * y + 1

            if (x, y) in maze.pattern_cells:
                fill = PATTERN_COLOR
            else:
                fill = floor_color

            canvas[cy][cx] = fill

            if not cell & MazeGenerator.N:
                canvas[cy - 1][cx] = fill
            if not cell & MazeGenerator.E:
                canvas[cy][cx + 1] = fill
            if not cell & MazeGenerator.S:
                canvas[cy + 1][cx] = fill
            if not cell & MazeGenerator.W:
                canvas[cy][cx - 1] = fill

    x, y = entry
    canvas[2 * y + 1][2 * x + 1] = PATH_COLOR

    moves = {
        "N": (0, -1),
        "E": (1, 0),
        "S": (0, 1),
        "W": (-1, 0),
    }

    for move in path:
        dx, dy = moves[move]
        nx, ny = x + dx, y + dy

        cx, cy = 2 * x + 1, 2 * y + 1
        ncx, ncy = 2 * nx + 1, 2 * ny + 1

        canvas[(cy + ncy) // 2][(cx + ncx) // 2] = PATH_COLOR
        canvas[ncy][ncx] = PATH_COLOR

        x, y = nx, ny

    ex, ey = entry
    fx, fy = exit_
    canvas[2 * ey + 1][2 * ex + 1] = ENTRY_COLOR
    canvas[2 * fy + 1][2 * fx + 1] = EXIT_COLOR

    return canvas


def draw_maze(
    maze: MazeGenerator,
    entry: tuple[int, int],
    exit_: tuple[int, int],
    path: list[str],
    show_path: bool = False,
    color_index: int = 0,
) -> None:
    palette = WALL_COLOR_PALETTES[color_index % len(WALL_COLOR_PALETTES)]
    wall_color, floor_color = palette

    displayed_path = path if show_path else []

    canvas = _build_canvas(
        maze,
        entry,
        exit_,
        displayed_path,
        wall_color,
        floor_color,
    )

    lines = [
        "".join(f"{_bg(color)}{PIXEL}{RESET}" for color in row)
        for row in canvas
    ]

    print("\n".join(lines))
