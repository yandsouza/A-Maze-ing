import sys
from pathlib import Path
from parser import parse_config
from mazegen import MazeGenerator
from output import output_maze


def main() -> None:
    if len(sys.argv) == 1:
        print("Usage: a_maze_ing.py config.txt")
        return

    config = parse_config(sys.argv[1])
    output_file = Path(config.pop("output_file"))

    maze = MazeGenerator(config["width"], config["height"])
    output_maze(maze, output_file)

if __name__ == "__main__":
    main()
