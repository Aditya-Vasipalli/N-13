import random
import time
import pygame
from character_creation import Character
from enemies import select_enemy, display_enemy_details, regenerate_enemy_mp, regenerate_enemy_sp
from skills import player_skills, enemy_skills
import sys

def playerdmgcalc(player):
    ch = random.random()
    if ch <= player.crit_chance:
        playerdmg = player.critdmg
    else:
        playerdmg = round(random.uniform(0, player.stats['Strength']), 2)
    return playerdmg

def oppdmgcalc(enemy):
    oppdmg = round(random.uniform(0, enemy['attack']), 2)
    return oppdmg

def display_bars(character, enemy, screen):
    # Draw health, MP, and SP bars on the screen
    font = pygame.font.Font(None, 36)
    player_hp_text = font.render(f"Player HP: {character.hp}", True, (255, 255, 255))
    player_mp_text = font.render(f"MP: {character.mp}", True, (255, 255, 255))
    player_sp_text = font.render(f"SP: {character.sp}", True, (255, 255, 255))
    enemy_hp_text = font.render(f"Enemy HP: {enemy['hp']}", True, (255, 255, 255))
    enemy_mp_text = font.render(f"MP: {enemy['mp']}", True, (255, 255, 255))
    enemy_sp_text = font.render(f"SP: {enemy['sp']}", True, (255, 255, 255))

    screen.blit(player_hp_text, (50, 50))
    screen.blit(player_mp_text, (50, 100))
    screen.blit(player_sp_text, (50, 150))
    screen.blit(enemy_hp_text, (450, 50))
    screen.blit(enemy_mp_text, (450, 100))
    screen.blit(enemy_sp_text, (450, 150))

def animate_action(action_text, screen):
    font = pygame.font.Font(None, 36)
    action_surface = font.render(action_text, True, (255, 255, 255))
    screen.fill((0, 0, 0))  # Clear screen
    screen.blit(action_surface, (50, 200))
    pygame.display.flip()
    pygame.time.wait(300)  # Wait for 300 milliseconds

def timing_slider(screen):
    font = pygame.font.Font(None, 36)
    slider_width = 200
    slider_height = 20
    slider_x = (screen.get_width() - slider_width) // 2
    slider_y = screen.get_height() - 100
    target_width = 40
    target_x = random.randint(slider_x, slider_x + slider_width - target_width)
    target_y = slider_y

    slider_rect = pygame.Rect(slider_x, slider_y, slider_width, slider_height)
    target_rect = pygame.Rect(target_x, target_y, target_width, slider_height)
    cursor_x = slider_x
    cursor_speed = 5
    direction = 1

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if target_rect.collidepoint(cursor_x, slider_y):
                        return True  # Hit
                    else:
                        return False  # Miss

        cursor_x += cursor_speed * direction
        if cursor_x <= slider_x or cursor_x >= slider_x + slider_width - 10:
            direction *= -1

        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (255, 255, 255), slider_rect)
        pygame.draw.rect(screen, (0, 255, 0), target_rect)
        pygame.draw.rect(screen, (255, 0, 0), (cursor_x, slider_y, 10, slider_height))
        text = font.render("Press SPACE to stop the slider!", True, (255, 255, 255))
        screen.blit(text, (slider_x, slider_y - 40))
        pygame.display.flip()
        pygame.time.Clock().tick(60)

def player_turn(player, enemy, screen):
    display_bars(player, enemy, screen)
    font = pygame.font.Font(None, 36)
    screen.fill((0, 0, 0))
    display_bars(player, enemy, screen)
    screen.blit(font.render("It's Your turn!", True, (255, 255, 255)), (50, 250))
    screen.blit(font.render("Choose your move:", True, (255, 255, 255)), (50, 300))
    
    options = [f"{i + 1}. {skill} - {player_skills[skill]['description']}" for i, skill in enumerate(player.skills)]
    options.append(f"{len(player.skills) + 1}. Use MP Potion")
    options.append(f"{len(player.skills) + 2}. Use SP Potion")
    
    for i, option in enumerate(options):
        screen.blit(font.render(option, True, (255, 255, 255)), (50, 350 + i * 50))
    
    pygame.display.flip()
    
    selected_skill = None  # Initialize selected_skill to None
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1 and len(player.skills) > 0:
                    selected_skill = player.skills[0]
                elif event.key == pygame.K_2 and len(player.skills) > 1:
                    selected_skill = player.skills[1]
                elif event.key == pygame.K_3 and len(player.skills) > 2:
                    selected_skill = player.skills[2]
                elif event.key == pygame.K_4 and len(player.skills) > 3:
                    selected_skill = player.skills[3]
                elif event.key == pygame.K_5:
                    use_mp_potion(player)
                    return None
                elif event.key == pygame.K_6:
                    use_sp_potion(player)
                    return None
                if selected_skill:
                    skill_cost = player_skills[selected_skill]["cost"]
                    if player.mp >= skill_cost.get("mp", 0) and player.sp >= skill_cost.get("sp", 0):
                        player.mp -= skill_cost.get("mp", 0)
                        player.sp -= skill_cost.get("sp", 0)
                        if timing_slider(screen):
                            animate_action(f"\nYou used {selected_skill}!", screen)
                            player_skills[selected_skill]["effect"](player, enemy)
                        else:
                            animate_action("\nYou missed!", screen)
                    else:
                        animate_action("\nNot enough MP or SP!", screen)
                    return selected_skill

def use_mp_potion(player):
    if "MP Potion" in player.inventory.items:
        player.mp = min(player.max_mp, player.mp + 20)
        player.inventory.items.remove("MP Potion")
        print("\nYou used an MP Potion and restored 20 MP.")
    else:
        print("\nYou don't have any MP Potions!")

def use_sp_potion(player):
    if "SP Potion" in player.inventory.items:
        player.sp = min(player.max_sp, player.sp + 20)
        player.inventory.items.remove("SP Potion")
        print("\nYou used an SP Potion and restored 20 SP.")
    else:
        print("\nYou don't have any SP Potions!")

def enemy_turn(player, enemy, screen):
    display_bars(player, enemy, screen)
    available_skills = [skill for skill in enemy_skills if 
                        ("mp" not in enemy_skills[skill]["cost"] or enemy["mp"] >= enemy_skills[skill]["cost"]["mp"]) and
                        ("sp" not in enemy_skills[skill]["cost"] or enemy["sp"] >= enemy_skills[skill]["cost"]["sp"])]
    if not available_skills:
        print("The opponent has no available skills to use.")
        return
    
    enemy_skill = random.choice(available_skills)
    skill_cost = enemy_skills[enemy_skill]["cost"]
    
    if "mp" in skill_cost:
        enemy["mp"] -= skill_cost["mp"]
    if "sp" in skill_cost:
        enemy["sp"] -= skill_cost["sp"]
    
    enemy_skills[enemy_skill]["effect"](player, enemy)
    animate_action(f"The opponent used {enemy_skill}!", screen)
    regenerate_enemy_mp(enemy)  # Regenerate MP after enemy's turn
    regenerate_enemy_sp(enemy)  # Regenerate SP after enemy's turn

def turnwise(player, enemy, screen):
    while player.hp > 0 and enemy['hp'] > 0:
        selected_skill = player_turn(player, enemy, screen)
        if selected_skill == "run":
            print("You ran away from the battle!")
            return False
        if enemy['hp'] <= 0:
            break
        if selected_skill not in ["Teleport", "Block"]:
            enemy_turn(player, enemy, screen)
    
    if enemy['hp'] <= 0:
        return True
    elif player.hp <= 0:
        return False

def win_or_loss(player, enemy, screen):
    print("Debug: Entering win_or_loss function.")
    if turnwise(player, enemy, screen):
        regen_health = int(player.max_hp * 0.65)
        player.hp = min(player.max_hp, player.hp + regen_health)
        player.gain_xp(enemy['xp_value'])  # Gain XP based on enemy's XP value
        print(f"You regenerated {regen_health} HP. Current HP: {player.hp}")
        return "Victory!"
    else:
        print("You are on your last legs, about to die")
        return "Defeat!"
