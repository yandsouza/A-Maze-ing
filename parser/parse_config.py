def parse_config():
    contents = ""
    with open("config.txt", "r") as file:
        contents = file.read()
        print(contents)
