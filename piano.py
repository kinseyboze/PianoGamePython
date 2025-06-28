import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 150, 255)

class Piano:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1200, 900))
        pygame.display.set_caption("Visual Piano")
        self.white_keys = []
        self.black_keys = []
        self.create_keys()

    def create_keys(self):
        white_key_width = 70
        white_key_height = 300
        black_key_width = 35
        black_key_height = 180

        # Create white keys
        for i in range(14):  # C to B
            rect = pygame.Rect((i * white_key_width) + 100, 350, white_key_width, white_key_height)
            self.white_keys.append(rect)

        # Create black keys (skip E and B)
        skip = [2, 6, 9, 13]  # Indices after which there are no black keys
        for i in range(14):
            if i not in skip:
                rect = pygame.Rect(((i + 1) * white_key_width - black_key_width // 2) + 100, 350, black_key_width, black_key_height)
                self.black_keys.append(rect)

    def draw_keys(self, pressed_white, pressed_black):
        self.screen.fill(BLACK)

        for i, rect in enumerate(self.white_keys):
            color = BLUE if i == pressed_white else WHITE
            pygame.draw.rect(self.screen, color, rect)
            pygame.draw.rect(self.screen, BLACK, rect, 2)

        for i, rect in enumerate(self.black_keys):
            color = BLUE if i == pressed_black else BLACK
            pygame.draw.rect(self.screen, color, rect)

    def play(self):
        running = True
        pressed_white = -1
        pressed_black = -1

        while running:
            self.draw_keys(pressed_white, pressed_black)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pressed_white = -1
                    pressed_black = -1

                    # Check black keys first (they sit on top visually)
                    for i, rect in enumerate(self.black_keys):
                        if rect.collidepoint(event.pos):
                            pressed_black = i
                            break

                    # If no black key was clicked, check white keys
                    if pressed_black == -1:
                        for i, rect in enumerate(self.white_keys):
                            if rect.collidepoint(event.pos):
                                pressed_white = i
                                break

                elif event.type == pygame.MOUSEBUTTONUP:
                    pressed_white = -1
                    pressed_black = -1
