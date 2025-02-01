from enemies import enemies
import pygame
import sys
import logging
class Player:
    def __init__(self, name, player_class):
        self.name = name
        self.player_class = player_class
        self.level = 1
        self.xp = 0
        self.hp = 100  # Default HP; you can adjust based on class
        self.xp_threshold = 100  # XP required to level up
        self.mp = self.calculate_mp()
        self.sp = self.calculate_sp()
        self.max_mp = self.mp
        self.max_sp = self.sp

    def calculate_mp(self):
        base_mp = 1
        mp = base_mp + (self.stats['Intelligence'] * 5)  # Example multiplier
        return mp

    def calculate_sp(self):
        base_sp = 1
        sp = base_sp + (self.stats['Agility'] * 5)  # Example multiplier
        return sp

    def regenerate_mp(self):
        regen_amount = 5  # Example regeneration amount
        if self.mp < self.max_mp:
            self.mp = min(self.max_mp, self.mp + regen_amount)
            print(f"{self.name} regenerated {regen_amount} MP. Current MP: {self.mp}")

    def regenerate_sp(self):
        regen_amount = 5  # Example regeneration amount
        if self.sp < self.max_sp:
            self.sp = min(self.max_sp, self.sp + regen_amount)
            print(f"{self.name} regenerated {regen_amount} SP. Current SP: {self.sp}")

    def gain_xp(self, xp_gained):
        print(f"{self.name} gained {xp_gained} XP!")
        self.xp += xp_gained
        self.check_level_up()

    def check_level_up(self):
        while self.xp >= self.xp_threshold:
            self.xp -= self.xp_threshold
            self.level += 1
            self.hp += 20  # Increase HP by 20 on level up; adjust as needed
            self.max_hp = self.hp
            self.mp = self.calculate_mp()  # Recalculate MP on level up
            self.max_mp = self.mp
            self.sp = self.calculate_sp()  # Recalculate SP on level up
            self.max_sp = self.sp
            self.xp_threshold = int(self.xp_threshold * 1.5)  # Increase XP threshold for next level
            self.stat_points += 1  # Grant 1 stat point per level
            if self.level % 5 == 0:
                self.stat_points += 5  # Grant 5 additional stat points every 5 levels
                self.learn_new_move()
            logging.debug(f"{self.name} leveled up to level {self.level}!")
            print(f"{self.name} leveled up to level {self.level}!")
            print(f"HP increased to {self.hp}. MP increased to {self.mp}. SP increased to {self.sp}.")
            print(f"XP needed for next level: {self.xp_threshold}")
            print(f"You have {self.stat_points} stat points to assign.")
            self.display_level_up_screen()

    def display_level_up_screen(self):
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        font = pygame.font.Font(None, 36)
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return

            screen.fill((0, 0, 0))
            text = font.render(f"{self.name} leveled up to level {self.level}!", True, (255, 255, 255))
            screen.blit(text, (50, 50))
            text = font.render(f"HP increased to {self.hp}.", True, (255, 255, 255))
            screen.blit(text, (50, 100))
            text = font.render(f"XP needed for next level: {self.xp_threshold}", True, (255, 255, 255))
            screen.blit(text, (50, 150))
            text = font.render(f"You have {self.stat_points} stat points to assign.", True, (255, 255, 255))
            screen.blit(text, (50, 200))
            if self.level % 5 == 0:
                text = font.render("You have learned a new move!", True, (255, 255, 255))
                screen.blit(text, (50, 250))
            text = font.render("Press Enter to continue", True, (255, 255, 255))
            screen.blit(text, (50, 300))
            pygame.display.flip()
            clock.tick(60)

    def draw(self, screen, image, position):
        screen.blit(image, position)

class Enemy:
    def __init__(self, name, xp_value):
        self.name = name
        self.xp_value = xp_value

# Example enemies with different XP values


# Example of gameplay
if __name__ == "__main__":
    player = Player("Hero", "Warrior")
    player.stats = {"Strength": 10, "Agility": 5, "Intelligence": 3}  # Example initial stats
    for enemy in enemies:
        print(f"Defeated {enemy.name} and gained {enemy.xp_value} XP!")
        player.gain_xp(enemy.xp_value)