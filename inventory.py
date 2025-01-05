import logging
from armor_weapon import Armor, Weapon  # Import Armor and Weapon classes

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(message)s')

class Inventory:
    def __init__(self):
        self.items = []
        self.equipped_items = {"Armor": None, "Weapon": None}
        logging.debug("Initialized Inventory")

    def add_item(self, item):
        self.items.append(item)
        logging.debug(f"Added item to inventory: {item}")

    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)
            logging.debug(f"Removed item from inventory: {item}")

    def show_inventory(self):
        logging.debug("Showing Inventory")
        print("Inventory:")
        for i, item in enumerate(self.items, start=1):
            print(f"{i}. {item}")
        print("Equipped Items:")
        for slot, item in self.equipped_items.items():
            if item:
                print(f"{slot}: {item}")
            else:
                print(f"{slot}: None")

    def equip_item(self, item):
        if isinstance(item, Weapon):
            self.equipped_items["Weapon"] = item
            logging.debug(f"Equipped {item.name} as Weapon")
            print(f"Equipped {item.name} as Weapon.")
        elif isinstance(item, Armor):
            self.equipped_items["Armor"] = item
            logging.debug(f"Equipped {item.name} as Armor")
            print(f"Equipped {item.name} as Armor.")
        else:
            logging.debug(f"Item cannot be equipped: {item}")
            print("This item cannot be equipped.")

    def use_item(self, index, character):
        item = self.items.pop(index)
        logging.debug(f"Used item from inventory: {item}")
        if item == "MP Potion":
            character.mp = min(character.max_mp, character.mp + 20)
            print(f"\nYou used an MP Potion and restored 20 MP. Current MP: {character.mp}")
        elif item == "SP Potion":
            character.sp = min(character.max_sp, character.sp + 20)
            print(f"\nYou used an SP Potion and restored 20 SP. Current SP: {character.sp}")
        else:
            print(f"Used {item}.")

    def draw(self, screen):
        # Draw inventory items on the screen
        pass