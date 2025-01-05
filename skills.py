# Define player skills
player_skills = {
    "Fireball": {
        "description": "A powerful fire attack.",
        "effect": lambda player, enemy: enemy.update({"hp": enemy["hp"] - 30}),
        "cost": {"mp": 10}  # Costs 10 MP
    },
    "Heal": {
        "description": "Heals the player.",
        "effect": lambda player, enemy: setattr(player, 'hp', player.hp + 20),
        "cost": {"mp": 5}  # Costs 5 MP
    },
    "Lightning Strike": {
        "description": "A powerful lightning attack.",
        "effect": lambda player, enemy: enemy.update({"hp": enemy["hp"] - 40}),
        "cost": {"mp": 15}  # Costs 15 MP
    },
    "Teleport": {
        "description": "Teleports the player to a safe location.",
        "effect": lambda player, enemy: print("You teleported to a safe location."),
        "cost": {"mp": 20}  # Costs 20 MP
    },
    "Steal": {
        "description": "Steals a small amount of health from the enemy.",
        "effect": lambda player, enemy: (enemy.update({"hp": enemy["hp"] - 5}), setattr(player, 'hp', player.hp + 5)),
        "cost": {"sp": 4}  # Costs 4 SP
    },
    "Backstab": {
        "description": "A sneaky attack that deals extra damage.",
        "effect": lambda player, enemy: enemy.update({"hp": enemy["hp"] - (player.stats["Agility"] * 2)}),
        "cost": {"sp": 6}  # Costs 6 SP
    },
    "Cure": {
        "description": "Removes all lingering effects.",
        "effect": lambda player, enemy: player.remove_lingering_effects(),
        "cost": {"mp": 8}  # Costs 8 MP
    },
    "Slash": {
        "description": "A basic attack with your weapon.",
        "effect": lambda player, enemy: enemy.update({"hp": enemy["hp"] - (player.stats["Strength"] * 1.5)}),
        "cost": {"sp": 2}  # Costs 2 SP
    },
    "Block": {
        "description": "Reduces incoming damage for one turn.",
        "effect": lambda player, enemy: setattr(player, 'block', True),
        "cost": {"sp": 3}  # Costs 3 SP
    },
    "Ice Shard": {
        "description": "A sharp ice attack.",
        "effect": lambda player, enemy: enemy.update({"hp": enemy["hp"] - 25}),
        "cost": {"mp": 12}  # Costs 12 MP
    },
    "Earthquake": {
        "description": "A powerful ground attack.",
        "effect": lambda player, enemy: enemy.update({"hp": enemy["hp"] - 35}),
        "cost": {"mp": 18}  # Costs 18 MP
    }
}

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
        "description": "A bite that infects the player, causing damage over time.",
        "effect": lambda player, enemy: setattr(player, 'hp', player.hp - 10),
        "cost": {"sp": 8}  # Costs 8 SP
    }
}