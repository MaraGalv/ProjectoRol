class Equipment:
    def __init__(self):
        self.name = ""
        self.description = ""
        self.slot = ""
        self.requisites = {}
        self.bonuses = {}
        self.damage = ""
        self.feats = {}

    def create_equipment(self, data):
        self.name = data["name"]
        self.description = data["description"]
        self.slot = data["slot"]
        self.requisites = data["requisites"]
        self.bonuses = data["bonuses"]
        self.damage = data["damage"]
        self.feats = data["feats"]