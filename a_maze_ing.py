import sys
from pathlib import Path

import menu
from parse_config import parse_config
from mazegen import MazeGenerator
from output import output_maze


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: a_maze_ing.py config.txt")
        return

    try:
        config = parse_config(sys.argv[1])
    except (FileNotFoundError, ValueError) as error:
        print(f"Error: {error}")
        return

    output_file = Path(config["output_file"])
    entry_x, entry_y = config["entry"]
    exit_x, exit_y = config["exit"]

    maze = MazeGenerator(
        config["width"],
        config["height"],
        config["perfect"],
        config.get("seed"),
    )

    solution = maze.solve(
        entry_x,
        entry_y,
        exit_x,
        exit_y,
    )

    output_maze(
        maze,
        output_file,
        solution,
        (entry_x, entry_y),
        (exit_x, exit_y),
    )

    menu.run(
        maze,
        solution,
        (entry_x, entry_y),
        (exit_x, exit_y),
        config["width"],
        config["height"],
        config["perfect"],
        config.get("seed")
    )


if __name__ == "__main__":
    main()
