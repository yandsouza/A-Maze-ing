import sys
from parser import parse_config
from mazegen import MazeGenerator


def main() -> None:
    if len(sys.argv) == 1:
        print("Usage: a_maze_ing.py config.txt")
        return

    config = parse_config(sys.argv[1])
    maze = MazeGenerator()


if __name__ == "__main__":
    main()
