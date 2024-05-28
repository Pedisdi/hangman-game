from .hangman_game import HangmanGame


def main():
    game = HangmanGame()
    try:
        game.play()
    except IndexError:
        exit()


if __name__ == '__main__':
    main()
