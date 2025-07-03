import pygame
import pygame.midi
import menu
import random
from piano import Piano

class Game:
    
    NOTE_SEQUENCES = [
    ["C4", "E4", "G4", "C5"],
    ["D4", "F4", "A4"],
    ["E4", "B4"],
    ["G3", "B3", "D4", "G4"],
    ["F3", "A3", "C4", "F4"],
    ["A3", "C4", "E4", "A4"],
    ["G4", "Gb4", "B4", "E4"],
    ["G4", "Bb4", "C5", "Eb4"],           
    ["E4", "Eb4", "E4", "Eb4", "E4", "B3", "C4", "A3"],  
    ["E4", "E4", "F4", "G4", "G4", "F4", "E4", "D4"],   
    ["C4", "C4", "G4", "G4", "A4", "A4", "G4"],         
    ["G3", "Bb3", "C4", "G3", "Bb3", "Db4"],             
    ["G4", "G4", "A4", "G4", "C5", "B4"],                
    ["C4", "D4", "E4", "F4", "G4"],                       
    ["A3", "B3", "C4", "D4", "E4"],                       
    ["C4", "E4", "G4", "C5"],
    ]
    
    def __init__(self):
        self.piano = Piano()
        self.sequence = random.choice(Game.NOTE_SEQUENCES)
        self.input_index = 0
        self.font = pygame.font.SysFont(None, 36)

        self.treble_clef = pygame.image.load("assets/images/treble.png").convert_alpha()
        self.treble_clef = pygame.transform.smoothscale(self.treble_clef, (80, 180))

        self.bass_clef = pygame.image.load("assets/images/bass.png").convert_alpha()
        self.bass_clef = pygame.transform.smoothscale(self.bass_clef, (80, 180))
        
        self.back_button = pygame.Rect(20, 20, 100, 40)
        self.button_font = pygame.font.SysFont(None, 32)

    def is_treble(self, note):
        # Notes C4 and higher go on treble clef
        return note[-1].isdigit() and int(note[-1]) >= 4

    def get_note_y(self, note, spacing):
        treble_positions = {
            "F5": 0, "E5": 1, "D5": 2, "C5": 3, "B4": 4, "Bb4": 4.5, "A4": 5, "Ab4": 5.5,
            "G4": 6, "Gb4": 6.5, "F4": 7, "E4": 8, "Eb4": 8, "D4": 9, "Db4": 9, "C4": 10
        }
        bass_positions = {
            "A3": 0, "Ab3": 0, "G3": 1, "Gb3": 1, "F3": 2, "E3": 3, "Eb3": 3,
            "D3": 4, "Db3": 4, "C3": 5, "B3": -1, "Bb3": -1
        }

        if self.is_treble(note):
            base_y = 150
            step = treble_positions.get(note, 10)
        else:
            base_y = 350
            step = bass_positions.get(note, 5)

        return base_y + step * (spacing / 2)

    def draw_sheet_music(self):
        treble_y = 150
        bass_y = 350
        line_spacing = 25
        note_spacing = 80
        start_x = 100

        # Draw staff lines
        for i in range(5):
            pygame.draw.line(self.piano.screen, (0, 0, 0),
                             (start_x, treble_y + i * line_spacing),
                             (start_x + 1000, treble_y + i * line_spacing), 2)
            pygame.draw.line(self.piano.screen, (0, 0, 0),
                             (start_x, bass_y + i * line_spacing),
                             (start_x + 1000, bass_y + i * line_spacing), 2)

        # Draw clefs
        self.piano.screen.blit(self.treble_clef, (start_x + 10, treble_y - 35))
        self.piano.screen.blit(self.bass_clef, (start_x + 10, bass_y - 35))

        # Draw notes
        for idx, note in enumerate(self.sequence):
            x = start_x + 150 + idx * note_spacing
            y = self.get_note_y(note, line_spacing)
            color = (0, 255, 0) if idx == self.input_index else (0, 0, 0)
            pygame.draw.circle(self.piano.screen, color, (x, int(y)), 12)
            label = self.font.render(note, True, (0, 0, 0))
            self.piano.screen.blit(label, (x - 18, int(y) + 20))

    def check_note(self, note):
        expected = self.sequence[self.input_index]
        if note == expected:
            print(f"Correct: {note}")
            self.input_index += 1
            if self.input_index == len(self.sequence):
                print("Sequence complete!")
                self.input_index = 0
                self.sequence = random.choice(Game.NOTE_SEQUENCES)
        else:
            print(f"Wrong note! Expected {expected}, got {note}")
            self.input_index = 0

    def run(self):
        running = True
        pressed_white = -1
        pressed_black = -1

        while running:
            self.piano.draw_keys(pressed_white, pressed_black)
            self.draw_sheet_music()
            
            # Draw back button
            pygame.draw.rect(self.piano.screen, (200, 0, 0), self.back_button)
            back_text = self.button_font.render("Back", True, (255, 255, 255))
            self.piano.screen.blit(back_text, (self.back_button.x + 20, self.back_button.y + 8))
            
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pressed_white = -1
                    pressed_black = -1
                    
                    if self.back_button.collidepoint(event.pos):
                        running = False
                        if pygame.midi.get_init():
                            pygame.midi.quit()
                        menu.start_menu()
                        return

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

            # MIDI input
            if self.piano.midi_input and self.piano.midi_input.poll():
                for midi_event in self.piano.midi_input.read(10):
                    data = midi_event[0]
                    status, note_num, velocity = data[:3]
                    if status == 144 and velocity > 0:
                        note_name = self.piano.midi_note_to_name(note_num)
                        if note_name:
                            self.piano.sounds[note_name].play()
                            self.check_note(note_name)
                    elif status == 128 or (status == 144 and velocity == 0):
                        note_name = self.piano.midi_note_to_name(note_num)
                        if note_name in self.piano.sounds:
                            self.piano.sounds[note_name].fadeout(300)
