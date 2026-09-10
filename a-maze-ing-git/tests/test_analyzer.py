from pathlib import Path
import sys

def count_edges(
    maze: list[list[int]],
    protected: set[tuple[int, int]],
) -> int:
    height = len(maze)
    width = len(maze[0])
    edges = 0

    for y in range(height):
        for x in range(width):
            if (x, y) in protected:
                continue

            cell = maze[y][x]

            if x + 1 < width:
                if (x + 1, y) not in protected:
                    if not (cell & 2):
                        edges += 1

            if y + 1 < height:
                if (x, y + 1) not in protected:
                    if not (cell & 4):
                        edges += 1

    return edges


def check_perfect(
    maze: list[list[int]],
    protected: set[tuple[int, int]],
) -> bool:
    height = len(maze)
    width = len(maze[0])

    vertices = width * height - len(protected)
    edges = count_edges(maze, protected)

    return edges == vertices - 1


def read_maze(
    path: Path,
) -> tuple[list[list[int]], tuple[int, int], tuple[int, int], str]:
    with path.open("r", encoding="utf-8") as file:
        lines = []

        for line in file:
            line = line.strip()

            if not line:
                break

            lines.append(line)

        entry = tuple(map(int, file.readline().strip().split(",")))
        exit = tuple(map(int, file.readline().strip().split(",")))
        solution = file.readline().strip()

    maze = [
        [int(cell, 16) for cell in row]
        for row in lines
    ]

    return maze, entry, exit, solution


def check_hex(maze: list[list[int]]) -> bool:
    for row in maze:
        for cell in row:
            if not 0 <= cell <= 15:
                return False

    return True

N, E, S, W = 1, 2, 4, 8


def check_walls(maze: list[list[int]]) -> bool:
    height = len(maze)
    width = len(maze[0])

    for y in range(height):
        for x in range(width):
            cell = maze[y][x]

            # Parede leste ↔ parede oeste da célula vizinha
            if x + 1 < width:
                neighbor = maze[y][x + 1]

                east_open = not (cell & E)
                west_open = not (neighbor & W)

                if east_open != west_open:
                    print(
                        f"Parede incoerente em "
                        f"({x},{y}) ↔ ({x + 1},{y})"
                    )
                    return False

            # Parede sul ↔ parede norte da célula vizinha
            if y + 1 < height:
                neighbor = maze[y + 1][x]

                south_open = not (cell & S)
                north_open = not (neighbor & N)

                if south_open != north_open:
                    print(
                        f"Parede incoerente em "
                        f"({x},{y}) ↔ ({x},{y + 1})"
                    )
                    return False

    return True

def check_borders(maze: list[list[int]]) -> bool:
    height = len(maze)
    width = len(maze[0])

    for y in range(height):
        for x in range(width):
            cell = maze[y][x]

            if y == 0 and not (cell & N):
                print(f"Borda norte aberta em ({x},{y})")
                return False

            if y == height - 1 and not (cell & S):
                print(f"Borda sul aberta em ({x},{y})")
                return False

            if x == 0 and not (cell & W):
                print(f"Borda oeste aberta em ({x},{y})")
                return False

            if x == width - 1 and not (cell & E):
                print(f"Borda leste aberta em ({x},{y})")
                return False

    return True


def get_42_cells(
    width: int,
    height: int,
) -> set[tuple[int, int]]:
    pattern_42 = [
        "X.X XX",
        "XXX .X",
        "..X XX",
        "..X X.",
        "..X XX",
    ]

    pattern_height = len(pattern_42)
    pattern_width = len(pattern_42[0])

    if width < pattern_width + 4 or height < pattern_height + 4:
        return set()

    start_x = (width - pattern_width) // 2
    start_y = (height - pattern_height) // 2

    cells: set[tuple[int, int]] = set()

    for y, row in enumerate(pattern_42):
        for x, char in enumerate(row):
            if char == "X":
                cells.add((start_x + x, start_y + y))

    return cells

def check_connectivity(maze: list[list[int]]) -> bool:
    height = len(maze)
    width = len(maze[0])

    visited: set[tuple[int, int]] = {(0, 0)}
    queue: list[tuple[int, int]] = [(0, 0)]

    directions = [
        (-1, 0, W),
        (1, 0, E),
        (0, -1, N),
        (0, 1, S),
    ]

    while queue:
        x, y = queue.pop(0)

        for dx, dy, direction in directions:
            nx = x + dx
            ny = y + dy

            if not (0 <= nx < width and 0 <= ny < height):
                continue

            if maze[y][x] & direction:
                continue

            if (nx, ny) in visited:
                continue

            visited.add((nx, ny))
            queue.append((nx, ny))

    pattern_cells = get_42_cells(width, height)

    normal_cells = {
        (x, y)
        for y in range(height)
        for x in range(width)
        if (x, y) not in pattern_cells
    }

    reachable_normal_cells = visited & normal_cells

    if reachable_normal_cells != normal_cells:
        missing = normal_cells - visited

        print(
            f"Conectividade: FALHOU "
            f"({len(reachable_normal_cells)}/"
            f"{len(normal_cells)} células normais alcançáveis)"
        )
        print(f"Células inacessíveis: {sorted(missing)}")
        return False

    return True


def check_solution(
    maze: list[list[int]],
    entry: tuple[int, int],
    exit: tuple[int, int],
) -> bool:
    width = len(maze[0])
    height = len(maze)

    queue: list[tuple[int, int]] = [entry]
    visited: set[tuple[int, int]] = {entry}

    directions = [
        (-1, 0, W),
        (1, 0, E),
        (0, -1, N),
        (0, 1, S),
    ]

    while queue:
        x, y = queue.pop(0)

        if (x, y) == exit:
            return True

        for dx, dy, direction in directions:
            nx = x + dx
            ny = y + dy

            if not (0 <= nx < width and 0 <= ny < height):
                continue

            if maze[y][x] & direction:
                continue

            if (nx, ny) in visited:
                continue

            visited.add((nx, ny))
            queue.append((nx, ny))

    return False


def check_path(
    maze: list[list[int]],
    entry: tuple[int, int],
    exit: tuple[int, int],
    path: str,
) -> bool:
    x, y = entry

    directions = {
        "N": (0, -1, N),
        "E": (1, 0, E),
        "S": (0, 1, S),
        "W": (-1, 0, W),
    }

    for move in path:
        if move not in directions:
            print(f"Movimento inválido: {move}")
            return False

        dx, dy, direction = directions[move]

        if maze[y][x] & direction:
            print(f"Parede fechada em ({x},{y}) para {move}")
            return False

        x += dx
        y += dy

        if not (0 <= x < len(maze[0]) and 0 <= y < len(maze)):
            print(f"Caminho saiu do maze em ({x},{y})")
            return False

    if (x, y) != exit:
        print(
            f"Caminho terminou em ({x},{y}), "
            f"mas deveria terminar em {exit}"
        )
        return False

    return True


def check_playable_points(maze: list[list[int]]) -> bool:
    height = len(maze)
    width = len(maze[0])

    points = [
        (0, 0),
        (width - 1, 0),
        (0, height - 1),
        (width - 1, height - 1),
        (width // 2, height // 2),
    ]

    for x, y in points:
        if maze[y][x] == 15:
            print(f"Célula sem passagem em ({x},{y})")
            return False

    return True

def check_loops(
    maze: list[list[int]],
    protected: set[tuple[int, int]],
) -> bool:
    height = len(maze)
    width = len(maze[0])

    vertices = width * height - len(protected)
    edges = count_edges(maze, protected)

    return edges > vertices - 1


def find_path(
    maze: list[list[int]],
    start: tuple[int, int],
    end: tuple[int, int],
    blocked_edge: tuple[tuple[int, int], tuple[int, int]] | None = None,
) -> bool:
    width = len(maze[0])
    height = len(maze)

    queue: list[tuple[int, int]] = [start]
    visited: set[tuple[int, int]] = {start}

    directions = [
        (-1, 0, W),
        (1, 0, E),
        (0, -1, N),
        (0, 1, S),
    ]

    while queue:
        x, y = queue.pop(0)

        if (x, y) == end:
            return True

        for dx, dy, direction in directions:
            nx = x + dx
            ny = y + dy

            if not (0 <= nx < width and 0 <= ny < height):
                continue

            edge = ((x, y), (nx, ny))
            reverse_edge = ((nx, ny), (x, y))

            if (
                blocked_edge == edge
                or blocked_edge == reverse_edge
            ):
                continue

            if maze[y][x] & direction:
                continue

            if (nx, ny) in visited:
                continue

            visited.add((nx, ny))
            queue.append((nx, ny))

    return False


def check_two_routes(
    maze: list[list[int]],
    entry: tuple[int, int],
    exit: tuple[int, int],
) -> bool:
    width = len(maze[0])
    height = len(maze)

    queue: list[tuple[int, int, list[tuple[int, int]]]] = [
        (entry[0], entry[1], [])
    ]

    visited: set[tuple[int, int]] = {entry}

    directions = [
        (-1, 0, W),
        (1, 0, E),
        (0, -1, N),
        (0, 1, S),
    ]

    while queue:
        x, y, path = queue.pop(0)

        if (x, y) == exit:
            for edge in path:
                if find_path(
                    maze,
                    entry,
                    exit,
                    edge,
                ):
                    return True
            return False

        for dx, dy, direction in directions:
            nx = x + dx
            ny = y + dy

            if not (0 <= nx < width and 0 <= ny < height):
                continue

            if maze[y][x] & direction:
                continue

            if (nx, ny) in visited:
                continue

            visited.add((nx, ny))
            queue.append(
                (nx, ny, path + [((x, y), (nx, ny))])
            )

    return False


def check_no_3x3_open_area(maze: list[list[int]]) -> bool:
    height = len(maze)
    width = len(maze[0])

    for start_y in range(height - 2):
        for start_x in range(width - 2):
            open_connections = 0

            # Verifica as conexões horizontais.
            for y in range(start_y, start_y + 3):
                for x in range(start_x, start_x + 2):
                    if not (maze[y][x] & E):
                        open_connections += 1

            # Verifica as conexões verticais.
            for y in range(start_y, start_y + 2):
                for x in range(start_x, start_x + 3):
                    if not (maze[y][x] & S):
                        open_connections += 1

            # Um 3x3 completamente aberto possui:
            # 3 linhas * 2 conexões horizontais = 6
            # 2 linhas * 3 conexões verticais = 6
            # Total = 12 conexões.
            if open_connections == 12:
                print(
                    f"Área aberta 3x3 encontrada em "
                    f"({start_x},{start_y})"
                )

                for y in range(start_y, start_y + 3):
                    print(
                        " ".join(
                            f"{maze[y][x]:X}"
                            for x in range(start_x, start_x + 3)
                        )
                    )

                return False

    return True

def main() -> None:
    maze, entry, exit, path = read_maze(Path("maze.txt"))

    print(f"Dimensões: {len(maze[0])}x{len(maze)}")

    if check_hex(maze):
        print("HEX: PASSOU")
    else:
        print("HEX: FALHOU")

    if check_walls(maze):
        print("PAREDES: PASSOU")
    else:
        print("PAREDES: FALHOU")

    if check_borders(maze):
        print("BORDAS: PASSOU")
    else:
        print("BORDAS: FALHOU")

    if check_connectivity(maze):
        print("CONECTIVIDADE: PASSOU")
    else:
        print("CONECTIVIDADE: FALHOU")

    if check_solution(maze, entry, exit):
        print("SOLUÇÃO: PASSOU")
    else:
        print("SOLUÇÃO: FALHOU")

    if check_path(maze, entry, exit, path):
        print("CAMINHO: PASSOU")
    else:
        print("CAMINHO: FALHOU")

    perfect = sys.argv[1] == "True"
    protected = get_42_cells(len(maze[0]), len(maze))

    if perfect:
        if check_perfect(maze, protected):
            print("PERFECT: PASSOU")
        else:
            print("PERFECT: FALHOU")
    if not perfect:
        if check_playable_points(maze):
            print("PONTOS JOGÁVEIS: PASSOU")
        else:
            print("PONTOS JOGÁVEIS: FALHOU")

        if check_loops(maze, protected):
            print("LOOPS: PASSOU")
        else:
            print("LOOPS: FALHOU")

        if check_two_routes(maze, entry, exit):
            print("DUAS ROTAS: PASSOU")
        else:
            print("DUAS ROTAS: FALHOU")

        if check_no_3x3_open_area(maze):
            print("ÁREA 3x3: PASSOU")
        else:
            print("ÁREA 3x3: FALHOU")


if __name__ == "__main__":
    main()
