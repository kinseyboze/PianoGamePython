import pygame
import pygame.midi

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 150, 255)
BACK = (115, 147, 179)

class Piano:
    
    sounds = {}
    white_notes = ["C3","D3","E3","F3", "G3", "A3", "B3", "C4", "D4", "E4", "F4", "G4", "A4", "B4", "C5"]
    black_notes = ["Db3","Eb3","Gb3", "Ab3", "Bb3", "Db4", "Eb4", "Gb4", "Ab4", "Bb4"]

    def __init__(self):
        pygame.init()
        
        # sound stuff
        pygame.mixer.init()
        
        def load_sound(key, filename):
            try:
                self.sounds[key] = pygame.mixer.Sound(filename)
            except pygame.error as message:
                print('Cannot load sound:', filename)
                raise SystemExit(message)

        for i in self.white_notes:
            load_sound(i, f"assets/sounds/{i}.wav")  

        for i in self.black_notes:
            load_sound(i, f"assets/sounds/{i}.wav")
        
        self.screen = pygame.display.set_mode((1200, 900))
        pygame.display.set_caption("Piano Game")
        self.white_keys = []
        self.black_keys = []
        self.create_keys()

        # Initialize MIDI if available
        self.midi_input = None
        self.init_midi()

    def create_keys(self):
        white_key_width = 70
        white_key_height = 300
        black_key_width = 35
        black_key_height = 180

        # Create white keys
        for i in range(15):  # C3 to C5 (15 keys)
            rect = pygame.Rect((i * white_key_width) + 80, 500, white_key_width, white_key_height)
            self.white_keys.append(rect)

        # Create black keys (skip E and B)
        skip = [2, 6, 9, 13, 14]  # Indices after which there are no black keys
        for i in range(15):
            if i not in skip:
                rect = pygame.Rect(((i + 1) * white_key_width - black_key_width // 2) + 80, 500, black_key_width, black_key_height)
                self.black_keys.append(rect)

    def draw_keys(self, pressed_white, pressed_black):
        self.screen.fill(BACK)

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

                    # Check black keys first 
                    for i, rect in enumerate(self.black_keys):
                        if rect.collidepoint(event.pos):
                            pressed_black = i
                            self.sounds[self.black_notes[i]].play()
                            break

                    # If no black key was clicked, check white keys
                    if pressed_black == -1:
                        for i, rect in enumerate(self.white_keys):
                            if rect.collidepoint(event.pos):
                                pressed_white = i
                                self.sounds[self.white_notes[i]].play()
                                break

                elif event.type == pygame.MOUSEBUTTONUP:
                    pressed_white = -1
                    pressed_black = -1

            # Process MIDI input if available
            if self.midi_input and self.midi_input.poll():
                for midi_event in self.midi_input.read(10):
                    data = midi_event[0]
                    status, note_num, velocity = data[:3]
                    if status == 144 and velocity > 0:  # Note On
                        note_name = self.midi_note_to_name(note_num)
                        if note_name:
                            self.sounds[note_name].play()
                    elif status == 128 or (status == 144 and velocity == 0):  # Note Off
                        note_name = self.midi_note_to_name(note_num)
                        if note_name and note_name in self.sounds:
                            self.sounds[note_name].fadeout(300)

    def init_midi(self):
        try:
            if not pygame.midi.get_init():
                pygame.midi.init()

            device_count = pygame.midi.get_count()
            for i in range(device_count):
                info = pygame.midi.get_device_info(i)
                interface, name, is_input, is_output, opened = info
                if is_input:
                    self.midi_input = pygame.midi.Input(i)
                    print(f"MIDI input initialized on device {i}: {name.decode()}")
                    break
            else:
                print("No MIDI input device found.")
        except Exception as e:
            print(f"MIDI initialization failed: {e}")


    def midi_note_to_name(self, midi_note):
        midi_to_note = {
            48: "C3", 49: "Db3", 50: "D3", 51: "Eb3", 52: "E3", 53: "F3", 54: "Gb3",
            55: "G3", 56: "Ab3", 57: "A3", 58: "Bb3", 59: "B3", 60: "C4", 61: "Db4",
            62: "D4", 63: "Eb4", 64: "E4", 65: "F4", 66: "Gb4", 67: "G4", 68: "Ab4",
            69: "A4", 70: "Bb4", 71: "B4", 72: "C5"
        }
        return midi_to_note.get(midi_note, None)
