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
    pygame.time.wait(300)  # Wait for 300 milliseconds

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
                # elif event.key == pygame.K_4 and len(player.skills) > 3:
                #     selected_skill = player.skills[3]
                elif event.key == pygame.K_4:
                    use_mp_potion(player)
                    if bullet_hell(screen):
                        animate_action("You dodged the attack!", screen)
                    else:
                        animate_action("You were hit while using the potion!", screen)
                    return None
                elif event.key == pygame.K_5:
                    use_sp_potion(player)
                    if bullet_hell(screen):
                        animate_action("You dodged the attack!", screen)
                    else:
                        animate_action("You were hit while using the potion!", screen)
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
                    player.regenerate_mp()  # Regenerate MP after player's turn
                    player.regenerate_sp()  # Regenerate SP after player's turn
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
