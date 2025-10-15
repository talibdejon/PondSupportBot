def load_prompt(name):
    with open("resources/prompts/" + name + ".txt", "r", encoding="utf8") as file:
        return file.read()
