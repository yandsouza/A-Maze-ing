"""Parse and validate the maze configuration file into a typed config dict."""
from typing import TypedDict


class Config(TypedDict):
    """Typed dictionary describing the validated maze configuration."""
    width: int
    height: int
    entry: tuple[int, int]
    exit: tuple[int, int]
    perfect: bool
    seed: int | None
    output_file: str


def validate_keys(config: dict[str, str]) -> None:
    """Ensure all required configuration keys are present.

    Raises ValueError listing any missing keys.
    """
    required_keys = {
        "WIDTH",
        "HEIGHT",
        "ENTRY",
        "EXIT",
        "OUTPUT_FILE",
        "PERFECT",
    }

    missing = required_keys - config.keys()

    if missing:
        raise ValueError(
            f"Missing required keys: {', '.join(sorted(missing))}"
        )


def validate_dimension(value: str, name: str) -> int:
    """Parse and validate a positive integer dimension from a string."""
    try:
        dimension = int(value)
    except ValueError:
        raise ValueError(
            f"{name} must be a positive integer."
        )

    if dimension <= 0:
        raise ValueError(
            f"{name} must be a positive integer."
        )

    return dimension


def parse_coordinates(value: str, name: str) -> tuple[int, int]:
    """Parse an 'x,y' coordinate string into a tuple of integers."""
    parts = value.split(",")

    if len(parts) != 2:
        raise ValueError(
            f"{name} must have the format x,y."
        )

    try:
        x = int(parts[0].strip())
        y = int(parts[1].strip())
    except ValueError:
        raise ValueError(
            f"{name} coordinates must be integers."
        )

    return x, y


def parse_seed(value: str) -> int:
    """Parse the SEED value from a string into an integer."""
    try:
        return int(value)
    except ValueError:
        raise ValueError(
            "SEED must be an integer."
        )


def parse_output_file(value: str) -> str:
    """Validate and return the output file path string."""
    if not value:
        raise ValueError(
            "OUTPUT_FILE must not be empty."
        )

    return value


def parse_config(path: str) -> Config:
    """Read, validate, and convert a config file into a Config dictionary."""
    config: dict[str, str] = {}

    with open(path, "r", encoding="utf-8") as file:
        for i, raw_line in enumerate(file, start=1):
            line = raw_line.strip()

            if not line or line.startswith("#"):
                continue

            if "=" not in line:
                raise ValueError(
                    f"Invalid input at line {i}."
                )

            key, value = line.split("=", maxsplit=1)
            config[key.strip()] = value.strip()

    validate_keys(config)
    return convert_data(config)


def convert_data(config: dict[str, str]) -> Config:
    """Convert raw string config values into validated typed values."""
    width = validate_dimension(
        config["WIDTH"],
        "WIDTH",
    )

    height = validate_dimension(
        config["HEIGHT"],
        "HEIGHT",
    )

    entry = parse_coordinates(
        config["ENTRY"],
        "ENTRY",
    )

    exit = parse_coordinates(
        config["EXIT"],
        "EXIT",
    )

    entry_x, entry_y = entry
    exit_x, exit_y = exit

    if not (0 <= entry_x < width and 0 <= entry_y < height):
        raise ValueError(
            "ENTRY coordinates are out of bounds."
        )

    if not (0 <= exit_x < width and 0 <= exit_y < height):
        raise ValueError(
            "EXIT coordinates are out of bounds."
        )

    if entry == exit:
        raise ValueError(
            "ENTRY and EXIT must be different."
        )

    if config["PERFECT"] == "True":
        perfect = True
    elif config["PERFECT"] == "False":
        perfect = False
    else:
        raise ValueError(
            "PERFECT must be either True or False."
        )

    seed: int | None = None

    if "SEED" in config:
        seed = parse_seed(config["SEED"])

    output_file = parse_output_file(
        config["OUTPUT_FILE"]
    )

    return {
        "width": width,
        "height": height,
        "entry": entry,
        "exit": exit,
        "perfect": perfect,
        "seed": seed,
        "output_file": output_file,
    }
