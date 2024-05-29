import logging
import random
import requests

from . import exceptions as ex
from . import constants as c


class HangmanGame:

    def __init__(self):
        self.remained_try = 0
        self.word = ''
        self.guessed_letters = {}

    @staticmethod
    def get_word_from_api() -> str | None:
        # TODO: https://requests.readthedocs.io/en/latest/user/quickstart/#errors-and-exceptions

        try:
            response = requests.get(c.API_URL, params=c.PAYLOAD, headers=c.API_KEY, timeout=1.5)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logging.error(e)
            return None
        else:
            return response.json()['word']

    @staticmethod
    def get_word_from_offline_word_list() -> str | None:
        # TODO: IndexError
        if c.OFFLINE_WORD_LIST:
            return random.choice(c.OFFLINE_WORD_LIST)
        return None
        # raise IndexError('Offline word list is empty.')

    def set_word(self):
        word = (self.get_word_from_api() or self.get_word_from_offline_word_list())

        if not word:
            raise ex.CanNotSetWord('Can not set word both with api and offline ways')
        self.word = word.strip().upper()

    def setup_game(self):
        """
        :raise:  CanNotSetWord
        """
        self.set_word()
        self.guessed_letters = {str(i + 1): None for i in range(len(self.word))}
        self.remained_try = len(self.word) * 3

    def is_finished(self) -> str:
        if all([letter is not None for letter in self.guessed_letters.values()]):
            return 'win'
        elif self.remained_try == 0:
            return 'lose'
        raise ex.GameNotFinishedError

    def reset_game(self):
        self.remained_try = 0
        self.word = ''
        self.guessed_letters = {}

    def get_guessed_letters_str(self) -> str:
        return ' '.join([letter if letter else place for place, letter in self.guessed_letters.items()])

    def evaluate_guess(self, place, letter):
        self.remained_try -= 1
        if self.word[int(place) - 1] == letter:
            self.guessed_letters[place] = letter
        else:
            raise ex.WrongGuessError("Your guess was wrong, try again")

    def replay(self, answer):
        if answer == 'y':
            self.reset_game()
            self.play()

    def play(self):
        if not self.word:  # ?? where should I check this condition? (inside the method or here)
            self.setup_game()

        while True:
            logging.warning(self.word)  # TODO: delete
            print(f'\nremained try: {self.remained_try}')
            print(f"guessed_letters: {self.get_guessed_letters_str()}")
            try:
                place = input('place: ').strip()
                place = self.is_valid_place(place)  # Error -> play()
                letter = input('letter: ').strip()
                letter = self.is_valid_letter(letter)  # Error -> play()
                self.evaluate_guess(place, letter)  # Error -> finish() -> GameNotFinishedError -> play()
            except ex.InvalidInputError as e:
                print(e)
                continue
            except ex.WrongGuessError as e:
                print(e)
            try:
                result = self.is_finished()
            except ex.GameNotFinishedError:
                continue
            print(f"You {result}!")
            break
        answer = input('Do you want to play again?(y/n) ').strip().lower()
        self.replay(answer)

    def is_valid_place(self, place: str) -> str:
        if place in self.guessed_letters and self.guessed_letters[place] is None:
            return place
        elif place not in self.guessed_letters:
            raise ex.InvalidInputError('Invalid place')
        raise ex.InvalidInputError("You've already guessed this letter correctly")

    @staticmethod
    def is_valid_letter(letter):
        if letter.isalpha() and len(letter) == 1:
            return letter.upper()
        raise ex.InvalidInputError('Letter should be an single alphabetic character.')


if __name__ == '__main__':
    g = HangmanGame()
    try:
        g.play()
    except ex.CanNotSetWord:
        exit()
