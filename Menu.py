import pygame
from character_creation import create_character
import sys

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
                            # Logic to select an existing character
                            pass
                        elif i == 2:
                            if character is None:
                                print("Please create or select a character first.")
                            else:
                                return character, current_position
                        elif i == 3:
                            if character is None:
                                print("Please create or select a character first.")
                            else:
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

def start_game(character, current_position):
    talk_to_king(character)
    start_quest(character, main_menu, current_position)

def talk_to_king(character):
    print("King: Brave warrior, our kingdom is in grave danger.")
    print("King: A fearsome dragon is terrorizing our lands.")
    print("King: You must embark on a quest to slay the dragon and save our people.")
    input("Press Enter to begin your quest...")