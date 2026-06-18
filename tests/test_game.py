import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from game import Game
from character import Character
from game_system import GameSystem

stats = [["Strength", 12, False], ["Dexterity", 20, False], ["Intelligence", 10, False], ["Athletics", 10, False], ["Stealth", 8, True], ["Arcana", 5, True]]
sheet_model_path = "tests/test_sheet_model_game.json"
game_system = GameSystem()
game_system.load_system(sheet_model_path)

class TestGame(unittest.TestCase):

    def test_game_initializes_correctly(self):
        game = Game(game_system, "Dead Light", "Geno")
        self.assertEqual(game.name, "Dead Light")
        self.assertEqual(game.owner, "Geno")
        self.assertEqual(game.users, ["Geno"])
        self.assertEqual(game.characters, [])
        self.assertEqual(game.game_system, game_system)

    def test_game_adds_user_correctly(self):
        game = Game(game_system, "Dead Light", "Geno")
        game.add_user("Mara")
        self.assertEqual(game.users, ["Geno", "Mara"])

    def test_game_adds_character_correctly(self):
        game = Game(game_system, "Dead Light", "Geno")
        hero = Character(stats, sheet_model_path)
        hero.set_name("Atrax")
        hero.set_owner("Geno")
        game.add_character(hero)
        self.assertEqual(game.users, ["Geno"])
        self.assertEqual(len(game.characters), 1)
        self.assertEqual(game.characters[0][0].name, "Atrax")
        self.assertEqual(game.characters[0][1], True)
        hero2 = Character(stats, "tests/test_sheet_model.json")
        hero2.set_name("Malkar")
        hero2.set_owner("Mara")
        game.add_character(hero2)
        self.assertEqual(game.users, ["Geno", "Mara"])
        self.assertEqual(len(game.characters), 2)
        self.assertEqual(game.characters[0][0].name, "Atrax")
        self.assertEqual(game.characters[0][1], True)
        self.assertEqual(game.characters[1][0].name, "Malkar")
        self.assertEqual(game.characters[1][1], False)

    def test_game_removes_user_correctly(self):
        game = Game(game_system, "Dead Light", "Geno")
        game.add_user("Mara")
        self.assertEqual(game.users, ["Geno", "Mara"])
        game.remove_user("Mara")
        self.assertEqual(game.users, ["Geno"])

    def test_game_changes_character_ownership_correctly(self):
        game = Game(game_system, "Dead Light", "Geno")
        hero = Character(stats, sheet_model_path)
        hero.set_name("Atrax")
        hero.set_owner("Geno")
        game.add_character(hero)
        hero2 = Character(stats, "tests/test_sheet_model.json")
        hero2.set_name("Malkar")
        hero2.set_owner("Mara")
        game.add_character(hero2)
        game.remove_user("Mara")
        self.assertEqual(game.users, ["Geno"])
        self.assertEqual(len(game.characters), 2)
        self.assertEqual(game.characters[1][0].owner, "Geno")

    def test_game_removes_character_correctly(self):
        game = Game(game_system, "Dead Light", "Geno")
        hero = Character(stats, sheet_model_path)
        hero.set_name("Atrax")
        hero.set_owner("Geno")
        game.add_character(hero)
        hero2 = Character(stats, "tests/test_sheet_model.json")
        hero2.set_name("Malkar")
        hero2.set_owner("Mara")
        game.add_character(hero2)
        game.remove_character(hero2)
        self.assertEqual(game.users, ["Geno", "Mara"])
        self.assertEqual(len(game.characters), 1)
        self.assertEqual(game.characters[0][0].name, "Atrax")
        self.assertEqual(game.characters[0][1], True)