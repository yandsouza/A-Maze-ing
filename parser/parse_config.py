def parse_config(path: str) -> None:
    data: dict[str, str] = {}

    try:
        with open(path, "r", encoding="utf-8") as file:
            for i, raw_line in enumerate(file, start=1):
                line = raw_line.strip()

                if not line or line.startswith("#"):
                    continue

                if "=" not in line:
                    raise Exception(f"Invalid input at line {i}.")

                key, value = line.split("=", maxsplit=1)
                data[key.strip()] = value.strip()
            print(data)
    except FileNotFoundError as error:
        print(error)
