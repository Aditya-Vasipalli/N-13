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
        screen.fill((0, 0, 0))
        text = font.render("Main Menu", True, (255, 255, 255))
        screen.blit(text, (350, 50))

        option_rects = []
        for i, option in enumerate(options):
            text = font.render(option, True, (255, 255, 255))
            rect = text.get_rect(topleft=(200, 150 + i * 50))
            option_rects.append(rect)
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