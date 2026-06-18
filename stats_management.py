class Stat:
    def __init__(self, name, current_value, favorited=False):
        self.name = name
        self.current = current_value
        self.base = current_value
        self.favorited = favorited
        self.pending_value = current_value

    def reset_pending_value(self):
        self.pending_value = self.current
        if self.favorited:
            self.pending_value += 1

class StatsManagement:
    def __init__(self):
        self.stats = []
    
    def initialize_stats(self, stats_data=None):
        """
        Initialize stats from provided data.
        
        Args:
            stats_data: List of tuples (stat_name, stat_value, stat_favorited)
        """
        if stats_data:
            for stat_name, stat_value, stat_favorited in stats_data:
                stat = Stat(name=stat_name, current_value=stat_value, favorited=stat_favorited)
                self.stats.append(stat)
    
    def create_stats_from_model(self, game_system):
        """Create stats from the sheet model if no stats_data was provided
        
        Args:
            game_system: An instance of the Character's GameSystem
        """
        if not game_system or not game_system.stats:
            return
        
        stat_name_list = [stat.name for stat in self.stats]
        
        # Recursively process nested stats dictionary
        def process_stats_dict(stats_dict, stat_name_list, prefix=""):
            for category, value in stats_dict.items():
                if isinstance(value, dict):
                    # This is a category, recurse with updated prefix
                    new_prefix = f"{prefix}{category}." if prefix else f"{category}."
                    process_stats_dict(value, stat_name_list, new_prefix)
                else:
                    # This is an actual stat
                    stat_name = f"{prefix}{category}"
                    if stat_name not in stat_name_list:
                        stat = Stat(name=stat_name, current_value=value, favorited=False)
                        self.stats.append(stat)
                    
        process_stats_dict(game_system.stats, stat_name_list)
    
    def check_if_stats_are_valid(self, game_system):
        """Check if character has all the stats required by the game system
        
        Args:
            game_system: An instance of the Character's GameSystem

        Returns:
            bool: True if the stats required from the game_system are present, False otherwise
        """
        if not game_system or not game_system.stats:
            return True
            
        required_stats = set()
        
        # Recursively collect all required stat names
        def collect_stat_names(stats_dict, prefix=""):
            for category, value in stats_dict.items():
                if isinstance(value, dict):
                    # This is a category, recurse with updated prefix
                    new_prefix = f"{prefix}{category}." if prefix else f"{category}."
                    collect_stat_names(value, new_prefix)
                else:
                    # This is an actual stat
                    stat_name = f"{prefix}{category}"
                    required_stats.add(stat_name)
        
        collect_stat_names(game_system.stats)
        
        # Get all character stat names
        character_stat_names = {stat.name for stat in self.stats}


        # Check if all required stats are present
        return required_stats.issubset(character_stat_names)
    
    def get_stat(self, stat_name):
        """
        Get a stat by name.
        
        Args:
            stat_name: The name of the stat
            
        Returns:
            Stat: The stat object or None if not found
        """
        for stat in self.stats:
            if stat.name == stat_name:
                return stat
        return None
    
    def get_stats_dict(self):
        """
        Get a nested dictionary representation of the character's stats.
        
        Returns:
            dict: Nested dict of stat names and values
        """
        data = {}
        for stat in self.stats:
            parts = stat.name.split('.')
            current = data
            for part in parts[:-1]:
                if part not in current:
                    current[part] = {}
                current = current[part]
            current[parts[-1]] = stat.current
        return data
    
    def prepare_for_level_up(self, game_system):
        """Prepare stats for level up by resetting pending values.

        Args:
            game_system: An instance of the Character's GameSystem
        """
        if game_system and game_system.favorited_style != 1:
            return
            
        for stat in self.stats:
            stat.reset_pending_value()
    
    def finalize_level_up(self):
        """Finalize level up by applying pending values to current values."""
        for stat in self.stats:
            stat.current = stat.pending_value
            stat.base = stat.current
    
    def calculate_stat_cost(self, stat, game_system):
        """
        Calculates the cost of a stat to upgrade.
        
        Args:
            stat: The Stat object to upgrade
            game_system: An instance of the Character's GameSystem
            
        Returns:
            int: The cost in experience points of upgrading the stat
        """
        # Calculate the cost to upgrade this stat
        stat_category = self.get_stat_category(stat.name, game_system)
        cost_formula = game_system.exp_cost[stat_category]
        if cost_formula.endswith("*"):
            # Cost is a multiple of the current value
            multiplier = int(cost_formula.rstrip("*"))
            return multiplier * stat.current
        else:
            # Cost is a fixed value
            return int(cost_formula)


    def is_stat_upgradable(self, stat, game_system, experience):
        """
        Check if a stat can be upgraded with the current experience points.
        
        Args:
            stat: The Stat object to check
            game_system: An instance of the Character's GameSystem
            experience: An int representing the experience of the Character
            
        Returns:
            bool: True if the stat can be upgraded, False otherwise
        """
        # Only allow stat upgrades if exp_style is 1
        if not game_system or game_system.exp_style != 1:
            return False
            
        # If there's no exp_cost defined, stats can't be upgraded
        if not game_system.exp_cost:
            return False
            
        # Find the category for this stat
        stat_category = self.get_stat_category(stat.name, game_system)
        if not stat_category or stat_category not in game_system.exp_cost:
            return False
            
        # Check if we have enough experience
        return experience >= self.calculate_stat_cost(stat, game_system)
    
    def upgrade_stat(self, stat, game_system, experience):
        """
        Upgrade a stat using experience points.
        
        Args:
            stat: The Stat object to upgrade
            game_system: An instance of the Character's GameSystem
            experience: An int representing the experience of the Character
            
        Returns:
            bool: True if the upgrade was successful, False otherwise
            
        Raises:
            ValueError: If the stat cannot be upgraded
        """
        if not self.is_stat_upgradable(stat, game_system, experience):
            raise ValueError(f"Stat '{stat.name}' cannot be upgraded with current experience.")
            
        # Deduct experience and upgrade the stat
        experience -= self.calculate_stat_cost(stat, game_system)
        stat.current += 1
        stat.base = stat.current
        stat.pending_value = stat.current
        
        return True
    
    def get_stat_category(self, stat_name, game_system):
        """
        Helper method to find the category of a stat based on its name.
        
        Args:
            stat_name: The full name of the stat (e.g., "Atributos.Fisicos.Fuerza")
            game_system: An instance of the Character's GameSystem
            
        Returns:
            str: The category name or None if not found
        """
        if not game_system or not game_system.exp_cost:
            return None
            
        # Check if the stat name starts with any of the categories in exp_cost
        for category in game_system.exp_cost.keys():
            if stat_name == category or stat_name.startswith(f"{category}."):
                return category
                
        return None