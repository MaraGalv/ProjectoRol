import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from character import Character
from feat_parser import Feat
from stats_management import Stat

stats = [["Strength", 12, False], ["Dexterity", 20, False], ["Intelligence", 10, False], ["Athletics", 10, False], ["Stealth", 8, True], ["Arcana", 5, True]]
sheet_model_path = "tests/test_sheet_model.json"
sheet_model_path_stats = "tests/test_sheet_model_stats.json"
sheet_model_path_position = "tests/test_sheet_model_position.json"

class CharacterTests(unittest.TestCase):

    def test_character_initialization(self):
        hero = Character(stats, sheet_model_path)
        for i, stat in enumerate(hero.stats_manager.stats):
            if i >= len(stats):
                break
            self.assertEqual(stat.name, stats[i][0])
            self.assertEqual(stat.current, stats[i][1])
            self.assertEqual(stat.favorited, stats[i][2])
        self.assertEqual(hero.level, 1)
        self.assertEqual(hero.experience, 0)
        self.assertEqual(hero.experience_to_next_level, 100)
        self.assertEqual(len(hero.feats), 0)
        self.assertIsNotNone(hero.game_system)

    def test_character_can_level_up(self):
        hero = Character(stats)
        hero.experience = 100
        self.assertTrue(hero.can_level_up())

    def test_character_wont_level_up_if_not_exp_used(self):
        hero = Character(stats, sheet_model_path)
        hero.experience = 100
        hero.game_system.exp_style = 1
        self.assertFalse(hero.can_level_up())

    def test_prepare_for_level_up_applies_favorited_bonus(self):
        hero = Character(stats)
        hero.prepare_for_level_up()

        for stat in hero.stats_manager.stats:
            expected_value = stat.current + 1 if stat.favorited else stat.current
            self.assertEqual(stat.pending_value, expected_value)

    def test_prepare_for_level_up_do_not_applies_favorited_bonus(self):
        hero = Character(stats, sheet_model_path)
        hero.prepare_for_level_up()
        hero.game_system.favorited_style = 0
        for stat in hero.stats_manager.stats:
            expected_value = stat.current
            self.assertEqual(stat.pending_value, expected_value)

    def test_level_up_raises_if_not_enough_xp(self):
        hero = Character(stats)
        hero.experience = 50
        with self.assertRaises(ValueError):
            hero.level_up()

    def test_level_up_increases_level_and_updates_stats(self):
        hero = Character(stats)
        hero.experience = 120
        hero.prepare_for_level_up()

        # Manually simulate stat increase
        original_strength = hero.stats_manager.stats[0].current
        hero.stats_manager.stats[0].pending_value += 2

        hero.level_up()

        self.assertEqual(hero.level, 2)
        self.assertEqual(hero.stats_manager.stats[0].current, original_strength + 2)
        self.assertEqual(hero.experience, 20)
        self.assertEqual(hero.experience_to_next_level, 150)

    def test_stats_are_reset_to_pending(self):
        hero = Character(stats)
        hero.experience = 100
        hero.prepare_for_level_up()

        for stat in hero.stats_manager.stats:
            stat.pending_value += 1  # Simulate stat allocation

        hero.level_up()

        for stat in hero.stats_manager.stats:
            self.assertEqual(stat.current, stat.base)
            self.assertEqual(stat.current, stat.pending_value)

    def test_feat_is_added_correctly(self):
        hero = Character(stats)
        feat = Feat('Power Strike', 'Strength + 1d6', '18 + 1d6', ['Strength'], ['Strength'], ['1d6'], [])
        hero.add_feat(feat)
        self.assertEqual(len(hero.feats), 1)
        self.assertEqual(hero.feats[0].name, "Power Strike")
        self.assertEqual(hero.feats[0].description, "Strength + 1d6")
        self.assertEqual(hero.feats[0].parsed_description, "18 + 1d6")
        self.assertEqual(hero.feats[0].used_attributes, ["Strength"])
        self.assertEqual(hero.feats[0].attribute_paths, ['Strength'])
        self.assertEqual(hero.feats[0].dice, ['1d6'])
        self.assertEqual(hero.feats[0].numbers, [])

    def test_check_if_stats_are_valid(self):
        hero = Character(stats, sheet_model_path)
        self.assertEqual(hero.stats_manager.check_if_stats_are_valid(hero.game_system), True)
        hero.stats_manager.stats.append(Stat("Test", 0))
        self.assertEqual(hero.stats_manager.check_if_stats_are_valid(hero.game_system), True)
        hero.stats_manager.stats.clear()
        self.assertEqual(hero.stats_manager.check_if_stats_are_valid(hero.game_system), False)

    def test_character_stat_is_upgradable(self):
        hero = Character(None, sheet_model_path_stats)
        hero.experience = 100
        stat = Stat("Atributos.Fisicos.Fuerza", 1)
        self.assertTrue(hero.is_stat_upgradable(stat))
        stat = Stat("Fuerza de Voluntad", 4)
        self.assertFalse(hero.is_stat_upgradable(stat))
        hero.experience = 0
        stat = Stat("Atributos.Fisicos.Fuerza", 1)
        self.assertFalse(hero.is_stat_upgradable(stat))

    def test_character_stat_is_upgraded(self):
        hero = Character(None, sheet_model_path_stats)
        hero.experience = 100
        stat = Stat("Atributos.Fisicos.Fuerza", 1)
        hero.upgrade_stat(stat)
        self.assertEqual(stat.current, 2)

    def test_character_calculates_position_correctly(self):
        hero = Character(None, sheet_model_path_position)
        hero.experience = 100
        data_position = hero.calculate_data_position((640, 480),(10, 20))
        data_position_matcher = {
            "Dead Light 1.0": (320, 20),
            "Nombre: Test": (10, 83),
            "Jugador: Test": (320, 83),
            "Naturaleza: Caotica": (630, 83),
            "Atributos": (320, 146),
            "Fisicos": (10, 209),
            "Sociales": (217, 209),
            "Mentales": (423, 209),
            "Suerte": (630, 209),
            "Fuerza": (10, 271),
            "Destreza": (10, 334),
            "Resistencia": (10,397),
            "Agilidad": (10, 460),
            "Carisma": (217, 271),
            "Constitucion": (217, 334),
            "Apariencia": (217,397),
            "Sabiduria": (217, 460),
            "Percepcion": (423, 271),
            "Inteligencia": (423, 334),
            "Astucia": (423, 397),
            "Trance": (423, 460),
            "Suerte2": (630, 271)}
        self.assertDictEqual(data_position, data_position_matcher)
        

if __name__ == "__main__":
    unittest.main()