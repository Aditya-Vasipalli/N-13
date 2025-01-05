import logging
import mysql.connector
from armor_weapon import armor_options, weapon_options, Armor, Weapon
from inventory import Inventory
import pygame
import sys

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class Character:
    def __init__(self, name, char_class, stats, skills):
        self.name = name
        self.char_class = char_class
        self.stats = stats
        self.skills = skills
        self.inventory = Inventory()
        self.level = 1
        self.xp = 0
        self.hp = 100  # Default HP; you can adjust based on class
        self.max_hp = self.hp
        self.mp = self.calculate_mp()  # Calculate MP based on Intelligence
        self.sp = self.calculate_sp()  # Calculate SP based on Agility
        self.max_mp = self.mp
        self.max_sp = self.sp
        self.xp_threshold = 100  # XP required to level up
        self.stat_points = 0  # Points to assign to stats
        self.crit_chance = 0.1  # Default critical hit chance
        self.critdmg = 2 * self.stats['Strength']  # Default critical damage
        self.equipped_weapon = None
        self.equipped_armor = None
        self.lingering_effects = []
        self.money = 100  # Starting money
        self.inventory.add_item("MP Potion")
        self.inventory.add_item("MP Potion")
        self.inventory.add_item("MP Potion")
        self.inventory.add_item("SP Potion")
        self.inventory.add_item("SP Potion")
        self.inventory.add_item("SP Potion")
        logging.debug(f"Added 3 MP Potions and 3 SP Potions to {self.name}'s inventory.")
        logging.debug(f"Created Character: {self.name}, Class: {self.char_class}, Stats: {self.stats}, Skills: {self.skills}")

    def calculate_mp(self):
        base_mp = 1
        mp = base_mp + (self.stats['Intelligence'] * 5)  # Example multiplier
        logging.debug(f"Calculated MP: {mp}")
        return mp

    def calculate_sp(self):
        base_sp = 1
        sp = base_sp + (self.stats['Agility'] * 5)  # Example multiplier
        logging.debug(f"Calculated SP: {sp}")
        return sp

    def regenerate_mp(self):
        regen_amount = 3  # Example regeneration amount
        if self.mp < self.max_mp:
            self.mp = min(self.max_mp, self.mp + regen_amount)
            if self.mp < self.max_mp:
                print(f"{self.name} regenerated {regen_amount} MP. Current MP: {self.mp}")

    def regenerate_sp(self):
        regen_amount = 3  # Example regeneration amount
        if self.sp < self.max_sp:
            self.sp = min(self.max_sp, self.sp + regen_amount)
            if self.sp < self.max_sp:
                print(f"{self.name} regenerated {regen_amount} SP. Current SP: {self.sp}")

    def __str__(self):
        return f"Name: {self.name}, Class: {self.char_class}, Stats: {self.stats}, Skills: {self.skills}, HP: {self.hp}, MP: {self.mp}, SP: {self.sp}"

    def gain_xp(self, xp_gained):
        print(f"{self.name} gained {xp_gained} XP!")
        self.xp += xp_gained
        self.check_level_up()

    def check_level_up(self):
        while self.xp >= self.xp_threshold:
            self.xp -= self.xp_threshold
            self.level += 1
            self.hp += 20  # Increase HP by 20 on level up; adjust as needed
            self.max_hp = self.hp
            self.mp = self.calculate_mp()  # Recalculate MP on level up
            self.max_mp = self.mp
            self.sp = self.calculate_sp()  # Recalculate SP on level up
            self.max_sp = self.sp
            self.xp_threshold = int(self.xp_threshold * 1.5)  # Increase XP threshold for next level
            self.stat_points += 1  # Grant 1 stat point per level
            if self.level % 5 == 0:
                self.stat_points += 5  # Grant 5 additional stat points every 5 levels
                self.learn_new_move()
            logging.debug(f"{self.name} leveled up to level {self.level}!")
            print(f"{self.name} leveled up to level {self.level}!")
            print(f"HP increased to {self.hp}. MP increased to {self.mp}. SP increased to {self.sp}.")
            print(f"XP needed for next level: {self.xp_threshold}")
            print(f"You have {self.stat_points} stat points to assign.")

    def learn_skill(self, skill):
        if skill not in self.skills:
            self.skills.append(skill)
            print(f"You have learned a new skill: {skill}")
        else:
            print(f"You already know the skill: {skill}")

    def use_skill(self, skill):
        if skill in self.skills:
            print(f"You use the skill: {skill}")
            # Implement skill usage logic here
        else:
            print(f"You do not know the skill: {skill}")

    def learn_new_move(self):
        available_moves = ["Thunder Strike", "Heal", "Ice Blast", "Shadow Step"]
        print("You have the opportunity to learn a new move!")
        for i, move in enumerate(available_moves):
            print(f"{i + 1}. {move}")
        choice = int(input("Enter the number of the move you want to learn: ")) - 1
        new_move = available_moves[choice]
        if len(self.skills) >= 4:
            print("You already have 4 moves. Choose a move to forget:")
            for i, skill in enumerate(self.skills):
                print(f"{i + 1}. {skill}")
            forget_choice = int(input("Enter the number of the move you want to forget: ")) - 1
            self.skills[forget_choice] = new_move
        else:
            self.skills.append(new_move)
        print(f"You learned {new_move}!")

    def equip_weapon(self):
        print("Choose a weapon to equip:")
        for i, weapon in enumerate(weapon_options):
            print(f"{i + 1}. {weapon.name} - Attack: {weapon.attack}, Weight: {weapon.weight}, Description: {weapon.description}")
        choice = int(input("Enter the number of your choice: ")) - 1
        self.equipped_weapon = weapon_options[choice]
        self.inventory.equip_item(self.equipped_weapon)
        logging.debug(f"Equipped Weapon: {self.equipped_weapon.name}")
        print(f"You equipped {self.equipped_weapon.name}!")

    def equip_armor(self):
        print("Choose an armor to equip:")
        for i, armor in enumerate(armor_options):
            print(f"{i + 1}. {armor.name} - Defense: {armor.defense}, Weight: {armor.weight}, Description: {armor.description}")
        choice = int(input("Enter the number of your choice: ")) - 1
        self.equipped_armor = armor_options[choice]
        self.inventory.equip_item(self.equipped_armor)
        logging.debug(f"Equipped Armor: {self.equipped_armor.name}")
        print(f"You equipped {self.equipped_armor.name}!")

    def apply_lingering_effects(self):
        for effect in self.lingering_effects:
            effect.apply(self)

    def remove_lingering_effects(self):
        self.lingering_effects = []
        print(f"{self.name} removed all lingering effects!")

    def equip_item(self, item):
        if item in self.inventory:
            print(f"You have equipped {item}.")
            # Implement equip logic here
        else:
            print(f"You do not have {item} in your inventory.")

    def use_item(self, item):
        if item in self.inventory:
            if item == "Health Potion":
                self.hp = min(100, self.hp + 50)
                print(f"Your health is restored. Current HP: {self.hp}")
            elif item == "Mana Potion":
                self.mp = min(50, self.mp + 30)
                print(f"Your mana is restored. Current MP: {self.mp}")
            self.inventory.remove(item)
        else:
            print(f"You do not have {item} in your inventory.")

def create_character(screen):
    pygame.init()
    font = pygame.font.Font(None, 36)

    # Load and resize class images
    mage_image = pygame.image.load('assets/mage.png')
    thief_image = pygame.image.load('assets/thief.png')
    warrior_image = pygame.image.load('assets/warrior.png')
    mage_image = pygame.transform.scale(mage_image, (300,300))
    thief_image = pygame.transform.scale(thief_image, (300,300))
    warrior_image = pygame.transform.scale(warrior_image, (350,300))
    class_images = {"Mage": mage_image, "Thief": thief_image, "Warrior": warrior_image}

    name = ""
    char_class = None
    stats = {}
    skills = []

    # Input character name
    name_entered = False
    while not name_entered:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name:
                    name_entered = True
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    name += event.unicode

        screen.fill((0, 0, 0))
        text = font.render("Enter your character's name: " + name, True, (255, 255, 255))
        screen.blit(text, (50, 50))
        pygame.display.flip()

    # Class selection
    class_options = [
        {"name": "Warrior", "stats": {"Strength": 10, "Agility": 5, "Intelligence": 3}, "skills": ["Slash", "Block", "Cure"]},
        {"name": "Mage", "stats": {"Strength": 3, "Agility": 5, "Intelligence": 10}, "skills": ["Fireball", "Teleport", "Cure"]},
        {"name": "Thief", "stats": {"Strength": 5, "Agility": 10, "Intelligence": 5}, "skills": ["Steal", "Backstab", "Cure"]}
    ]
    selected_class = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for i, option in enumerate(class_options):
                    rect = pygame.Rect(50, 100 + i * 50, 200, 40)
                    if rect.collidepoint(mouse_pos):
                        selected_class = option
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and selected_class:
                char_class = selected_class["name"]
                stats = selected_class["stats"]
                skills = selected_class["skills"]
                break

        screen.fill((0, 0, 0))
        text = font.render("Choose your class:", True, (255, 255, 255))
        screen.blit(text, (50, 50))

        for i, option in enumerate(class_options):
            text = font.render(option["name"], True, (255, 255, 255))
            screen.blit(text, (50, 100 + i * 50))

        if selected_class:
            text = font.render(f"Selected Class: {selected_class['name']}", True, (255, 255, 255))
            screen.blit(text, (300, 100))
            text = font.render(f"Stats: {selected_class['stats']}", True, (255, 255, 255))
            screen.blit(text, (300, 150))
            text = font.render(f"Skills: {', '.join(selected_class['skills'])}", True, (255, 255, 255))
            screen.blit(text, (300, 200))
            text = font.render("Press Enter to confirm or click another class to change", True, (255, 255, 255))
            screen.blit(text, (50, 300))

            # Display class image aligned to the side
            class_image = class_images[selected_class["name"]]
            screen.blit(class_image, (70, 300))

        pygame.display.flip()

        if char_class:
            break

    character = Character(name, char_class, stats, skills)
    logging.debug(f"Created Character: {character.name}, Class: {character.char_class}, Stats: {character.stats}, Skills: {character.skills}")
    print("Character created successfully!")
    print(character)

    return character

def save_character_to_db(character):
    # Placeholder function to save character to a database
    pass

if __name__ == "__main__":
    screen = pygame.display.set_mode((800, 600))
    create_character(screen)