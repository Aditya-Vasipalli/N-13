import pygame
import sys

def assign_stat_points(stat_points):
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    font = pygame.font.Font(None, 36)
    clock = pygame.time.Clock()
    stats = {"Strength": 0, "Agility": 0, "Intelligence": 0}

    while stat_points > 0:
        print(f"Debug: Starting stat allocation loop with {stat_points} stat points.")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    stats['Strength'] += 1
                    stat_points -= 1
                    print(f"Debug: Assigned 1 point to Strength. Remaining stat points: {stat_points}")
                elif event.key == pygame.K_2:
                    stats['Agility'] += 1
                    stat_points -= 1
                    print(f"Debug: Assigned 1 point to Agility. Remaining stat points: {stat_points}")
                elif event.key == pygame.K_3:
                    stats['Intelligence'] += 1
                    stat_points -= 1
                    print(f"Debug: Assigned 1 point to Intelligence. Remaining stat points: {stat_points}")

        screen.fill((0, 0, 0))
        text = font.render(f"You have {stat_points} stat points to assign.", True, (255, 255, 255))
        screen.blit(text, (50, 50))
        text = font.render("1. Strength", True, (255, 255, 255))
        screen.blit(text, (50, 100))
        text = font.render("2. Agility", True, (255, 255, 255))
        screen.blit(text, (50, 150))
        text = font.render("3. Intelligence", True, (255, 255, 255))
        screen.blit(text, (50, 200))
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    stat_points = int(sys.argv[1])
    assign_stat_points(stat_points)
