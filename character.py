from game_system import GameSystem
from inventory_management import InventoryManagement
from stats_management import StatsManagement

class Character:
    def __init__(self, stats_data=None, sheet_model_path=None):
        self.name = ""
        self.owner = ""
        self.info = dict()
        self.level = 1
        self.experience = 0
        self.experience_to_next_level = 100
        self.game_system = None
        self.sheet_model = None
        
        # Initialize management classes
        self.stats_manager = StatsManagement()
        self.inventory_manager = InventoryManagement()
        
        self.feats = []
        
        # Initialize stats through the stats manager
        self.stats_manager.initialize_stats(stats_data)

        if sheet_model_path:
            self.parse_sheet_model(sheet_model_path)
        
        # Check if stats are valid based on the game system
        if self.game_system:
            self.stats_manager.check_if_stats_are_valid(self.game_system)

    def parse_sheet_model(self, sheet_model_path):
        # Create GameSystem instance and load from file
        self.game_system = GameSystem()
        self.game_system.load_system(sheet_model_path)
        
        self.stats_manager.create_stats_from_model(self.game_system)
        self.create_info_from_model()

    def create_info_from_model(self):
        if not self.game_system or not self.game_system.info:
            return
        self.info = self.game_system.info

    def add_feat(self, feat):
        self.feats.append(feat)
        
    def remove_feat(self, feat_name):
        for i, feat in enumerate(self.feats):
            if feat.name == feat_name:
                return self.feats.pop(i)
        return None
    
    def get_feat(self, feat_name):
        for feat in self.feats:
            if feat.name == feat_name:
                return feat
        return None
    
    def has_feat(self, feat_name):
        return any(feat.name == feat_name for feat in self.feats)

    def can_level_up(self) -> bool:
        # If exp_style is 1, don't allow level up
        if self.game_system and self.game_system.exp_style == 1:
            return False
        return self.experience >= self.experience_to_next_level

    def prepare_for_level_up(self) -> None:
        self.stats_manager.prepare_for_level_up(self.game_system)

    def level_up(self) -> None:
        if not self.can_level_up():
            raise ValueError("Character does not have enough experience to level up.")
            
        # If exp_style is 1, don't allow level up
        if self.game_system and self.game_system.exp_style == 1:
            raise ValueError("This game system doesn't support traditional level ups.")

        self.level += 1
        self.experience -= self.experience_to_next_level
        self.experience_to_next_level = int(self.experience_to_next_level * 1.5)

        self.stats_manager.finalize_level_up()
    
    def set_name(self, name):
        self.name = name

    def set_owner(self, owner):
        self.owner = owner

    def calculate_data_position(self, sheet_size, margin):
        """
        Calculate the position of character data elements on a character sheet.
        Args:
            sheet_size (tuple): (width, height) in pixels
            margin (tuple): (margin_w, margin_h) in pixels
        Returns:
            dict: mapping of labels to (x, y) positions (rounded ints)
        """
        width, height = sheet_size
        margin_w, margin_h = margin

        available_width = width - 2 * margin_w
        available_height = height - 2 * margin_h

        positions = {}

        all_rows = []  # List of rows. Each row is a list of (label) strings.
        vertical_elements = 0
        # Title (game name)
        all_rows.append([self.game_system.name])
        vertical_elements += 1

        # INFO SECTION
        if self.info:
            info_items = [f"{k}: {v}" for k, v in self.info.items()]
            all_rows.append(info_items)
            vertical_elements += 1
            
        # STATS SECTION
        max_vertical_stats = 0
        if self.stats_manager.stats:
            # Organize stats by top-level category and possible subcategories
            category_rows = {}
            stats = {}
            last_category = ""
            category_rows["Uncategorized"] = []
            for stat in self.stats_manager.stats:
                parts = stat.name.split('.')
                if len(parts) == 1:
                    category_rows["Uncategorized"].append(parts)
                for index, part in enumerate(parts):
                    if index == 0:
                        if [part] not in all_rows:
                            all_rows.append([part])
                        last_category = part
                    elif index == len(parts) - 1:
                        if last_category not in stats:
                            stats[last_category] = []
                        stats[last_category].append(part)   
                    else:
                        if index not in category_rows:
                            category_rows[index] = []
                        if part not in category_rows[index]:
                            category_rows[index].append(part)
                        last_category = part

            vertical_elements += max_vertical_stats
            last_row = None
            for key, value in category_rows.items():
                if key == "Uncategorized":
                    if value != []:
                        last_row = value
                else: 
                    all_rows.append(value)
            stat_rows = {}
            max_horizontal_items = 0
            for index, item in stats.items():
                for i in range(len(item)):
                    if i not in stat_rows:
                        stat_rows[i] = []
                    stat_rows[i].append(item[i])
                    if i + 1 > max_horizontal_items:
                        max_horizontal_items += 1
            for key, value in stat_rows.items():
                while(len(value) < max_horizontal_items):
                    value.append("")
                all_rows.append(value)
            if last_row is not None:
                all_rows.append(last_row)

        # FEATS SECTION
        if self.feats:
            all_rows.append([feat.name for feat in self.feats])

        # Now place each row
        row_count = len(all_rows)
        row_step = available_height / max(row_count - 1, 1)
        y = margin_h
        for row_index, row in enumerate(all_rows):
            col_count = len(row)
            col_step = available_width / max(col_count - 1, 1)
            x = margin_w if col_count > 1 else width / 2

            for col_index, item in enumerate(row):
                if not item:
                    continue  # skip blanks   
                positions[item] = (round(x), round(y))
                x = x + col_step 
            y = y + row_step
        return positions

    # Delegate equipment methods to inventory manager
    def add_equipment(self, equipment_data):
        """
        Add equipment to the character's inventory.
        
        Args:
            equipment_data: JSON-like dict containing equipment details
        """
        self.inventory_manager.add_equipment(equipment_data)

    def remove_equipment(self, equipment_name):
        """
        Remove equipment from the character's inventory.
        
        Args:
            equipment_name: A string with the equipment name
        """
        self.inventory_manager.remove_equipment(equipment_name)

    def get_equipment(self, equipment_name):
        """
        Get equipment by name.
        
        Args:
            equipment_name: The name of the equipment
            
        Returns:
            tuple: (Equipment, is_equipped) or None if not found
        """
        return self.inventory_manager.get_equipment(equipment_name)

    def equip(self, equipment_name):
        """
        Equip a piece of equipment if requisites are met and slot is available.
        
        Args:
            equipment_name: The name of the equipment to equip
            
        Returns:
            bool: True if equipped successfully, False otherwise
        """
        is_equipped, feats_to_add = self.inventory_manager.equip(equipment_name, self.stats_manager)
        for feat in feats_to_add:
            self.add_feat(feat)
        return is_equipped

    def unequip(self, equipment_name):
        """
        Unequip a piece of equipment and remove its effects.
        
        Args:
            equipment_name: The name of the equipment to unequip
            
        Returns:
            bool: True if unequipped successfully, False otherwise
        """
        is_unequipped, feats_to_add = self.inventory_manager.unequip(equipment_name, self.stats_manager, self.feats)
        for feat in feats_to_add:
            self.remove_feat(feat)
        return is_unequipped

    # Delegate stats methods to stats manager
    def get_stat(self, stat_name):
        """
        Get a stat by name.
        
        Args:
            stat_name: The name of the stat
            
        Returns:
            Stat: The stat object or None if not found
        """
        return self.stats_manager.get_stat(stat_name)

    def get_stats_dict(self):
        """
        Get a nested dictionary representation of the character's stats.
        
        Returns:
            dict: Nested dict of stat names and values
        """
        return self.stats_manager.get_stats_dict()

    def calculate_stat_cost(self, stat):
        """
        Calculates the cost of a stat to upgrade.
        
        Args:
            stat: The Stat object to upgrade
            
        Returns:
            int: The cost in experience points of upgrading the stat
        """
        return self.stats_manager.calculate_stat_cost(stat, self.game_system)

    def is_stat_upgradable(self, stat):
        """
        Check if a stat can be upgraded with the current experience points.
        
        Args:
            stat: The Stat object to check
            
        Returns:
            bool: True if the stat can be upgraded, False otherwise
        """
        return self.stats_manager.is_stat_upgradable(stat, self.game_system, self.experience)

    def upgrade_stat(self, stat):
        """
        Upgrade a stat using experience points.
        
        Args:
            stat: The Stat object to upgrade
            
        Returns:
            bool: True if the upgrade was successful, False otherwise
        """
        return self.stats_manager.upgrade_stat(stat, self.game_system, self.experience)

    def get_stat_category(self, stat_name):
        """
        Helper method to find the category of a stat based on its name.
        
        Args:
            stat_name: The full name of the stat (e.g., "Atributos.Fisicos.Fuerza")
            
        Returns:
            str: The category name or None if not found
        """
        return self.stats_manager.get_stat_category(stat_name, self.game_system)