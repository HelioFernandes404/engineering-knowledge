def write_to_file(filename: str, content: str):
    with open(filename, "w") as file:
        file.write(content)
