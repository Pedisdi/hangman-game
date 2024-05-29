import logging
from .hangman_game import HangmanGame
from . import exceptions as ex


def main():
    game = HangmanGame()
    try:
        game.play()
    except ex.CanNotSetWord as e:
        logging.error(e)
        exit()


if __name__ == '__main__':
    main()
