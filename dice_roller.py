import random

class DiceRoller:
    def __init__(self):
        pass
    
    def roll_base_dice(self, dice_system, num_dice=1):
        """
        Rolls the base dice according to the game system's dice_system.
        Only d10 (dice_system=0) supports rolling multiple dice.
        
        Args:
            dice_system (int): The dice system (0=d10, 1=d20, 2=d100).
            num_dice (int, optional): Number of dice (only for d10). Defaults to 1.
        
        Returns:
            list: List of roll results.
        
        Raises:
            ValueError: If dice_system is invalid.
        """
        if dice_system == 0:  # d10: Can roll multiple
            return [random.randint(1, 10) for _ in range(num_dice)]
        elif dice_system == 1:  # d20: Always 1 die
            return random.randint(1, 20)
        elif dice_system == 2:  # d100: Always 1 die
            return random.randint(1, 100)
        else:
            raise ValueError(f"Invalid dice_system: {dice_system}")
    
    def roll_dice(self, dice_str):
        """
        Rolls dice based on a string in "xdy" format (e.g., "2d6", "d20").
        
        Args:
            dice_str (str): Dice notation, where x is number of dice (optional, defaults to 1),
                            and y is number of faces.
        
        Returns:
            list: List of individual roll results.
        
        Raises:
            ValueError: If the format is invalid.
        """
        if 'd' not in dice_str:
            raise ValueError("Invalid dice string format: must contain 'd'")
        
        parts = dice_str.split('d')
        if len(parts) != 2:
            raise ValueError("Invalid dice string format: must be 'xdy' or 'dy'")
        
        try:
            if parts[0] == '':
                num_dice = 1
            else:
                num_dice = int(parts[0])
            faces = int(parts[1])
        except ValueError:
            raise ValueError("Invalid dice string: x and y must be integers")
        
        if num_dice < 1 or faces < 1:
            raise ValueError("Number of dice and faces must be at least 1")
        
        return [random.randint(1, faces) for _ in range(num_dice)]

    def _calculate_d10_successes(self, rolls):
            """
            Helper method to calculate successes for d10 rolls.
            - 5+ = 1 success
            - 10 = 2 successes total (1 base + 1 extra)
            - 1 = -1 success
            Private method for internal use in confrontation and difficulty rolls.
            
            Args:
                rolls (list): List of d10 roll results.
            
            Returns:
                int: Total successes (can be negative).
            """
            successes = 0
            for roll in rolls:
                if roll == 10:
                    successes += 2  # Extra success for 10
                elif roll >= 5:
                    successes += 1
                elif roll == 1:
                    successes -= 1
            return successes
    
    def roll_confrontation_dice(self, char1_name, char2_name, dice_system, char1_dice=1, char2_dice=1):
        """
        Simulates a confrontation roll between two characters.
        - For d10 (0): Rolls multiple d10s, calculates successes (5+ = 1, 10 = 2, 1 = -1). Higher successes win.
        - For d20 (1): Rolls 1d20 each. Higher roll wins.
        - For d100 (2): Rolls 1d100 each. Lower roll wins.
        On a tie, automatically re-rolls until a winner is determined (up to 10 re-rolls, then declares a tie).
        
        Args:
            char1_name (str): Name of the first character.
            char2_name (str): Name of the second character.
            dice_system (int): The dice system (0=d10, 1=d20, 2=d100).
            char1_dice (int, optional): Number of d10s for char1 (only for d10). Defaults to 1.
            char2_dice (int, optional): Number of d10s for char2 (only for d10). Defaults to 1.
        
        Returns:
            str: Result message, e.g., "Alice wins!" or "It's a tie after multiple rolls!".
        
        Raises:
            ValueError: If inputs are invalid.
        """
        if dice_system not in [0, 1, 2]:
            raise ValueError("Invalid dice_system: must be 0 (d10), 1 (d20), or 2 (d100).")
        if char1_dice < 1 or char2_dice < 1:
            raise ValueError("Number of dice must be at least 1.")

        while (True):
            if dice_system == 0:  # d10: Compare successes
                char1_rolls = self.roll_base_dice(dice_system, char1_dice)
                char2_rolls = self.roll_base_dice(dice_system, char2_dice)
                char1_score = self._calculate_d10_successes(char1_rolls)
                char2_score = self._calculate_d10_successes(char2_rolls)
                if char1_score > char2_score:
                    return f"{char1_name} wins!"
                elif char2_score > char1_score:
                    return f"{char2_name} wins!"
            elif dice_system == 1:  # d20: Higher wins
                char1_roll = self.roll_base_dice(dice_system)
                char2_roll = self.roll_base_dice(dice_system)
                if char1_roll > char2_roll:
                    return f"{char1_name} wins!"
                elif char2_roll > char1_roll:
                    return f"{char2_name} wins!"
            elif dice_system == 2:  # d100: Lower wins
                char1_roll = self.roll_base_dice(dice_system)
                char2_roll = self.roll_base_dice(dice_system)
                if char1_roll < char2_roll:
                    return f"{char1_name} wins!"
                elif char2_roll < char1_roll:
                    return f"{char2_name} wins!"
    
    def roll_difficulty_dice(self, dice_system, difficulty, num_dice=1):
        """
        Rolls dice against a difficulty and checks for success.
        - For d10 (0): Rolls multiple d10s, calculates successes (5+ = 1, 10 = 2, 1 = -1). Success if successes >= difficulty.
        - For d20 (1): Rolls 1d20. Success if roll >= difficulty.
        - For d100 (2): Rolls 1d100. Success if roll <= difficulty.
        
        Args:
            dice_system (int): The dice system (0=d10, 1=d20, 2=d100).
            difficulty (int): The difficulty number to beat.
            num_dice (int, optional): Number of d10s (only for d10). Defaults to 1.
        
        Returns:
            bool: True if successful, False otherwise.
        
        Raises:
            ValueError: If inputs are invalid.
        """
        if dice_system not in [0, 1, 2]:
            raise ValueError("Invalid dice_system: must be 0 (d10), 1 (d20), or 2 (d100).")
        if num_dice < 1:
            raise ValueError("Number of dice must be at least 1.")
        if difficulty < 0:
            raise ValueError("Difficulty must be non-negative.")
        
        if dice_system == 0:  # d10: Check successes >= difficulty
            rolls = self.roll_base_dice(dice_system, num_dice)
            successes = self._calculate_d10_successes(rolls)
            return successes >= difficulty
        elif dice_system == 1:  # d20: Roll >= difficulty
            roll = self.roll_base_dice(dice_system)
            return roll >= difficulty
        elif dice_system == 2:  # d100: Roll <= difficulty
            roll = self.roll_base_dice(dice_system)
            return roll <= difficulty