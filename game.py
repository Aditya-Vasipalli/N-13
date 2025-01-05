import pygame
import sys
from xp import Player
from enemies import select_enemy, display_enemy_details, adjust_enemy_stats
from quest import start_quest
from Menu import main_menu
from combat_system import win_or_loss

# Initialize Pygame
pygame.init()

# Set up the game window
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("2D RPG Game")

# Load and scale background image to fit 33x33 blocks
background_image = pygame.image.load('assets/background_map.png')
background_image = pygame.transform.scale(background_image, (33 * 32, 33 * 32))

# Load character images
mage_image = pygame.image.load('assets/mage.png')
thief_image = pygame.image.load('assets/thief.png')
warrior_image = pygame.image.load('assets/warrior.png')
class_images = {"Mage": mage_image, "Thief": thief_image, "Warrior": warrior_image}

# Resize character images to fit one grid box
for key in class_images:
    class_images[key] = pygame.transform.scale(class_images[key], (32, 32))

# Create a red box as a placeholder for the enemy image
enemy_image = pygame.Surface((32, 32))  # Adjust size to 1 block
enemy_image.fill((255, 0, 0))

# Define a fixed map layout with different areas
map_grid = [
    [""] * 33 for _ in range(33)
]

# Define enemy positions (hidden in certain regions)
enemy_positions = [(2, 2), (4, 4), (6, 6), (8, 8)]

# Main game loop
def main():
    global screen
    character = None
    current_position = (0, 0) 
    clock = pygame.time.Clock()
    full_screen = False

    while True:
        if character is None:
            character, current_position = main_menu(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    full_screen = not full_screen
                    if full_screen:
                        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    else:
                        screen = pygame.display.set_mode((800, 600))
                # Handle sprite movement
                elif event.key == pygame.K_RIGHT and current_position[1] < len(map_grid[0]) - 1:
                    current_position = (current_position[0], current_position[1] + 1)
                elif event.key == pygame.K_LEFT and current_position[1] > 0:
                    current_position = (current_position[0], current_position[1] - 1)
                elif event.key == pygame.K_DOWN and current_position[0] < len(map_grid) - 1:
                    current_position = (current_position[0] + 1, current_position[1])
                elif event.key == pygame.K_UP and current_position[0] > 0:
                    current_position = (current_position[0] - 1, current_position[1])
                
                # Handle interaction with the current map location
                location = map_grid[current_position[0]][current_position[1]]
                print(f"Interacting with {location}")
                handle_location_interaction(character, location, current_position)

        # Draw everything
        screen.fill((0, 0, 0))  # Clear screen with black

        # Calculate the offset for scrolling
        offset_x = max(0, min(current_position[1] * 32 - screen.get_width() // 2, background_image.get_width() - screen.get_width()))
        offset_y = max(0, min(current_position[0] * 32 - screen.get_height() // 2, background_image.get_height() - screen.get_height()))

        # Draw the background image with scrolling
        screen.blit(background_image, (-offset_x, -offset_y))

        # Draw the map
        for y, row in enumerate(map_grid):
            for x, cell in enumerate(row):
                if (x, y) == current_position:
                    screen.blit(class_images[character.char_class], (y * 32 - offset_x, x * 32 - offset_y))
                elif (x, y) in enemy_positions:
                    screen.blit(enemy_image, (y * 32 - offset_x, x * 32 - offset_y))

        pygame.display.flip()

        clock.tick(60)  # Limit to 60 frames per second

def assign_stat_points(character):
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    font = pygame.font.Font(None, 36)
    clock = pygame.time.Clock()
    while character.stat_points > 0:
        #print(f"Debug: Starting stat allocation loop with {character.stat_points} stat points.")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    character.stats['Strength'] += 1
                    character.stat_points -= 1
                    print(f"Debug: Assigned 1 point to Strength. Remaining stat points: {character.stat_points}")
                elif event.key == pygame.K_2:
                    character.stats['Agility'] += 1
                    character.stat_points -= 1
                    print(f"Debug: Assigned 1 point to Agility. Remaining stat points: {character.stat_points}")
                elif event.key == pygame.K_3:
                    character.stats['Intelligence'] += 1
                    character.stat_points -= 1
                    print(f"Debug: Assigned 1 point to Intelligence. Remaining stat points: {character.stat_points}")

        screen.fill((0, 0, 0))
        text = font.render(f"You have {character.stat_points} stat points to assign.", True, (255, 255, 255))
        screen.blit(text, (50, 50))
        text = font.render("1. Strength", True, (255, 255, 255))
        screen.blit(text, (50, 100))
        text = font.render("2. Agility", True, (255, 255, 255))
        screen.blit(text, (50, 150))
        text = font.render("3. Intelligence", True, (255, 255, 255))
        screen.blit(text, (50, 200))
        pygame.display.flip()
        clock.tick(60)

def handle_location_interaction(character, location, current_position):
    print(f"Debug: Handling interaction at location {location} with position {current_position}.")
    if current_position in enemy_positions:
        print("You have encountered an enemy!")
        enemy = select_enemy("goblin")  # Replace with logic to select the appropriate enemy
        if enemy:
            adjust_enemy_stats(enemy, character.level)
            display_enemy_details(enemy)
            result = win_or_loss(character, enemy, screen)
            print(result)
            if character.hp > 0:
                print("Debug: Calling assign_stat_points after winning the battle.")
                if character.stat_points > 0:
                    assign_stat_points(character)  # Call assign_stat_points if stat_points is greater than 0
            if character.hp <= 0:
                game_over(character)
        else:
            print("Enemy not found.")
    elif location in ["village", "market", "forest", "cave", "mountain"]:
        print(f"You have arrived at the {location}.")
        # Add logic for specific locations
    else:
        print(f"You have arrived at the {location}.")

def game_over(character):
    print(f"{character.name} has died. Game Over.")
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
