import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from feat_parser import FeatParser

class TestFeatParser(unittest.TestCase):
    def setUp(self):
        self.character_data = {
            'Strength': 18,
            'Dexterity': 12,
            'Level': 5,
            'Skills': {
                'CloseCombat': 4,
                'RangedCombat': 3
            }
        }
        self.parser = FeatParser(self.character_data)

    def test_attribute_mapping(self):
        self.assertIn('Strength', self.parser.attribute_map)
        self.assertIn('CloseCombat', self.parser.attribute_map)
        self.assertEqual(self.parser.attribute_map['Strength']['value'], 18)

    def test_extract_dice_and_numbers(self):
        desc = "Deal 2d6+3 damage and add 5 extra points"
        result = self.parser.extract_dice_and_numbers(desc)
        self.assertIn("2d6+3", result['dice'])
        self.assertIn(5, result['numbers'])

    def test_validate_description(self):
        valid, msg, used = self.parser.validate_description("Use Strength to strike")
        self.assertTrue(valid)
        self.assertIn("Strength", used)

    def test_parse_description(self):
        desc = "Strength + CloseCombat + 1d8"
        valid, _, used = self.parser.validate_description(desc)
        result = self.parser.parse_description(desc, used)
        self.assertIn("1d8", result['dice'])
        self.assertIn("18", result['parsed_description'])
        self.assertIn("4", result['parsed_description'])

    def test_create_feat_success(self):
        feat = self.parser.create_feat("Power Strike", "Strength + 1d6")
        self.assertEqual(feat.name, "Power Strike")
        self.assertIn("1d6", feat.parsed_description)

    def test_create_feat_fail(self):
        with self.assertRaises(ValueError):
            self.parser.create_feat("", "No attribute")

        with self.assertRaises(ValueError):
            self.parser.create_feat("Test", "NoAttrHere")

if __name__ == '__main__':
    unittest.main()
