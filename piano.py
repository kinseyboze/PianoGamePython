import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

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
            rect = pygame.Rect  ((i * white_key_width)+100, 350, white_key_width, white_key_height)
            self.white_keys.append(rect)

        # Create black keys (skip E and B)
        skip = [2, 6, 9, 13]  # No black keys after E (index 2) and B (index 6)
        for i in range(14):  # 5 black keys total
            if i not in skip:
                rect = pygame.Rect(     ((i + 1) * white_key_width - black_key_width // 2) + 100 , 350, black_key_width, black_key_height)
                self.black_keys.append(rect)

    def draw_keys(self):
        self.screen.fill((0, 0, 0))  # Background black
        for rect in self.white_keys:
            pygame.draw.rect(self.screen, WHITE, rect)
            pygame.draw.rect(self.screen, BLACK, rect, 2)  # Outline

        for rect in self.black_keys:
            pygame.draw.rect(self.screen, BLACK, rect)

    def play(self):
        running = True
        while running:
            self.draw_keys()
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
