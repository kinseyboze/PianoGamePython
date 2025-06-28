import pygame
from piano import Piano

class Game:
    def __init__(self):
        self.piano = Piano()
        self.sequence = ["G4", "Gb4", "B4", "E4"]
        self.input_index = 0
        self.font = pygame.font.SysFont(None, 48)

    def draw_sheet_music(self):
        start_x = 100
        start_y = 200  # Y position of the top staff line (F5)
        line_spacing = 25
        note_spacing = 70

        # Draw 5 staff lines (top line = F5)
        for i in range(5):
            y = start_y + i * line_spacing
            pygame.draw.line(self.piano.screen, (0, 0, 0), (start_x, y), (start_x + 1000, y), 2)

        # Draw note circles and labels
        for idx, note in enumerate(self.sequence):
            x = start_x + 150 + idx * note_spacing
            y = self.get_note_y(note, start_y, line_spacing)
            color = (0, 255, 0) if idx == self.input_index else (255, 255, 255)
            pygame.draw.circle(self.piano.screen, color, (x, int(y)), 10)
            label = self.font.render(note, True, (255, 255, 255))
            self.piano.screen.blit(label, (x - 20, int(y) + 20))

    def get_note_y(self, note, top_y, spacing):
        """
        Map notes to vertical positions on the treble clef staff.
        top_y: y-position of the top staff line (F5)
        spacing: distance between staff lines
        """

        # Each step represents a line or space (lines=even, spaces=odd), counting from top line (F5) = 0
        note_steps = {
            "F5": 0,
            "E5": 1,
            "D5": 2,
            "C5": 3,
            "B4": 4,
            "Bb4": 4,
            "A4": 5,
            "Ab4": 5,
            "G4": 6,
            "Gb4": 6,
            "F4": 7,
            "E4": 8,
            "Eb4": 8,
            "D4": 9,
            "Db4": 9,
            "C4": 10,
            "B3": 11,
            "Bb3": 11,
            "A3": 12,
            "Ab3": 12,
            "G3": 13,
            "Gb3": 13,
            "F3": 14,
        }

        step = note_steps.get(note)
        if step is None:
            # Default to middle line B4 if unknown
            step = 4
        # Each step moves half the line spacing (since lines and spaces alternate)
        y = top_y + step * (spacing / 2)
        return y

    def run(self):
        running = True
        pressed_white = -1
        pressed_black = -1

        while running:
            self.piano.draw_keys(pressed_white, pressed_black)
            self.draw_sheet_music()
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
                self.input_index = 0  # Reset or load new sequence here
        else:
            print(f"Wrong note! Expected {expected}, got {note}")
            self.input_index = 0  # Reset progress
