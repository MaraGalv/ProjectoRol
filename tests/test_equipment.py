import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from equipment import Equipment

class TestEquipment(unittest.TestCase):
    def test_equipment_is_created_correctly(self):
        weapon_data = {"name": "TestWeapon", "description": "Test Description", "slot": "main hand", "requisites": {"Fuerza": 2, "Destreza": 1}, "bonuses": {"Armas C.C.": 1}, "damage": "1d6", "feats": {"PowerStrike" : "Golpea con 2d6 + Fuerza"}}
        weapon = Equipment()
        weapon.create_equipment(weapon_data)
        self.assertEqual(weapon.name, "TestWeapon")
        self.assertEqual(weapon.description, "Test Description")
        self.assertEqual(weapon.slot, "main hand")
        self.assertDictEqual(weapon.requisites, {"Fuerza": 2, "Destreza": 1})
        self.assertDictEqual(weapon.bonuses, {"Armas C.C.": 1})
        self.assertEqual(weapon.damage, "1d6")
        self.assertDictEqual(weapon.feats, {"PowerStrike" : "Golpea con 2d6 + Fuerza"})