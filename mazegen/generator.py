from collections import deque
import random


class MazeGenerator:
    """
    Generate and solve mazes using a depth-first search algorithm.

    The maze is represented as a grid of hexadecimal values, where each
    bit corresponds to a wall:

        N = 1 (North)
        E = 2 (East)
        S = 4 (South)
        W = 8 (West)

    A set bit means that the wall exists, while a cleared bit means that
    the passage is open.

    The generator supports two modes:

    - perfect=True:
      Creates a perfect maze with exactly one path between any two cells.

    - perfect=False:
      Creates a Pac-Man-like board with loops, fewer dead ends and
      accessible special positions.

    A "42" pattern may also be placed in the centre of large mazes.
    """

    N, E, S, W = 1, 2, 4, 8

    OPPOSITE = {N: S, S: N, E: W, W: E}

    def __init__(
        self,
        width: int,
        height: int,
        perfect: bool = False,
        seed: int | None = None,
    ) -> None:
        """
        Initialize the maze generator.

        Args:
            width: Maze width in cells.
            height: Maze height in cells.
            perfect: Generate a perfect maze if True.
            seed: Optional random seed for reproducible mazes.
        """
        self.width = width
        self.height = height
        self.perfect = perfect
        self.random = random.Random(seed)

        self.grid = [
            [15 for _ in range(width)]
            for _ in range(height)
        ]

        self.visited = [
            [False for _ in range(width)]
            for _ in range(height)
        ]

        self.pattern_cells: set[tuple[int, int]] = set()

        self._place_42()
        self.generate()

    def _place_42(self) -> None:
        """
        Place the "42" pattern in the centre of the maze.

        Protected cells are marked as already visited so the generation
        algorithm does not carve passages through the pattern.

        If the maze is too small, the pattern is not placed.
        """
        pattern_42 = [
            "X.X XX",
            "XXX .X",
            "..X XX",
            "..X X.",
            "..X XX",
        ]

        pattern_height = len(pattern_42)
        pattern_width = len(pattern_42[0])

        if (
            self.width < pattern_width + 4
            or self.height < pattern_height + 4
        ):
            return

        start_x = (self.width - pattern_width) // 2
        start_y = (self.height - pattern_height) // 2

        for y, row in enumerate(pattern_42):
            for x, char in enumerate(row):
                if char == "X":
                    cell_x = start_x + x
                    cell_y = start_y + y

                    self.pattern_cells.add((cell_x, cell_y))
                    self.visited[cell_y][cell_x] = True

    def generate(self) -> None:
        """
        Generate the maze using an iterative depth-first search algorithm.

        The algorithm starts from the top-left cell and removes walls
        between neighbouring cells until all reachable cells are visited.

        If the maze is not perfect, additional modifications are applied
        to create a more playable board.
        """
        directions = [
            (0, -1, self.N),
            (1, 0, self.E),
            (0, 1, self.S),
            (-1, 0, self.W),
        ]

        start_x, start_y = 0, 0
        self.visited[start_y][start_x] = True
        stack = [(start_x, start_y)]

        while stack:
            cx, cy = stack[-1]
            unvisited_neighbors = []

            for dx, dy, direction in directions:
                nx = cx + dx
                ny = cy + dy

                if (
                    0 <= nx < self.width
                    and 0 <= ny < self.height
                    and not self.visited[ny][nx]
                ):
                    unvisited_neighbors.append((nx, ny, direction))

            if unvisited_neighbors:
                nx, ny, direction = self.random.choice(
                    unvisited_neighbors
                )

                self.grid[cy][cx] &= ~direction
                self.grid[ny][nx] &= ~self.OPPOSITE[direction]

                self.visited[ny][nx] = True
                stack.append((nx, ny))
            else:
                stack.pop()

        if not self.perfect:
            self._make_playable_board()

    def _break_random_wall(self, x: int, y: int) -> bool:
        """
        Remove a random wall from a cell.

        Protected cells belonging to the "42" pattern are ignored.

        Args:
            x: Cell x coordinate.
            y: Cell y coordinate.

        Returns:
            True if a wall was removed, False otherwise.
        """
        if (x, y) in self.pattern_cells:
            return False

        directions = [
            (0, -1, self.N),
            (1, 0, self.E),
            (0, 1, self.S),
            (-1, 0, self.W),
        ]

        valid_walls = []

        for dx, dy, direction in directions:
            nx = x + dx
            ny = y + dy

            if not (0 <= nx < self.width and 0 <= ny < self.height):
                continue

            if (nx, ny) in self.pattern_cells:
                continue

            if self.grid[y][x] & direction:
                valid_walls.append((nx, ny, direction))

        if not valid_walls:
            return False

        nx, ny, direction = self.random.choice(valid_walls)

        self.grid[y][x] &= ~direction
        self.grid[ny][nx] &= ~self.OPPOSITE[direction]

        return True

    def _count_walls(self, x: int, y: int) -> int:
        """
        Count how many walls a cell currently has.

        Args:
            x: Cell x coordinate.
            y: Cell y coordinate.

        Returns:
            Number of walls in the cell.
        """
        return self.grid[y][x].bit_count()

    def _make_playable_board(self) -> None:
        """
        Transform a perfect maze into a Pac-Man-like board.

        This method reduces dead ends, creates loops, and opens the four
        corners and the centre of the maze.
        """
        dead_ends = {7, 11, 13, 14}

        for y in range(self.height):
            for x in range(self.width):
                if (
                    self.grid[y][x] in dead_ends
                    and (x, y) not in self.pattern_cells
                ):
                    self._break_random_wall(x, y)

        special_cells = [
            (0, 0),
            (self.width - 1, 0),
            (0, self.height - 1),
            (self.width - 1, self.height - 1),
            (self.width // 2, self.height // 2),
        ]

        for x, y in special_cells:
            while self._count_walls(x, y) > 2:
                if not self._break_random_wall(x, y):
                    break

    def solve(
        self,
        start_x: int,
        start_y: int,
        end_x: int,
        end_y: int,
    ) -> list[str]:
        """
        Find the shortest path between two cells using BFS.

        Args:
            start_x: Starting x coordinate.
            start_y: Starting y coordinate.
            end_x: Destination x coordinate.
            end_y: Destination y coordinate.

        Returns:
            A list of movement letters: N, E, S and W.
        """
        queue: deque[tuple[int, int, list[str]]] = deque(
            [(start_x, start_y, [])]
        )

        visited: set[tuple[int, int]] = {(start_x, start_y)}

        moves = [
            (0, -1, self.N, "N"),
            (1, 0, self.E, "E"),
            (0, 1, self.S, "S"),
            (-1, 0, self.W, "W"),
        ]

        while queue:
            cx, cy, path = queue.popleft()

            if cx == end_x and cy == end_y:
                return path

            for dx, dy, direction, letter in moves:
                nx = cx + dx
                ny = cy + dy

                if (
                    0 <= nx < self.width
                    and 0 <= ny < self.height
                    and not (self.grid[cy][cx] & direction)
                    and (nx, ny) not in visited
                ):
                    visited.add((nx, ny))
                    queue.append(
                        (nx, ny, path + [letter])
                    )

        return []

    def get_grid(self) -> list[list[int]]:
        """
        Return the maze grid.

        Returns:
            The maze represented as hexadecimal wall values.
        """
        return self.grid
