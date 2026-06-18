import sys
import os
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dice_roller import DiceRoller

class TestDiceRoller(unittest.TestCase):

    def test_dice_roller_makes_base_roll_correctly(self):
        dice_roller = DiceRoller()
        # Test d10 system (multiple rolls allowed)
        results = dice_roller.roll_base_dice(0, 5)
        self.assertEqual(len(results), 5)
        for value in results:
            self.assertGreaterEqual(value, 1)
            self.assertLessEqual(value, 10)

        # Test d20 system
        result = dice_roller.roll_base_dice(1)
        self.assertGreaterEqual(value, 1)
        self.assertLessEqual(value, 20)

        # Test d100 system
        result = dice_roller.roll_base_dice(2)
        self.assertGreaterEqual(value, 1)
        self.assertLessEqual(value, 100)

        # Test that multiple dice are not allowed for d20/d100
        result = dice_roller.roll_base_dice(1, 3)
        self.assertIsInstance(result, int)
        result = dice_roller.roll_base_dice(2, 3)
        self.assertIsInstance(result, int)

    def test_dice_roller_makes_roll_correctly(self):
        dice_roller = DiceRoller()
        results = dice_roller.roll_dice("2d4")
        self.assertEqual(len(results), 2)
        for value in results:
            self.assertGreaterEqual(value, 1)
            self.assertLessEqual(value, 4)

    @patch('random.randint')
    def test_confrontation_dice_d10(self, mock_randint):
        dice_roller = DiceRoller()
        mock_randint.side_effect = [10, 5, 6, 1]
        winner = dice_roller.roll_confrontation_dice("Alice", "Bob", 0, 2, 2)
        self.assertIn("Alice", winner)

    @patch('random.randint')
    def test_confrontation_dice_d20(self, mock_randint):
        dice_roller = DiceRoller()
        mock_randint.side_effect = [15, 12]
        winner = dice_roller.roll_confrontation_dice("Alice", "Bob", 1)
        self.assertIn("Alice", winner)

    @patch('random.randint')
    def test_confrontation_dice_d100(self, mock_randint):
        dice_roller = DiceRoller()
        mock_randint.side_effect = [40, 75]
        winner = dice_roller.roll_confrontation_dice("Alice", "Bob", 2)
        self.assertIn("Alice", winner)

    @patch('random.randint')
    def test_difficulty_dice_d10_success(self, mock_randint):
        dice_roller = DiceRoller()
        mock_randint.side_effect = [10, 6]
        result = dice_roller.roll_difficulty_dice(0, 2, 2)
        self.assertTrue(result)

    @patch('random.randint')
    def test_difficulty_dice_d20_fail(self, mock_randint):
        dice_roller = DiceRoller()
        mock_randint.return_value = 8
        result = dice_roller.roll_difficulty_dice(1, 10)
        self.assertFalse(result)

    @patch('random.randint')
    def test_difficulty_dice_d100_success(self, mock_randint):
        dice_roller = DiceRoller()
        mock_randint.return_value = 43
        result = dice_roller.roll_difficulty_dice(2, 50)
        self.assertTrue(result)
