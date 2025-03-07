import pygame
from character_creation import create_character, Character  # Import Character class
import sys
import os

def start_quest(character, main_menu_callback, current_position):
    from quest import start_quest as quest_start
    quest_start(character, main_menu_callback, current_position)

def main_menu(screen):
    pygame.init()
    pygame.display.set_caption("Main Menu")

    character = None
    current_position = (0, 0)
    font = pygame.font.Font(None, 36)

    # Load and scale the menu background image
    menu_bg = pygame.image.load('assets/menu.png')
    menu_bg = pygame.transform.scale(menu_bg, (screen.get_width(), screen.get_height()))

    options = ["Create New Character", "Select Existing Character", "Start Game", "Continue Game", "Exit"]
    option_rects = []

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for i, rect in enumerate(option_rects):
                    if rect.collidepoint(mouse_pos):
                        if i == 0:
                            character = create_character(screen)
                            current_position = (0, 0)  # Reset position for new character
                        elif i == 1:
                            character, current_position = select_existing_character(screen)
                        elif i == 2:
                            if character is None:
                                character = create_default_character()  # Use default character if none selected
                            return character, current_position
                        elif i == 3:
                            if character is None:
                                character, current_position = load_last_saved_character()
                            return character, current_position
                        elif i == 4:
                            pygame.quit()
                            sys.exit()

        # Draw menu
        screen.blit(menu_bg, (0, 0))  # Draw the background image
        text = font.render("Main Menu", True, (0, 0, 0))  # Black color
        screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, 50))

        option_rects = []
        box_width = 300
        box_height = 50
        for i, option in enumerate(options):
            text = font.render(option, True, (0, 0, 0))  # Black color
            rect = text.get_rect(center=(screen.get_width() // 2, 150 + i * 60))
            option_rects.append(rect)
            # Draw semi-transparent rounded box
            box_color = (255, 255, 255, 128)  # Semi-transparent white
            if rect.collidepoint(pygame.mouse.get_pos()):
                box_color = (255, 255, 255, 255)  # Opaque white when hovered
            box_surface = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
            pygame.draw.rect(box_surface, box_color, box_surface.get_rect(), border_radius=10)
            screen.blit(box_surface, (rect.x - (box_width - rect.width) // 2, rect.y - (box_height - rect.height) // 2))
            screen.blit(text, rect)

        pygame.display.flip()

def select_existing_character(screen):
    font = pygame.font.Font(None, 36)
    save_files = [f for f in os.listdir() if f.endswith("_save.json")]
    selected_file = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for i, rect in enumerate(option_rects):
                    if rect.collidepoint(mouse_pos):
                        selected_file = save_files[i]
                        break

        screen.fill((0, 0, 0))
        text = font.render("Select a character to load:", True, (255, 255, 255))
        screen.blit(text, (50, 50))

        option_rects = []
        for i, save_file in enumerate(save_files):
            text = font.render(save_file, True, (255, 255, 255))
            rect = text.get_rect(topleft=(50, 100 + i * 50))
            option_rects.append(rect)
            screen.blit(text, rect)

        pygame.display.flip()

        if selected_file:
            return Character.load_character(selected_file)

def load_last_saved_character():
    save_files = [f for f in os.listdir() if f.endswith("_save.json")]
    if save_files:
        latest_save = max(save_files, key=os.path.getctime)
        return Character.load_character(latest_save)
    else:
        return create_default_character(), (0, 0)

def create_default_character():
    stats = {"Strength": 10, "Agility": 5, "Intelligence": 3}
    skills = ["Slash", "Block", "Cure"]
    return Character("Default Warrior", "Warrior", stats, skills)

def start_game(character, current_position):
    talk_to_king(character)
    start_quest(character, main_menu, current_position)

def talk_to_king(character):
    print("King: Brave warrior, our kingdom is in grave danger.")
    print("King: A fearsome dragon is terrorizing our lands.")
    print("King: You must embark on a quest to slay the dragon and save our people.")
    input("Press Enter to begin your quest...")