import logging
import mysql.connector
from armor_weapon import armor_options, weapon_options, Armor, Weapon
from inventory import Inventory
import pygame
import sys
import json

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

    def learn_new_move(self, screen):
        available_moves = ["Thunder Strike", "Heal", "Ice Blast", "Shadow Step"]
        font = pygame.font.Font(None, 36)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        new_move = available_moves[0]
                        break
                    elif event.key == pygame.K_2:
                        new_move = available_moves[1]
                        break
                    elif event.key == pygame.K_3:
                        new_move = available_moves[2]
                        break
                    elif event.key == pygame.K_4:
                        new_move = available_moves[3]
                        break

            screen.fill((0, 0, 0))
            text = font.render("You have the opportunity to learn a new move!", True, (255, 255, 255))
            screen.blit(text, (50, 50))
            for i, move in enumerate(available_moves):
                text = font.render(f"{i + 1}. {move}", True, (255, 255, 255))
                screen.blit(text, (50, 100 + i * 50))
            pygame.display.flip()

        if len(self.skills) >= 4:
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                            forget_choice = int(event.unicode) - 1
                            break

                screen.fill((0, 0, 0))
                text = font.render("You already have 4 moves. Choose a move to forget:", True, (255, 255, 255))
                screen.blit(text, (50, 50))
                for i, skill in enumerate(self.skills):
                    text = font.render(f"{i + 1}. {skill}", True, (255, 255, 255))
                    screen.blit(text, (50, 100 + i * 50))
                pygame.display.flip()

            self.skills[forget_choice] = new_move
        else:
            self.skills.append(new_move)

        screen.fill((0, 0, 0))
        text = font.render(f"You learned {new_move}!", True, (255, 255, 255))
        screen.blit(text, (50, 50))
        pygame.display.flip()
        pygame.time.wait(2000)  # Show for 2 seconds

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
            self.hp -= effect["damage"]
            print(f"{self.name} takes {effect['damage']} damage from {effect['name']}. Current HP: {self.hp}")
            flash_lingering_effect_message(self.name, effect["name"])

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
        if item in self.inventory.items:
            if item == "Health Potion":
                self.hp = min(self.max_hp, self.hp + 50)
                print(f"Your health is restored. Current HP: {self.hp}")
            elif item == "MP Potion":
                self.mp = min(self.max_mp, self.mp + 20)
                print(f"Your mana is restored. Current MP: {self.mp}")
            elif item == "SP Potion":
                self.sp = min(self.max_sp, self.sp + 20)
                print(f"Your stamina is restored. Current SP: {self.sp}")
            self.inventory.remove_item(item)
        else:
            print(f"You do not have {item} in your inventory.")

    def game_over(self, screen):
        font = pygame.font.Font(None, 36)
        screen.fill((0, 0, 0))
        text = font.render(f"{self.name} has died. Game Over.", True, (255, 0, 0))
        screen.blit(text, (50, 50))
        pygame.display.flip()
        pygame.time.wait(3000)  # Show for 3 seconds
        pygame.quit()
        sys.exit()

    def save_character(self, current_position):
        character_data = {
            "name": self.name,
            "char_class": self.char_class,
            "stats": self.stats,
            "skills": self.skills,
            "level": self.level,
            "xp": self.xp,
            "hp": self.hp,
            "max_hp": self.max_hp,
            "mp": self.mp,
            "max_mp": self.max_mp,
            "sp": self.sp,
            "max_sp": self.max_sp,
            "xp_threshold": self.xp_threshold,
            "stat_points": self.stat_points,
            "crit_chance": self.crit_chance,
            "critdmg": self.critdmg,
            "equipped_weapon": self.equipped_weapon.name if self.equipped_weapon else None,
            "equipped_armor": self.equipped_armor.name if self.equipped_armor else None,
            "lingering_effects": self.lingering_effects,
            "money": self.money,
            "inventory": self.inventory.items,
            "current_position": current_position
        }
        with open(f"{self.name}_save.json", "w") as file:
            json.dump(character_data, file)
        print(f"Character {self.name} saved successfully.")

    @classmethod
    def load_character(cls, filename):
        with open(filename, "r") as file:
            character_data = json.load(file)
        character = cls(
            character_data["name"],
            character_data["char_class"],
            character_data["stats"],
            character_data["skills"]
        )
        character.level = character_data["level"]
        character.xp = character_data["xp"]
        character.hp = character_data["hp"]
        character.max_hp = character_data["max_hp"]
        character.mp = character_data["mp"]
        character.max_mp = character_data["max_mp"]
        character.sp = character_data["sp"]
        character.max_sp = character_data["max_sp"]
        character.xp_threshold = character_data["xp_threshold"]
        character.stat_points = character_data["stat_points"]
        character.crit_chance = character_data["crit_chance"]
        character.critdmg = character_data["critdmg"]
        character.equipped_weapon = character_data["equipped_weapon"]
        character.equipped_armor = character_data["equipped_armor"]
        character.lingering_effects = character_data["lingering_effects"]
        character.money = character_data["money"]
        character.inventory.items = character_data["inventory"]
        current_position = character_data["current_position"]
        print(f"Character {character.name} loaded successfully.")
        return character, current_position

def flash_lingering_effect_message(name, effect_name):
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    font = pygame.font.Font(None, 36)
    message = f"{name} has been hit with a lingering effect: {effect_name}. Use Cure to stop more damage!"
    text = font.render(message, True, (255, 0, 0))  # Red color for warning
    screen.fill((0, 0, 0))  # Clear screen with black
    screen.blit(text, (50, 300))
    pygame.display.flip()
    pygame.time.wait(1000)  # Show for 1 second (reduced from 2 seconds)

def create_character(screen):
    pygame.init()
    font = pygame.font.Font(None, 36)

    # Load and resize class images
    mage_image = pygame.image.load('assets/mage.png')
    thief_image = pygame.image.load('assets/thief.png')
    warrior_image = pygame.image.load('assets/warrior.png')
    mage_image = pygame.transform.scale(mage_image, (180, 180))
    thief_image = pygame.transform.scale(thief_image, (180, 180))
    warrior_image = pygame.transform.scale(warrior_image, (180, 180))
    class_images = {"Mage": mage_image, "Thief": thief_image, "Warrior": warrior_image}

    # Load and scale the character creation background image
    creation_bg = pygame.image.load('assets/character_creation.png')
    creation_bg = pygame.transform.scale(creation_bg, (screen.get_width(), screen.get_height()))

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

        screen.blit(creation_bg, (0, 0))  # Draw the background image
        text = font.render("Enter your character's name: " + name, True, (0, 0, 0))  # Black color
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
                    rect = pygame.Rect(50, 100 + i * 70, 302, 52)  # Increase size of options and make boxes 2 pixels wider
                    if rect.collidepoint(mouse_pos):
                        selected_class = option
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and selected_class:
                char_class = selected_class["name"]
                stats = selected_class["stats"]
                skills = selected_class["skills"]
                break

        screen.blit(creation_bg, (0, 0))  # Draw the background image
        text = font.render("Choose your class:", True, (0, 0, 0))  # Black color
        screen.blit(text, (50, 50))

        for i, option in enumerate(class_options):
            text = font.render(option["name"], True, (0, 0, 0))  # Black color
            rect = text.get_rect(topleft=(50, 100 + i * 70))  # Increase size of options
            # Draw semi-transparent rounded box
            box_color = (255, 255, 255, 128)  # Semi-transparent white
            if rect.collidepoint(pygame.mouse.get_pos()):
                box_color = (255, 255, 255, 255)  # Opaque white when hovered
            box_surface = pygame.Surface((rect.width + 42, rect.height + 22), pygame.SRCALPHA)
            pygame.draw.rect(box_surface, box_color, box_surface.get_rect(), border_radius=10)
            screen.blit(box_surface, (rect.x - 21, rect.y - 11))
            screen.blit(text, rect)

        if selected_class:
            text = font.render(f"Selected Class: {selected_class['name']}", True, (0, 0, 0))  # Black color
            screen.blit(text, (300, 100))
            text = font.render(f"Stats:", True, (0, 0, 0))  # Black color
            screen.blit(text, (300, 150))
            for j, (stat, value) in enumerate(selected_class['stats'].items()):
                stat_text = font.render(f"{stat}: {value}", True, (0, 0, 0))  # Black color
                screen.blit(stat_text, (300, 180 + j * 30))
            text = font.render(f"Skills: {', '.join(selected_class['skills'])}", True, (0, 0, 0))  # Black color
            screen.blit(text, (300, 300))
            text = font.render("Press Enter to confirm or click another class to change", True, (0, 0, 0))  # Black color
            screen.blit(text, (50, 400))

            # Display class image aligned to the side
            class_image = class_images[selected_class["name"]]
            screen.blit(class_image, (70, 420))

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