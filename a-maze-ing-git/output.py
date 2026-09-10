from pathlib import Path

from mazegen import MazeGenerator


def output_maze(
    maze: MazeGenerator,
    output_path: Path,
    path: list[str],
    entry: tuple[int, int],
    exit: tuple[int, int],
) -> None:
    with output_path.open("w", encoding="utf-8") as file:
        for row in maze.grid:
            line = "".join(f"{cell:X}" for cell in row)
            file.write(line + "\n")

        file.write("\n")

        ex, ey = entry
        fx, fy = exit

        file.write(f"{ex},{ey}\n")
        file.write(f"{fx},{fy}\n")
        file.write("".join(path) + "\n")
