from collections import deque
import random

class MazeGenerator:
    N, E, S, W = 1, 2, 4, 8

    OPPOSITE = {N: S, S: N, E: W, W: E}

    def __init__(
        self,
        width: int,
        height: int,
        perfect: bool = False,
        seed: int | None = None,
    ) -> None:
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

    def _place_42(self) -> None:
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
                nx, ny, direction = self.random.choice(unvisited_neighbors)

                self.grid[cy][cx] &= ~direction
                self.grid[ny][nx] &= ~self.OPPOSITE[direction]

                self.visited[ny][nx] = True
                stack.append((nx, ny))
            else:
                stack.pop()

        if not self.perfect:
            self._make_playable_board()


    def _break_random_wall(self, x: int, y: int) -> bool:

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
        return self.grid[y][x].bit_count()

    def _make_playable_board(self) -> None:
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
    ) -> str:
        queue = deque([(start_x, start_y, "")])
        visited = {(start_x, start_y)}

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
                    queue.append((nx, ny, path + letter))

        return ""

    def get_grid(self) -> list[list[int]]:
        return self.grid