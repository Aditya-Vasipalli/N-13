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

    # Load potion icons
    mp_potion_icon = pygame.image.load('assets/mp_potion.png')
    sp_potion_icon = pygame.image.load('assets/sp_potion.png')
    mp_potion_icon = pygame.transform.scale(mp_potion_icon, (32, 32))
    sp_potion_icon = pygame.transform.scale(sp_potion_icon, (32, 32))

    # Display potion counts with icons
    mp_potion_count = character.inventory.items.count("MP Potion")
    sp_potion_count = character.inventory.items.count("SP Potion")
    mp_potion_text = font.render(f"x{mp_potion_count}", True, (255, 255, 255))
    sp_potion_text = font.render(f"x{sp_potion_count}", True, (255, 255, 255))

    screen.blit(mp_potion_icon, (50, 200))
    screen.blit(mp_potion_text, (90, 200))
    screen.blit(sp_potion_icon, (130, 200))
    screen.blit(sp_potion_text, (170, 200))

    # Display character images
    player_image = pygame.transform.scale(pygame.image.load(f"assets/{character.char_class.lower()}.png"), (40, 40))
    enemy_image = pygame.Surface((32, 32))
    enemy_image.fill((255, 0, 0))
    screen.blit(player_image, (50, 300))
    screen.blit(enemy_image, (450, 300))

def animate_action(action_text, screen):
    font = pygame.font.Font(None, 36)
    action_surface = font.render(action_text, True, (255, 255, 255))
    screen.fill((0, 0, 0))  # Clear screen
    screen.blit(action_surface, (50, 200))
    pygame.display.flip()
    pygame.time.wait(1000)  # Wait for 1000 milliseconds (1 second)

def timing_slider(screen):
    font = pygame.font.Font(None, 36)
    slider_bg = pygame.image.load('assets/slider_bg.png')
    slider_bg = pygame.transform.scale(slider_bg, (screen.get_width(), screen.get_height()))
    
    # Manually define the length and width of the slider
    slider_width = int(screen.get_width() * 0.9) - 40
    slider_height = 20
    slider_x = (screen.get_width() - slider_width - 40) // 2
    slider_y = screen.get_height() - 100
    target_width = 30
    target_x = random.randint(slider_x + 20, slider_x + slider_width - target_width)
    target_y = slider_y + 20

    slider_rect = pygame.Rect(slider_x + 20, slider_y + 20, slider_width, slider_height)
    target_rect = pygame.Rect(target_x, target_y, target_width, slider_height)
    cursor_x = slider_x + 20
    cursor_speed = 8  # Increase speed
    direction = 1

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if target_rect.collidepoint(cursor_x, slider_y + 20):
                        return True  # Hit
                    else:
                        return False  # Miss

        cursor_x += cursor_speed * direction
        if cursor_x <= slider_x + 20 or cursor_x >= slider_x + slider_width - 10:
            direction *= -1

        screen.blit(slider_bg, (0, 0))
        pygame.draw.rect(screen, (255, 0, 0), slider_rect)
        pygame.draw.rect(screen, (0, 255, 0), target_rect)
        pygame.draw.rect(screen, (255, 255, 255), (cursor_x, slider_y + 20, 10, slider_height))  # White slider
        text = font.render("Press SPACE to stop the slider!", True, (0, 0, 0))
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
    
    options = [f"{skill} (MP: {player_skills[skill]['cost'].get('mp', 0)}, SP: {player_skills[skill]['cost'].get('sp', 0)})" for skill in player.skills]
    options.append("Use MP Potion")
    options.append("Use SP Potion")
    
    option_rects = []
    for i, option in enumerate(options):
        text = font.render(option, True, (255, 255, 255))
        rect = text.get_rect(topleft=(50, 350 + i * 50))
        option_rects.append((rect, option))
        # Draw semi-transparent rounded box
        box_color = (255, 255, 255, 128)  # Semi-transparent white
        box_surface = pygame.Surface((rect.width + 20, rect.height + 10), pygame.SRCALPHA)
        pygame.draw.rect(box_surface, box_color, box_surface.get_rect(), border_radius=10)
        screen.blit(box_surface, (rect.x - 10, rect.y - 5))
        screen.blit(text, rect)
    
    pygame.display.flip()
    
    selected_skill = None  # Initialize selected_skill to None
    hover_description = None  # Initialize hover_description to None
    
    player.apply_lingering_effects()  # Apply lingering effects at the start of the turn
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for rect, option in option_rects:
                    if rect.collidepoint(mouse_pos):
                        if option.startswith("Use MP Potion"):
                            use_mp_potion(player)
                            if bullet_hell(screen):
                                animate_action("You dodged the attack!", screen)
                            else:
                                animate_action("You were hit while using the potion!", screen)
                            return None
                        elif option.startswith("Use SP Potion"):
                            use_sp_potion(player)
                            if bullet_hell(screen):
                                animate_action("You dodged the attack!", screen)
                            else:
                                animate_action("You were hit while using the potion!", screen)
                            return None
                        else:
                            selected_skill = option.split(" (")[0]
                        break

        if selected_skill:
            skill_cost = player_skills[selected_skill]["cost"]
            if player.mp >= skill_cost.get("mp", 0) and player.sp >= skill_cost.get("sp", 0):
                player.mp -= skill_cost.get("mp", 0)
                player.sp -= skill_cost.get("sp", 0)
                if timing_slider(screen):
                    animate_action(f"\nYou used {selected_skill}!", screen)
                    player_skills[selected_skill]["effect"](player, enemy)
                    if selected_skill == "Cure":
                        player.remove_lingering_effects()  # Remove lingering effects if Cure is used
                else:
                    animate_action("\nYou missed!", screen)
            else:
                animate_action("\nNot enough MP or SP!", screen)
            player.regenerate_mp()  # Regenerate MP after player's turn
            player.regenerate_sp()  # Regenerate SP after player's turn
            show_regeneration(screen, player.name, player.mp, player.sp)  # Show regeneration
            return selected_skill

        # Update hover effect
        mouse_pos = pygame.mouse.get_pos()
        for rect, option in option_rects:
            if rect.collidepoint(mouse_pos):
                skill_name = option.split(" (")[0]
                if skill_name in player_skills:
                    description = player_skills[skill_name]["description"]
                    hover_description = font.render(description, True, (255, 255, 255))
                    screen.blit(hover_description, (rect.x, rect.y - 30))
                    pygame.display.flip()
                    break
        else:
            if hover_description:
                screen.fill((0, 0, 0))  # Clear screen
                display_bars(player, enemy, screen)
                screen.blit(font.render("It's Your turn!", True, (255, 255, 255)), (50, 250))
                screen.blit(font.render("Choose your move:", True, (255, 255, 255)), (50, 300))
                for rect, option in option_rects:
                    text = font.render(option, True, (255, 255, 255))
                    box_color = (255, 255, 255, 128)  # Semi-transparent white
                    box_surface = pygame.Surface((rect.width + 20, rect.height + 10), pygame.SRCALPHA)
                    pygame.draw.rect(box_surface, box_color, box_surface.get_rect(), border_radius=10)
                    screen.blit(box_surface, (rect.x - 10, rect.y - 5))
                    screen.blit(text, rect)
                pygame.display.flip()
                hover_description = None

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

def bullet_hell(screen):
    font = pygame.font.Font(None, 36)
    bullet_hell_bg = pygame.image.load('assets/bullet_hell_bg.png')
    bullet_hell_bg = pygame.transform.scale(bullet_hell_bg, (screen.get_width(), screen.get_height()))
    player_image = pygame.image.load('assets/bullet_hell.png')
    player_image = pygame.transform.scale(player_image, (60, 60))
    player_rect = player_image.get_rect(center=(screen.get_width() // 2, screen.get_height() - 50))
    bullets = []
    bullet_speed = 9  # Increase bullet speed
    player_speed = 6  # Increase player speed
    dodge_time = 5  # Time to dodge in seconds
    start_time = time.time()

    while time.time() - start_time < dodge_time:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_rect.x -= player_speed
        if keys[pygame.K_RIGHT]:
            player_rect.x += player_speed
        if keys[pygame.K_UP]:
            player_rect.y -= player_speed
        if keys[pygame.K_DOWN]:
            player_rect.y += player_speed

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Add new bullets
        if random.random() < 0.3:  # Increase bullet frequency
            bullet_x = random.randint(0, screen.get_width() - 10)
            bullets.append(pygame.Rect(bullet_x, 0, 10, 30))  # Make bullets three times longer

        # Move bullets
        for bullet in bullets:
            bullet.y += bullet_speed

        # Check for collisions
        for bullet in bullets:
            if player_rect.colliderect(bullet):
                return False  # Hit

        # Remove off-screen bullets
        bullets = [bullet for bullet in bullets if bullet.y < screen.get_height()]

        # Draw everything
        screen.blit(bullet_hell_bg, (0, 0))
        screen.blit(player_image, player_rect.topleft)
        for bullet in bullets:
            pygame.draw.rect(screen, (255, 0, 0), bullet)
        text = font.render("Dodge the bullets for 5 seconds!", True, (255, 255, 255))
        screen.blit(text, (50, 50))
        pygame.display.flip()
        pygame.time.Clock().tick(60)

    return True  # Successfully dodged

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
    
    if bullet_hell(screen):
        animate_action("You dodged the attack!", screen)
    else:
        animate_action(f"The opponent used {enemy_skill}!", screen)
        enemy_skills[enemy_skill]["effect"](player, enemy)
    
    regenerate_enemy_mp(enemy)  # Regenerate MP after enemy's turn
    regenerate_enemy_sp(enemy)  # Regenerate SP after enemy's turn
    show_regeneration(screen, enemy["name"], enemy["mp"], enemy["sp"], enemy=True)  # Show regeneration
    
    player.apply_lingering_effects()  # Apply lingering effects at the start of the turn

def show_regeneration(screen, name, mp, sp, enemy=False):
    font = pygame.font.Font(None, 36)
    mp_text = font.render(f"{name} regenerated MP to {mp}", True, (255, 255, 255))
    sp_text = font.render(f"{name} regenerated SP to {sp}", True, (255, 255, 255))
    if enemy:
        screen.blit(mp_text, (screen.get_width() - 300, 50))
        screen.blit(sp_text, (screen.get_width() - 300, 80))
    else:
        screen.blit(mp_text, (50, screen.get_height() - 100))
        screen.blit(sp_text, (50, screen.get_height() - 70))
    pygame.display.flip()
    pygame.time.wait(1000)  # Show for 1 second

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
        
        # Display victory image
        victory_image = pygame.image.load('assets/victory.png')
        victory_image = pygame.transform.scale(victory_image, (screen.get_width(), screen.get_height()))
        screen.blit(victory_image, (0, 0))
        pygame.display.flip()
        pygame.time.wait(2000)  # Display for 2 seconds
        
        return "Victory!"
    else:
        print("You are on your last legs, about to die")
        return "Defeat!"

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Combat System Debug")

    # Create a test player and enemy
    player_stats = {"Strength": 10, "Agility": 5, "Intelligence": 3}
    player_skills = ["Slash", "Block", "Cure"]
    player = Character("Hero", "Warrior", player_stats, player_skills)
    
    enemy = {
        "name": "Goblin",
        "hp": 50,
        "mp": 20,
        "sp": 20,
        "attack": 5,
        "xp_value": 50
    }

    # Start the fight
    result = win_or_loss(player, enemy, screen)
    print(result)

if __name__ == "__main__":
    main()
