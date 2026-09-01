from typing import Any


def parse_config(path: str) -> None:
    config: dict[str, str] = {}

    try:
        with open(path, "r", encoding="utf-8") as file:
            for i, raw_line in enumerate(file, start=1):
                line = raw_line.strip()

                if not line or line.startswith("#"):
                    continue

                if "=" not in line:
                    raise Exception(f"Invalid input at line {i}.")

                key, value = line.split("=", maxsplit=1)
                config[key.strip()] = value.strip()
            convert_data(config)
    except FileNotFoundError as error:
        print(error)


def convert_data(config: dict[str, str]) -> dict[str, Any]:
    safe_config: dict[str, Any] = {}

    try:
        safe_config["width"] = int(config["WIDTH"])
    except Exception as error:
        print(error)

    try:
        safe_config["height"] = int(config["HEIGHT"])
    except Exception as error:
        print(error)

    try:
        x, y = config["ENTRY"].split(",", maxsplit=1)
        safe_config["entry"] = (int(x), int(y))
    except Exception as error:
        print(error)

    try:
        x, y = config["EXIT"].split(",", maxsplit=1)
        safe_config["exit"] = (int(x), int(y))
    except Exception as error:
        print(error)

    safe_config["output_file"] = config["OUTPUT_FILE"]

    if config["PERFECT"] == "True":
        safe_config["perfect"] = True
    else:
        safe_config["perfect"] = False

    return safe_config
