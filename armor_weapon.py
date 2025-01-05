import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class Armor:
    def __init__(self, name, defense, weight, description):
        self.name = name
        self.defense = defense
        self.weight = weight
        self.description = description

    def __str__(self):
        return f"{self.name}: Defense={self.defense}, Weight={self.weight}, Description={self.description}"

class Weapon:
    def __init__(self, name, attack, weight, description):
        self.name = name
        self.attack = attack
        self.weight = weight
        self.description = description

    def __str__(self):
        return f"{self.name}: Attack={self.attack}, Weight={self.weight}, Description={self.description}"

# List of armor options
armor_options = [
    Armor("Leather Armor", 5, 2, "Basic armor made of leather."),
    Armor("Chainmail Armor", 10, 5, "Armor made of interlocking metal rings."),
    Armor("Plate Armor", 20, 10, "Heavy armor made of metal plates.")
]

# List of weapon options
weapon_options = [
    Weapon("Sword", 10, 3, "A basic sword."),
    Weapon("Axe", 15, 5, "A heavy axe."),
    Weapon("Bow", 8, 2, "A long-range bow.")
]

# Function to display armor options
def display_armor_options():
    print("Available Armor:")
    for armor in armor_options:
        print(armor)

# Function to display weapon options
def display_weapon_options():
    print("Available Weapons:")
    for weapon in weapon_options:
        print(weapon)