import random
import pygame

# Predefined list of 20 enemies with their characteristics
enemies = [
    {
        "name": "Goblin",
        "hp": 50,
        "attack": 5,
        "defense": 2,
        "magical_resistance": 10,
        "special_ability": "Poisoned Dagger",
        "xp_value": 50,
        "level": 1,
        "mp": 20,  # Default MP for enemy
        "sp": 30   # Default SP for enemy
    },
    {
        "name": "Orc",
        "hp": 100,
        "attack": 10,
        "defense": 5,
        "magical_resistance": 20,
        "special_ability": "Berserk Rage",
        "xp_value": 100,
        "level": 1,
        "mp": 30,  # Default MP for enemy
        "sp": 40   # Default SP for enemy
    },
    {
        "name": "Dragon",
        "hp": 300,
        "attack": 25,
        "defense": 15,
        "magical_resistance": 50,
        "special_ability": "Fire Breath",
        "xp_value": 500,
        "level": 1,
        "mp": 50,  # Default MP for enemy
        "sp": 60   # Default SP for enemy
    },
    # Add more enemies as needed
    {
        "name": "Troll",
        "hp": 150,
        "attack": 15,
        "defense": 10,
        "magical_resistance": 5,
        "special_ability": "Regeneration",
        "xp_value": 150,
        "level": 1,
        "mp": 20,  # Default MP for enemy
        "sp": 30   # Default SP for enemy
    },
    {
        "name": "Vampire",
        "hp": 120,
        "attack": 20,
        "defense": 8,
        "magical_resistance": 15,
        "special_ability": "Life Drain",
        "xp_value": 200,
        "level": 1,
        "mp": 40,  # Default MP for enemy
        "sp": 20   # Default SP for enemy
    },
    {
        "name": "Zombie",
        "hp": 80,
        "attack": 8,
        "defense": 5,
        "magical_resistance": 5,
        "special_ability": "Infectious Bite",
        "xp_value": 70,
        "level": 1,
        "mp": 10,  # Default MP for enemy
        "sp": 20   # Default SP for enemy
    },
    {
        "name": "Skeleton",
        "hp": 60,
        "attack": 7,
        "defense": 3,
        "magical_resistance": 5,
        "special_ability": "Curse",
        "xp_value": 60,
        "level": 1,
        "mp": 15,  # Default MP for enemy
        "sp": 10   # Default SP for enemy
    },
    {
        "name": "Werewolf",
        "hp": 140,
        "attack": 18,
        "defense": 12,
        "magical_resistance": 10,
        "special_ability": "Frenzy",
        "xp_value": 180,
        "level": 1,
        "mp": 20,  # Default MP for enemy
        "sp": 30   # Default SP for enemy
    },
    {
        "name": "Giant Spider",
        "hp": 90,
        "attack": 12,
        "defense": 8,
        "magical_resistance": 5,
        "special_ability": "Poisoned Dagger",
        "xp_value": 90,
        "level": 1,
        "mp": 10,  # Default MP for enemy
        "sp": 20   # Default SP for enemy
    },
    {
        "name": "Dark Mage",
        "hp": 70,
        "attack": 10,
        "defense": 5,
        "magical_resistance": 20,
        "special_ability": "Curse",
        "xp_value": 100,
        "level": 1,
        "mp": 50,  # Default MP for enemy
        "sp": 10   # Default SP for enemy
    },
    {
        "name": "Lich",
        "hp": 200,
        "attack": 15,
        "defense": 10,
        "magical_resistance": 30,
        "special_ability": "Life Drain",
        "xp_value": 300,
        "level": 1,
        "mp": 60,  # Default MP for enemy
        "sp": 20   # Default SP for enemy
    },
    {
        "name": "Minotaur",
        "hp": 180,
        "attack": 20,
        "defense": 15,
        "magical_resistance": 10,
        "special_ability": "Berserk Rage",
        "xp_value": 250,
        "level": 1,
        "mp": 30,  # Default MP for enemy
        "sp": 40   # Default SP for enemy
    },
    {
        "name": "Hydra",
        "hp": 250,
        "attack": 22,
        "defense": 18,
        "magical_resistance": 20,
        "special_ability": "Regeneration",
        "xp_value": 400,
        "level": 1,
        "mp": 50,  # Default MP for enemy
        "sp": 30   # Default SP for enemy
    },
    {
        "name": "Golem",
        "hp": 300,
        "attack": 25,
        "defense": 20,
        "magical_resistance": 15,
        "special_ability": "Earthquake Stomp",
        "xp_value": 350,
        "level": 1,
        "mp": 20,  # Default MP for enemy
        "sp": 40   # Default SP for enemy
    },
    {
        "name": "Phoenix",
        "hp": 150,
        "attack": 18,
        "defense": 12,
        "magical_resistance": 25,
        "special_ability": "Fire Breath",
        "xp_value": 300,
        "level": 1,
        "mp": 60,  # Default MP for enemy
        "sp": 30   # Default SP for enemy
    },
    {
        "name": "Basilisk",
        "hp": 130,
        "attack": 17,
        "defense": 10,
        "magical_resistance": 15,
        "special_ability": "Poisoned Dagger",
        "xp_value": 200,
        "level": 1,
        "mp": 20,  # Default MP for enemy
        "sp": 30   # Default SP for enemy
    },
    {
        "name": "Griffin",
        "hp": 160,
        "attack": 20,
        "defense": 15,
        "magical_resistance": 10,
        "special_ability": "Sky Dive",
        "xp_value": 250,
        "level": 1,
        "mp": 30,  # Default MP for enemy
        "sp": 40   # Default SP for enemy
    },
    {
        "name": "Cyclops",
        "hp": 220,
        "attack": 25,
        "defense": 18,
        "magical_resistance": 10,
        "special_ability": "Earthquake Stomp",
        "xp_value": 300,
        "level": 1,
        "mp": 20,  # Default MP for enemy
        "sp": 40   # Default SP for enemy
    },
    {
        "name": "Kraken",
        "hp": 280,
        "attack": 22,
        "defense": 20,
        "magical_resistance": 15,
        "special_ability": "Life Drain",
        "xp_value": 400,
        "level": 1,
        "mp": 50,  # Default MP for enemy
        "sp": 30   # Default SP for enemy
    },
    {
        "name": "Demon",
        "hp": 250,
        "attack": 30,
        "defense": 20,
        "magical_resistance": 25,
        "special_ability": "Fire Breath",
        "xp_value": 500,
        "level": 1,
        "mp": 60,  # Default MP for enemy
        "sp": 40   # Default SP for enemy
    }
]

# Function to select an enemy
def select_enemy(enemy_name):
    for enemy in enemies:
        if enemy["name"].lower() == enemy_name.lower():
            return enemy.copy()  # Return a copy to avoid modifying the original

# Function to display enemy details
def display_enemy_details(enemy):
    if enemy:
        print(f"Selected enemy: {enemy['name']}")
        print(f"Health: {enemy['hp']}")
        print(f"Attack: {enemy['attack']}")
        print(f"Defense: {enemy['defense']}")
        print(f"Magical Resistance: {enemy['magical_resistance']}")
        print(f"Special Ability: {enemy['special_ability']}")
        print(f"XP Value: {enemy['xp_value']}")
        print(f"Level: {enemy['level']}")
        print(f"MP: {enemy['mp']}")
        print(f"SP: {enemy['sp']}")
    else:
        print("Enemy not found.")

# Function to get story relevance of an enemy
def get_enemy_story(enemy_name):
    story_relevance = {
        "Goblin": "A common creature found in the dark corners of the forest.",
        "Orc": "A fierce warrior guarding the entrance to the ancient cave.",
        "Dragon": "The legendary dragon that holds the key to the kingdom's treasure.",
        "Troll": "A large and brutish creature that regenerates health.",
        "Vampire": "A blood-sucking creature that drains life from its victims.",
        "Zombie": "A reanimated corpse that spreads infection.",
        "Skeleton": "A skeletal warrior that curses its enemies.",
        "Werewolf": "A ferocious beast that goes into a frenzy during battle.",
        "Giant Spider": "A massive spider that uses poison to weaken its prey.",
        "Dark Mage": "A sorcerer who uses dark magic to curse opponents.",
        "Lich": "An undead mage that drains life to sustain itself.",
        "Minotaur": "A powerful beast that goes berserk in battle.",
        "Hydra": "A multi-headed serpent that regenerates its health.",
        "Golem": "A stone guardian that causes earthquakes with its stomps.",
        "Phoenix": "A mythical bird that breathes fire.",
        "Basilisk": "A serpent that uses poison to kill its enemies.",
        "Griffin": "A majestic creature that dives from the sky to attack.",
        "Cyclops": "A one-eyed giant that causes earthquakes with its stomps.",
        "Kraken": "A sea monster that drains life from its victims.",
        "Demon": "A powerful demon that breathes fire and causes destruction."
    }
    return story_relevance.get(enemy_name, "No story available for this enemy.")

# Function to adjust enemy stats based on level
def adjust_enemy_stats(enemy, level):
    multiplier = 1 + (level - 1) * 0.1  # Example multiplier: 10% increase per level
    enemy["hp"] = int(enemy["hp"] * multiplier)
    enemy["attack"] = int(enemy["attack"] * multiplier)
    enemy["defense"] = int(enemy["defense"] * multiplier)
    enemy["magical_resistance"] = int(enemy["magical_resistance"] * multiplier)
    enemy["xp_value"] = int(enemy["xp_value"] * multiplier)
    enemy["level"] = level
    enemy["mp"] = int(enemy["mp"] * multiplier)  # Adjust MP based on level
    enemy["sp"] = int(enemy["sp"] * multiplier)  # Adjust SP based on level

# Define enemy skills
enemy_skills = {
    "Poisoned Dagger": {
        "description": "A poisoned attack that deals damage over time.",
        "effect": lambda player, enemy: setattr(player, 'hp', player.hp - 5),
        "cost": {"sp": 5}  # Costs 5 SP
    },
    "Berserk Rage": {
        "description": "Increases attack power for a short time.",
        "effect": lambda player, enemy: enemy.update({"attack": enemy["attack"] * 1.5}),
        "cost": {"sp": 10}  # Costs 10 SP
    },
    "Fire Breath": {
        "description": "A fiery attack that deals massive damage.",
        "effect": lambda player, enemy: setattr(player, 'hp', player.hp - (enemy["attack"] * 2)),
        "cost": {"mp": 15}  # Costs 15 MP
    },
    "Infectious Bite": {
        "description": "A bite that infects the player, dealing damage over time.",
        "effect": lambda player, enemy: setattr(player, 'hp', player.hp - 5),
        "cost": {"sp": 5}  # Costs 5 SP
    },
    "Frenzy": {
        "description": "A frenzied attack that deals extra damage.",
        "effect": lambda player, enemy: setattr(player, 'hp', player.hp - (enemy["attack"] * 1.5)),
        "cost": {"sp": 10}  # Costs 10 SP
    },
    "Earthquake Stomp": {
        "description": "A powerful stomp that deals area damage.",
        "effect": lambda player, enemy: setattr(player, 'hp', player.hp - 10),
        "cost": {"sp": 15}  # Costs 15 SP
    },
    "Sky Dive": {
        "description": "A diving attack from above.",
        "effect": lambda player, enemy: setattr(player, 'hp', player.hp - (enemy["attack"] * 1.5)),
        "cost": {"sp": 10}  # Costs 10 SP
    },
    "Life Drain": {
        "description": "Drains life from the player to heal the enemy.",
        "effect": lambda player, enemy: (setattr(player, 'hp', player.hp - 10), enemy.update({"hp": enemy["hp"] + 10})),
        "cost": {"mp": 10}  # Costs 10 MP
    },
    "Regeneration": {
        "description": "Regenerates health over time.",
        "effect": lambda player, enemy: enemy.update({"hp": enemy["hp"] + 10}),
        "cost": {"mp": 5}  # Costs 5 MP
    },
    "Curse": {
        "description": "Curses the player, reducing their stats.",
        "effect": lambda player, enemy: setattr(player, 'stats', {k: v - 1 for k, v in player.stats.items()}),
        "cost": {"mp": 5}  # Costs 5 MP
    }
}

# Function to regenerate MP for an enemy
def regenerate_enemy_mp(enemy):
    regen_amount = 5  # Example regeneration amount
    max_mp = 10 + (enemy["magical_resistance"] * 5)  # Example calculation for max MP
    enemy["mp"] = min(max_mp, enemy["mp"] + regen_amount)
    if enemy["mp"] < max_mp:
        print(f"{enemy['name']} regenerated {regen_amount} MP. Current MP: {enemy['mp']}")

# Function to regenerate SP for an enemy
def regenerate_enemy_sp(enemy):
    regen_amount = 5  # Example regeneration amount
    max_sp = 10 + (enemy["defense"] * 5)  # Example calculation for max SP
    enemy["sp"] = min(max_sp, enemy["sp"] + regen_amount)
    if enemy['sp'] < max_sp:
        print(f"{enemy['name']} regenerated {regen_amount} SP. Current SP: {enemy['sp']}")

class Enemy:
    def __init__(self, name, hp, attack, defense, magical_resistance, special_ability, xp_value, level, mp, sp):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.magical_resistance = magical_resistance
        self.special_ability = special_ability
        self.xp_value = xp_value
        self.level = level
        self.mp = mp
        self.sp = sp

    def draw(self, screen, position):
        enemy_image = pygame.Surface((50, 50))
        enemy_image.fill((255, 255, 255))
        screen.blit(enemy_image, position)

# Example usage
if __name__ == "__main__":
    enemy_name = input("Enter the name of the enemy to select: ")
    selected_enemy = select_enemy(enemy_name)
    if selected_enemy:
        level = int(input("Enter the level of the enemy: "))
        adjust_enemy_stats(selected_enemy, level)
        display_enemy_details(selected_enemy)
        story = get_enemy_story(selected_enemy["name"])
        print(f"Story: {story}")