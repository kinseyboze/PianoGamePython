# menu.py

import pygame
import sys
from piano import Piano

def start_menu():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Piano Game - Start Menu")
    font = pygame.font.SysFont(None, 72)
    freeplay_font = pygame.font.SysFont(None, 50)

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BLUE = (0, 150, 255)

    running = True
    while running:
        screen.fill(BLACK)

        title = font.render("Piano Practice Game", True, WHITE)
        screen.blit(title, (250, 100))

        play_button = pygame.Rect(300, 300, 200, 80)
        pygame.draw.rect(screen, BLUE, play_button)
        play_text = font.render("PLAY", True, BLACK)
        screen.blit(play_text, (play_button.x + 35, play_button.y + 10))
        
        
        freeplay_button = pygame.Rect(300, 410, 200, 80)
        pygame.draw.rect(screen, BLUE, freeplay_button)
        freeplay_text = freeplay_font.render("FREEPLAY", True, BLACK)
        screen.blit(freeplay_text, (freeplay_button.x + 5, freeplay_button.y + 10))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    pygame.quit()
                    Piano().play()
                elif freeplay_button.collidepoint(event.pos):
                    pygame.quit()
                    Piano.play()
