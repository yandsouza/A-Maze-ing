from mazegen import MazeGenerator
from pathlib import Path

def output_maze(
    maze: MazeGenerator,
    output_path: Path,
) -> None:
    with output_path.open("w") as f:
        out = ""
        for row in maze.grid:
            for cell in row:
                out += f"{cell:X}"
            out += "\n"
        f.write(out + "\n")

"""
        ex, ey = maze.entry
        fx, fy = maze.exit
        f.write(f"{ex},{ey}\n")
        f.write(f"{fx},{fy}\n")
"""
