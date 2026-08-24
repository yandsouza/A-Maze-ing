import sys
from parser import parse_config


def main() -> None:
    if len(sys.argv) == 1:
        print("Usage: a_maze_ing.py config.txt")
        return

    parse_config(sys.argv[1])


if __name__ == "__main__":
    main()
