import re

class Feat:
    def __init__(self, name, description, parsed_description, used_attributes, attribute_paths, dice, numbers):
        self.name = name
        self.description = description
        self.parsed_description = parsed_description
        self.used_attributes = used_attributes
        self.attribute_paths = attribute_paths
        self.dice = dice
        self.numbers = numbers

class FeatParser:
    def __init__(self, character_data):
        self.character_data = character_data
        self.attribute_map = self.create_attribute_map()

    def create_attribute_map(self):
        attribute_map = {}
        for key, value in self.character_data.items():
            if isinstance(value, (int, float)):
                attribute_map[key] = {'value': value, 'path': key}
            elif isinstance(value, dict):
                for subkey, subvalue in value.items():
                    natural_name = f"{subkey}"
                    attribute_map[natural_name] = {
                        'value': subvalue,
                        'path': f"{key}.{subkey}"
                    }
        return attribute_map

    def extract_dice_and_numbers(self, description):
        dice_pattern = r'(\d+d\d+(?:[+-]\d+)?)'
        dice_matches = re.findall(dice_pattern, description)
        number_pattern = r'(?<!\d[d+-])\b(\d+)\b(?![d+-]\d)'
        number_matches = re.findall(number_pattern, description)
        return {
            'dice': dice_matches,
            'numbers': [int(n) for n in number_matches]
        }

    def validate_description(self, description):
        used_attributes = [attr for attr in self.attribute_map if attr in description]
        if not used_attributes:
            return False, "Description must reference at least one attribute", []
        return True, "", used_attributes

    def parse_description(self, description, used_attributes):
        attr_values = {
            attr: self.attribute_map[attr]['value']
            for attr in used_attributes
        }

        calc_data = self.extract_dice_and_numbers(description)
        parsed_desc = description
        for attr, value in attr_values.items():
            parsed_desc = parsed_desc.replace(attr, str(value))

        return {
            'original_description': description,
            'parsed_description': parsed_desc,
            'used_attributes': used_attributes,
            'attribute_paths': [
                self.attribute_map[attr]['path'] for attr in used_attributes
            ],
            'dice': calc_data['dice'],
            'numbers': calc_data['numbers']
        }

    def create_feat(self, name, description):
        name = name.strip()
        description = description.strip()

        if not name or not description:
            raise ValueError("Both name and description must be provided.")

        valid, error_msg, used_attributes = self.validate_description(description)
        if not valid:
            raise ValueError(error_msg)

        feat_data = self.parse_description(description, used_attributes)

        return Feat(
            name=name,
            description=feat_data['original_description'],
            parsed_description=feat_data['parsed_description'],
            used_attributes=feat_data['used_attributes'],
            attribute_paths=feat_data['attribute_paths'],
            dice=feat_data['dice'],
            numbers=feat_data['numbers']
        )
