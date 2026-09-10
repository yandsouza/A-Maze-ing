from mazegen import MazeGenerator


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


def draw_maze(
    maze: MazeGenerator,
    entry: tuple[int, int],
    exit: tuple[int, int],
    path: list[str],
) -> None:
    path_cells = get_path_cells(entry, path)

    for y in range(maze.height):
        top = ""

        for x in range(maze.width):
            cell = maze.grid[y][x]

            if cell & MazeGenerator.N:
                top += "+---"
            else:
                top += "+   "

        top += "+"
        print(top)

        middle = ""

        for x in range(maze.width):
            cell = maze.grid[y][x]

            if cell & MazeGenerator.W:
                middle += "|"
            else:
                middle += " "

            if (x, y) == entry:
                middle += " S "
            elif (x, y) == exit:
                middle += " E "
            elif (x, y) in path_cells:
                middle += " . "
            else:
                middle += "   "

        cell = maze.grid[y][maze.width - 1]

        if cell & MazeGenerator.E:
            middle += "|"
        else:
            middle += " "

        print(middle)

    bottom = ""

    for x in range(maze.width):
        cell = maze.grid[maze.height - 1][x]

        if cell & MazeGenerator.S:
            bottom += "+---"
        else:
            bottom += "+   "

    bottom += "+"
    print(bottom)


if __name__ == "__main__":
    maze = MazeGenerator(
        10,
        10,
        perfect=True,
        seed=42,
    )

    entry = (0, 0)
    exit = (9, 9)

    path = maze.solve(
        entry[0],
        entry[1],
        exit[0],
        exit[1],
    )

    draw_maze(
        maze,
        entry,
        exit,
        path,
    )