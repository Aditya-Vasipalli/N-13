import logging
from character_creation import create_character
from combat_system import win_or_loss, display_bars
from enemies import select_enemy, display_enemy_details, adjust_enemy_stats, enemy_skills, enemies
from inventory import Inventory  # Import Inventory class

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    logging.info("Welcome to the RPG Game!")
    character = create_character()
    
    while True:
        print("\nMain Menu")
        print("1. Start Combat")
        print("2. Equip Weapon")
        print("3. Equip Armor")
        print("4. View Inventory")
        print("5. Exit")
        choice = input("Select an option: ")

        if choice == '1':
            start_combat(character)
        elif choice == '2':
            character.equip_weapon()
        elif choice == '3':
            character.equip_armor()
        elif choice == '4':
            view_inventory(character)
        elif choice == '5':
            logging.info("Exiting the game.")
            break
        else:
            print("Invalid choice. Please select again.")

def start_combat(character):
    logging.info("Starting combat")
    enemy = select_enemy("Goblin")  # Example enemy
    if enemy:
        level = character.level  # Match enemy level to character level
        adjust_enemy_stats(enemy, level)
        display_enemy_details(enemy)
        result = win_or_loss(character, enemy)
        logging.info(result)
        print(result)
    else:
        logging.error("Enemy not found")

def view_inventory(character):
    logging.info("Viewing inventory")
    character.inventory.show_inventory()

def view_enemies():
    logging.info("Viewing all enemies")
    for enemy in enemies:
        if enemy:
            level = 1
            logging.debug(f"Adjusting stats for enemy: {enemy['name']} at level {level}")
            adjust_enemy_stats(enemy, level)
            logging.debug(f"Displaying details for enemy: {enemy['name']}")
            display_enemy_details(enemy)
            logging.debug(f"Displaying skills for enemy: {enemy['name']}")
            print("Enemy Skills:")
            for skill in enemy_skills:
                logging.debug(f"Skill: {skill}, Description: {enemy_skills[skill]['description']}")
                print(f"- {skill}: {enemy_skills[skill]['description']}")


if __name__ == "__main__":
    logging.info("Starting debug script")
    main()
    logging.info("Finished debug script")
