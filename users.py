import csv
import os


class User():
    def __init__(self):
        self.username = ""
        self.character_sheets = []
        self.games = []
        self.sheet_models = []

    def validate_user(self, name, password):
        if name == "" or password == "":
            return 0
        with open("users.csv","r") as file:
            parser = csv.reader(file, delimiter=",")
            for row in parser:
                if row[0] == name and row[1] == password:
                    self.username = name
                    self.get_user_data()
                    return 1
            return 0
        
    def register_user(self, name, password):
        if name == "" or password == "":
            return 0
        with open("users.csv","r") as file:
            parser = csv.reader(file, delimiter=",")
            for row in parser:
                if row[0] == name:
                    return 0
            
        with open("users.csv","a") as file:
            file.write(name + "," + password +"\n")
        self.username = name
        os.makedirs("Users/" + name)
        os.makedirs("Users/" + name + "/CharacterSheets")
        os.makedirs("Users/" + name + "/Games")
        os.makedirs("Users/" + name + "/SheetModels")
        self.get_user_data()
        return 1
    
    def get_character_sheets(self):
        for character_sheet in os.scandir("Users/" + self.username + "/CharacterSheets"):
            temp_dict = dict()
            temp_dict["name"] = character_sheet.name.removesuffix(".json")
            temp_dict["path"] = character_sheet.path
            self.character_sheets.append(temp_dict)
    
    def get_games(self):
        for game in os.scandir("Users/" + self.username + "/Games"):
            temp_dict = dict()
            temp_dict["name"] = game.name.removesuffix(".json")
            temp_dict["path"] = game.path
            self.games.append(temp_dict)

    def get_sheet_models(self):
        for sheet_model in os.scandir("Users/" + self.username + "/SheetModels"):
            temp_dict = dict()
            temp_dict["name"] = sheet_model.name.removesuffix(".json")
            temp_dict["path"] = sheet_model.path
            self.sheet_models.append(temp_dict)

    def get_user_data(self):
        self.get_character_sheets()
        self.get_games()
        self.get_sheet_models()