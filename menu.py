import pygame
import sys
from game import Game
from freeplay import Freeplay

def start_menu():
    pygame.init()
    screen = pygame.display.set_mode((1200, 900))
    pygame.display.set_caption("Piano Game - Start Menu")

    # Fonts
    title_font = pygame.font.SysFont("georgia", 80)
    button_font = pygame.font.SysFont("arial", 50)

    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BLUE = (0, 150, 255)
    HOVER_BLUE = (0, 180, 255)

    # Icons
    treble_icon = pygame.image.load("assets/images/treble.png")
    treble_icon = pygame.transform.smoothscale(treble_icon, (60, 120))
    
    bass_icon = pygame.image.load("assets/images/bass.png")
    bass_icon = pygame.transform.smoothscale(bass_icon, (60, 105))

    def draw_button(rect, text, icon, hovered):
        color = HOVER_BLUE if hovered else BLUE
        pygame.draw.rect(screen, color, rect, border_radius=15)
        screen.blit(icon, (rect.x - 70, rect.y - 10))
        label = button_font.render(text, True, BLACK)
        screen.blit(label, (rect.x + (rect.width - label.get_width()) // 2, rect.y + 15))

    running = True
    while running:
        screen.fill((20, 20, 30))  # Dark blue-gray background

        # Title
        title_text = title_font.render("Piano Practice Game", True, WHITE)
        screen.blit(title_text, ((screen.get_width() - title_text.get_width()) // 2, 120))

        # Buttons
        play_button = pygame.Rect(500, 350, 235, 100)
        freeplay_button = pygame.Rect(500, 500, 235, 100)

        mouse_pos = pygame.mouse.get_pos()

        draw_button(play_button, "SIGHTREAD", treble_icon, play_button.collidepoint(mouse_pos))
        draw_button(freeplay_button, "FREEPLAY", bass_icon, freeplay_button.collidepoint(mouse_pos))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    pygame.quit()
                    Game().run()
                elif freeplay_button.collidepoint(event.pos):
                    pygame.quit()
                    Freeplay().play()
