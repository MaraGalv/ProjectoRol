import json

class ConfigurationParser():
    def __init__(self):
        self.language = ""
        self.translation = dict()
        self.config = dict()
        self.read_configuration()

    def read_configuration(self):
        self.config = json.load(open("options.json"))
        self.language = self.config["language"]
        self.read_language_json()

    def read_language_json(self):
        language_file = "Languages/" + self.language + ".json"
        self.translation = json.load(open(language_file))

    def change_language_in_file(self, language):
        self.config["language"] = language
        with open("options.json", "w") as file:
            file.write(json.dumps(self.config))
        self.read_configuration()