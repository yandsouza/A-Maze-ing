from __future__ import annotations
from mazegen import MazeGenerator
from visualizer import WALL_COLOR_PALETTES, draw_maze
import os

MENU_TEXT = """=== A-Maze-ing ===
1. Re-generate a new maze
2. Show / Hide the shortest path
3. Rotate the wall colours
4. Quit
"""

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')


def run(
    maze: MazeGenerator,
    solution: list[str],
    entry: tuple[int, int],
    exit_: tuple[int, int],
    width: int,
    height: int,
    perfect: bool,
    seed: int | None = None,
) -> None:
    show_path = False
    color_index = 0

    while True:
        clear_terminal()
        draw_maze(maze, entry, exit_, solution, show_path, color_index)
        print(MENU_TEXT)

        try:
            choice = input("Choice? (1-4): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            return

        if choice == "1":
            print("\033[3A", end="")
            maze = MazeGenerator(width, height, perfect, seed)
            solution = maze.solve(
                entry[0],
                entry[1],
                exit_[0],
                exit_[1],
            )
        elif choice == "2":
            show_path = not show_path
        elif choice == "3":
            color_index = (color_index + 1) % len(WALL_COLOR_PALETTES)
        elif choice == "4":
            return
        else:
            print("Please enter a number between 1 and 4.")
