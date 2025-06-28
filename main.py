from piano import Piano
from game import Game

def main():
    mode = input("Choose mode (piano/game): ").strip().lower()

    if mode == "game":
        game = Game()
        game.run()
    else:
        piano = Piano()
        piano.play()

if __name__ == "__main__":
    main()
