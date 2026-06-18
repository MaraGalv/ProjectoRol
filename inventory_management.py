from equipment import Equipment
from feat_parser import FeatParser


class InventoryManagement:
    def __init__(self):
        self.equipment = []
    
    def add_equipment(self, equipment_data):
        """
        Add equipment to the character's inventory.
        
        Args:
            equipment_data: JSON-like dict containing equipment details
        """
        eq = Equipment()
        eq.create_equipment(equipment_data)
        self.equipment.append((eq, False))
    
    def remove_equipment(self, equipment_name):
        """
        Remove equipment from the character's inventory.
        
        Args:
            equipment_name: A string with the equipment name
        """
        self.unequip(equipment_name)
        equipment_tuple = self.get_equipment(equipment_name)
        if equipment_tuple:
            self.equipment.remove(equipment_tuple)
    
    def get_equipment(self, equipment_name):
        """
        Get equipment by name.
        
        Args:
            equipment_name: The name of the equipment
            
        Returns:
            tuple: (Equipment, is_equipped) or None if not found
        """
        for eq in self.equipment:
            if eq[0].name == equipment_name:
                return eq
        return None
    
    def equip(self, equipment_name, stats_manager):
        """
        Equip a piece of equipment if requisites are met and slot is available.
        
        Args:
            equipment_name: The name of the equipment to equip
            stats_manager: An instance of the StatManager of the Character
            
        Returns:
            A tuple (bool: True if equipped successfully, False otherwise, list: a list of Feat objects to add to Character)
        """
        eq = self.get_equipment(equipment_name)
        if not eq:
            return False, None
        if eq[1]:
            return True, None  # Already equipped
        
        if not self._check_requisites(eq[0], stats_manager):
            return False, None
        
        if not self._check_slot_availability(eq[0], eq):
            return False, None
        
        feats_to_add = self._apply_equipment_effects(eq[0], stats_manager)
        eq = (eq[0], True)  # Mark as equipped
        
        # Update the equipment list
        for i, equipment_tuple in enumerate(self.equipment):
            if equipment_tuple[0].name == equipment_name:
                self.equipment[i] = eq
                break
        
        return True, feats_to_add
    
    def unequip(self, equipment_name, stats_manager, feats):
        """
        Unequip a piece of equipment and remove its effects.
        
        Args:
            equipment_name: The name of the equipment to unequip
            stats_manager: An instance of the StatManager of the Character
            feats: A list of feats of the Character
        Returns:
            A tuple (bool: True if unequipped successfully, False otherwise, list: a list of Feat objects to remove from Character)
        """
        eq = self.get_equipment(equipment_name)
        if not eq or not eq[1]:
            return False, None
        
        feats_to_remove = self._remove_equipment_effects(eq[0], stats_manager, feats)
        eq = (eq[0], False)  # Mark as unequipped
        
        # Update the equipment list
        for i, equipment_tuple in enumerate(self.equipment):
            if equipment_tuple[0].name == equipment_name:
                self.equipment[i] = eq
                break
        
        return True, feats_to_remove
    
    def _check_requisites(self, equipment, stats_manager):
        """
        Check if character meets equipment requisites.
        
        Args:
            equipment: Equipment object to check
            stats_manager: An instance of the StatManager of the Character
            
        Returns:
            bool: True if requisites are met
        """
        for stat_name, min_value in equipment.requisites.items():
            stat = stats_manager.get_stat(stat_name)
            if not stat or stat.current < min_value:
                return False
        return True
    
    def _check_slot_availability(self, equipment, current_eq):
        """
        Check if equipment slot is available.
        
        Args:
            equipment: Equipment object to check
            current_eq: Current equipment tuple
            
        Returns:
            bool: True if slot is available
        """
        for e in self.equipment:
            if e[1] and e[0].slot == equipment.slot and e != current_eq:
                return False
        return True
    
    def _apply_equipment_effects(self, equipment, stats_manager):
        """
        Apply equipment bonuses and feats to character.
        
        Args:
            equipment: Equipment object to apply effects from
            stats_manager: An instance of the StatManager of the Character
        
        Returns:
            feats_to_add: A list of feats to add to the Character
        """
        self._apply_stat_bonuses(equipment, stats_manager)
        feats_to_add = self._apply_equipment_feats(equipment, stats_manager)
        return feats_to_add
    
    def _remove_equipment_effects(self, equipment, stats_manager, feats):
        """
        Remove equipment bonuses and feats from character.
        
        Args:
            equipment: Equipment object to remove effects from
            stats_manager: An instance of the StatManager of the Character
            feats: A list of feats of the Character
        
        Returns:
            feats_to_remove: A list of feats to remove from the Character
        """
        self._remove_stat_bonuses(equipment, stats_manager)
        feats_to_remove = self._remove_equipment_feats(equipment, feats)
        return feats_to_remove
    
    def _apply_stat_bonuses(self, equipment, stats_manager):
        """Apply stat bonuses from equipment.
        
        Args:
            equipment: Equipment object to remove effects from
            stats_manager: An instance of the StatManager of the Character
        """
        for stat_name, bonus in equipment.bonuses.items():
            stat = stats_manager.get_stat(stat_name)
            if stat:
                stat.current += bonus
                stat.base += bonus
    
    def _remove_stat_bonuses(self, equipment, stats_manager):
        """Remove stat bonuses from equipment.
        
        Args:
            equipment: Equipment object to remove effects from
            stats_manager: An instance of the StatManager of the Character
        """
        for stat_name, bonus in equipment.bonuses.items():
            stat = stats_manager.get_stat(stat_name)
            if stat:
                stat.current -= bonus
                stat.base -= bonus
    
    def _apply_equipment_feats(self, equipment, stats_manager):
        """Apply feats from equipment.
        
        Args:
            equipment: Equipment object to remove effects from
            stats_manager: An instance of the StatManager of the Character

        Returns:
            feats_to_add: A list of feats to add to the Character
        """
        feats_to_add = []
        for feat_name, feat_description in equipment.feats.items():
            feat_parser = FeatParser(stats_manager.get_stats_dict())
            try:
                feat = feat_parser.create_feat(f"{equipment.name} - {feat_name}", feat_description)
                feats_to_add.append(feat)
            except ValueError:
                raise ValueError(f"Failed to create feat {feat_name} for equipment {equipment.name}")
        return feats_to_add
    
    def _remove_equipment_feats(self, equipment, feats):
        """Remove feats from equipment.
        Args:
            equipment: Equipment object to remove effects from
            feats: A list of feats of the Character 

        Returns:
            feats_to_remove: A list of feats to remove from the Character
        """
        feats_to_remove = []
        for feat in feats:
            if feat.name.startswith(f"{equipment.name} - "):
                feats_to_remove.append(feat.name)
        return feats_to_remove