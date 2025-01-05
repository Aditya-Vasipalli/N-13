class NPC:
    def __init__(self, name, description, dialogue):
        self.name = name
        self.description = description
        self.dialogue = dialogue

    def interact(self):
        print(f"{self.name}: {self.dialogue}")

# Example NPC functions

def create_town_guard():
    name = "Town Guard"
    description = "A stern-looking guard patrolling the town."
    dialogue = "Halt! Who goes there?"
    return NPC(name, description, dialogue)

def create_shopkeeper():
    name = "Shopkeeper"
    description = "A friendly shopkeeper ready to sell you goods."
    dialogue = "Welcome to my shop! How can I help you today?"
    return NPC(name, description, dialogue)

def create_wise_old_man():
    name = "Wise Old Man"
    description = "An old man with a long beard and a wealth of knowledge."
    dialogue = "Greetings, traveler. Do you seek wisdom?"
    return NPC(name, description, dialogue)

# Example usage
if __name__ == "__main__":
    town_guard = create_town_guard()
    shopkeeper = create_shopkeeper()
    wise_old_man = create_wise_old_man()

    town_guard.interact()
    shopkeeper.interact()
    wise_old_man.interact()