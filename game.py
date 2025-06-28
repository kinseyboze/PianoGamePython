import pygame
from piano import Piano

class Game:
    def __init__(self):
        self.piano = Piano()
        self.sequence = ["G4", "Gb4", "B4", "E4"] 
        self.input_index = 0
        self.font = pygame.font.SysFont(None, 48)

    def display_sequence(self):
        text_surface = self.font.render("Play this: " + " ".join(self.sequence), True, (255, 255, 255))
        self.piano.screen.blit(text_surface, (50, 50))

    def run(self):
        running = True
        pressed_white = -1
        pressed_black = -1

        while running:
            self.piano.draw_keys(pressed_white, pressed_black)
            self.display_sequence()
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pressed_white = -1
                    pressed_black = -1

                    # Check black keys first
                    for i, rect in enumerate(self.piano.black_keys):
                        if rect.collidepoint(event.pos):
                            note = self.piano.black_notes[i]
                            pressed_black = i
                            self.piano.sounds[note].play()
                            self.check_note(note)
                            break

                    if pressed_black == -1:
                        for i, rect in enumerate(self.piano.white_keys):
                            if rect.collidepoint(event.pos):
                                note = self.piano.white_notes[i]
                                pressed_white = i
                                self.piano.sounds[note].play()
                                self.check_note(note)
                                break

                elif event.type == pygame.MOUSEBUTTONUP:
                    pressed_white = -1
                    pressed_black = -1

    def check_note(self, note):
        expected = self.sequence[self.input_index]
        if note == expected:
            print(f"Correct: {note}")
            self.input_index += 1
            if self.input_index == len(self.sequence):
                print("Sequence complete!")
                self.input_index = 0  # Or load a new sequence
        else:
            print(f"Wrong note! Expected {expected}, got {note}")
            self.input_index = 0  # Reset progress


# Only run this if it's the main file
if __name__ == "__main__":
    game = Game()
    game.run()
