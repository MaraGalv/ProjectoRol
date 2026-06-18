import json
import os

class GameSystem:
    def __init__(self, owner=None):
        self.owner = owner
        self.name = ""
        self.exp_style = None  # 0 = exp is for level up, 1 = exp is for upgrading stats
        self.stat_style = None  # 0 = numerical, 1 = dots
        self.dice_system = None  # 0 = d10, 1 = d20, 2 = d100
        self.favorited_style = None  # 0 = not used, 1 = add 1 per level up
        self.stats = {}  # A dict of stats
        self.info = {}  # A dict
        self.exp_cost = {}  # Dictionary mapping stat categories to their exp cost formula

    def load_system(self, file_path):
        """Load game system data from a JSON file."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Game system file not found: {file_path}")
        
        with open(file_path, 'r') as file:
            data = json.load(file)
            
        self.name = data.get("game_name", "")
        self.exp_style = data.get("exp_style", None)
        self.stat_style = data.get("stat_style", None)
        self.dice_system = data.get("dice_system", None)
        self.favorited_style = data.get("favorited_style", None)
        self.stats = data.get("stats", {})
        self.info = data.get("info", {})
        self.exp_cost = data.get("exp_cost", {})

    def save_system(self, file_path):
        """Save game system data to a JSON file."""
        data = {
            "game_name": self.name,
            "exp_style": self.exp_style,
            "stat_style": self.stat_style,
            "dice_system": self.dice_system,
            "favorited_style": self.favorited_style,
            "stats": self.stats,
            "info": self.info,
            "exp_cost": self.exp_cost
        }
        
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

    def is_owner(self, username):
        """Checks if a user is the owner."""
        if username == self.owner:
            return True
        else:
            raise ValueError(f"User '{username}' is not the owner of the GameSystem.")
        
    def set_name(self, name, username):
        """Set the game system name."""
        self.is_owner(username)
        self.name = name

    def set_owner(self, owner, username):
        """Set the game system owner."""
        self.is_owner(username)
        self.owner = owner

    def set_exp_style(self, exp_style, username):
        """Set the experience style (0 or 1)."""
        self.is_owner(username)
        if exp_style not in [0, 1]:
            raise ValueError("exp_style must be 0 or 1")
        self.exp_style = exp_style

    def set_stat_style(self, stat_style, username):
        """Set the stat style (0 or 1)."""
        self.is_owner(username)
        if stat_style not in [0, 1]:
            raise ValueError("stat_style must be 0 or 1")
        self.stat_style = stat_style

    def set_dice_system(self, dice_system, username):
        """Set the dice system (0, 1, or 2)."""
        self.is_owner(username)
        if dice_system not in [0, 1, 2]:
            raise ValueError("dice_system must be 0, 1, or 2")
        self.dice_system = dice_system

    def set_favorited_style(self, favorited_style, username):
        """Set the favorited style (0 or 1)."""
        self.is_owner(username)
        if favorited_style not in [0, 1]:
            raise ValueError("favorited_style must be 0 or 1")
        self.favorited_style = favorited_style

    def add_stat(self, stat_path, default_value, username):
        """
        Add a stat to the system.
        
        Args:
            stat_path: Dot-separated path for the stat (e.g., "Atributos.Fisicos.Fuerza")
            default_value: Default value for the stat
        """
        self.is_owner(username)
        parts = stat_path.split('.')
        current = self.stats
        
        # Navigate/create the nested structure
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]
        
        # Set the final stat value
        current[parts[-1]] = default_value

    def remove_stat(self, stat_path, username):
        """
        Remove a stat from the system.
        
        Args:
            stat_path: Dot-separated path for the stat to remove
            
        Returns:
            bool: True if stat was removed, False if not found
        """
        self.is_owner(username)
        parts = stat_path.split('.')
        current = self.stats
        
        # Navigate to the parent of the stat to remove
        try:
            for part in parts[:-1]:
                current = current[part]
            
            if parts[-1] in current:
                del current[parts[-1]]
                return True
            return False
        except KeyError:
            return False

    def update_stat_value(self, stat_path, new_value, username):
        """
        Update the default value of a stat.
        
        Args:
            stat_path: Dot-separated path for the stat
            new_value: New default value for the stat
            
        Returns:
            bool: True if updated, False if stat not found
        """
        self.is_owner(username)
        parts = stat_path.split('.')
        current = self.stats
        
        try:
            for part in parts[:-1]:
                current = current[part]
            
            if parts[-1] in current:
                current[parts[-1]] = new_value
                return True
            return False
        except KeyError:
            return False

    def add_info_field(self, key, value, username):
        """Add or update an info field."""
        self.is_owner(username)
        self.info[key] = value

    def remove_info_field(self, key, username):
        """Remove an info field."""
        self.is_owner(username)
        if key in self.info:
            del self.info[key]
            return True
        return False

    def set_exp_cost(self, category, cost_formula, username):
        """
        Set the experience cost formula for a stat category.
        
        Args:
            category: The stat category name
            cost_formula: The cost formula (e.g., "10", "5*", etc.)
        """
        self.is_owner(username)
        self.exp_cost[category] = cost_formula

    def remove_exp_cost(self, category, username):
        """Remove experience cost for a category."""
        self.is_owner(username)
        if category in self.exp_cost:
            del self.exp_cost[category]
            return True
        return False

    def get_all_stat_paths(self):
        """
        Get all stat paths in the system as a flat list.
        
        Returns:
            list: List of dot-separated stat paths
        """
        paths = []
        
        def collect_paths(current_dict, prefix=""):
            for key, value in current_dict.items():
                current_path = f"{prefix}.{key}" if prefix else key
                if isinstance(value, dict):
                    collect_paths(value, current_path)
                else:
                    paths.append(current_path)
        
        collect_paths(self.stats)
        return paths