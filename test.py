import unittest
from character_creation import create_character, Character
from combat_system import win_or_loss, display_bars, playerdmgcalc, oppdmgcalc
from enemies import select_enemy, display_enemy_details, adjust_enemy_stats, enemy_skills, enemies
from skills import player_skills
from quest import start_quest, traverse_paths, manage_inventory, village_path, visit_market, explore_forest, find_hidden_treasure, visit_wise_old_man, deeper_forest, return_to_king, dragon_lair
from npc import create_town_guard, create_shopkeeper, create_wise_old_man
from inventory import Inventory
from armor_weapon import armor_options, weapon_options

class TestRPGGame(unittest.TestCase):

    def test_create_character(self):
        character = create_character()
        self.assertIsInstance(character, Character)
        self.assertGreater(len(character.name), 0)
        self.assertIn(character.char_class, ["Warrior", "Mage", "Thief"])

    def test_combat_system(self):
        character = create_character()
        enemy = select_enemy("Goblin")
        adjust_enemy_stats(enemy, 1)
        result = win_or_loss(character, enemy)
        self.assertIn(result, ["Victory!", "Defeat!"])

    def test_inventory(self):
        inventory = Inventory()
        inventory.add_item("Health Potion")
        self.assertIn("Health Potion", inventory.items)
        inventory.remove_item("Health Potion")
        self.assertNotIn("Health Potion", inventory.items)

    def test_npc_interaction(self):
        town_guard = create_town_guard()
        self.assertEqual(town_guard.name, "Town Guard")
        self.assertEqual(town_guard.dialogue, "Halt! Who goes there?")

    def test_armor_weapon(self):
        self.assertGreater(len(armor_options), 0)
        self.assertGreater(len(weapon_options), 0)

    def test_quest(self):
        character = create_character()
        start_quest(character, lambda: None)

    def test_playerdmgcalc(self):
        character = create_character()
        damage = playerdmgcalc(character)
        self.assertGreaterEqual(damage, 0)

    def test_oppdmgcalc(self):
        enemy = select_enemy("Goblin")
        damage = oppdmgcalc(enemy)
        self.assertGreaterEqual(damage, 0)

    def test_display_bars(self):
        character = create_character()
        enemy = select_enemy("Goblin")
        display_bars(character, enemy)

    def test_traverse_paths(self):
        character = create_character()
        traverse_paths(character, lambda: None, (0, 0))

    def test_manage_inventory(self):
        character = create_character()
        manage_inventory(character)

    def test_village_path(self):
        character = create_character()
        village_path(character)

    def test_visit_market(self):
        character = create_character()
        visit_market(character)

    def test_explore_forest(self):
        character = create_character()
        explore_forest(character)

    def test_find_hidden_treasure(self):
        character = create_character()
        find_hidden_treasure(character)

    def test_visit_wise_old_man(self):
        character = create_character()
        visit_wise_old_man(character)

    def test_deeper_forest(self):
        character = create_character()
        deeper_forest(character)

    def test_return_to_king(self):
        character = create_character()
        return_to_king(character)

    def test_dragon_lair(self):
        character = create_character()
        dragon_lair(character)

if __name__ == "__main__":
    unittest.main()