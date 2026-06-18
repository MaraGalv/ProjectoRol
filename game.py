from character import Character
from game_system import GameSystem

class Game:
    def __init__(self, game_system, name, owner):
        if not isinstance(game_system, GameSystem):
            raise ValueError("game_system must be an instance of GameSystem")
        self.game_system = game_system
        self.name = name
        self.owner = owner
        self.users = [owner]  # List of user names, starting with the owner
        self.characters = []  # List of [character, flag] tuples
    
    def add_user(self, user_name):
        """Add a user to the game if not already present."""
        if not isinstance(user_name, str):
            raise ValueError("user_name must be a string")
        if user_name not in self.users:
            self.users.append(user_name)
    
    def add_character(self, character):
        """Add a character to the game, compute the flag, and ensure the owner is added as a user."""
        if not isinstance(character, Character):
            raise ValueError("character must be an instance of Character")
        # Compute flag: True if character's game_system matches the game's
        flag = character.game_system.__dict__ == self.game_system.__dict__
        # Add to characters list
        self.characters.append([character, flag])
        # Automatically add the character's owner as a user if not present
        if character.owner and character.owner not in self.users:
            self.users.append(character.owner)
    
    def remove_user(self, user_name):
        """Remove a user from the game (except the owner) and reassign ownership of their characters."""
        if not isinstance(user_name, str):
            raise ValueError("user_name must be a string")
        if user_name == self.owner:
            raise ValueError("The owner of the game cannot be removed")
        if user_name in self.users:
            self.users.remove(user_name)
            # Reassign ownership of any characters owned by this user to the game owner
            for char_info in self.characters:
                character = char_info[0]
                if character.owner == user_name:
                    character.set_owner(self.owner)
    
    def remove_character(self, character):
        """Remove a character from the game without affecting users."""
        if not isinstance(character, Character):
            raise ValueError("character must be an instance of Character")
        # Find and remove the matching [character, flag] tuple
        for char_info in self.characters:
            if char_info[0] == character:
                self.characters.remove(char_info)
                break