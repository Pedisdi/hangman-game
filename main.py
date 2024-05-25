import logging
import random

import requests
import json


class HangmanGame:
    offline_word_list = ['apple', 'book']

    def __init__(self):
        self.remained_try = 0
        self.word = ''
        self.guessed_letters = {}

    @staticmethod
    def get_word_from_api() -> str:
        # TODO: https://requests.readthedocs.io/en/latest/user/quickstart/#errors-and-exceptions

        api_url = 'https://api.api-ninjas.com/v1/randomword'
        key = {'X-Api-Key': '/lMrWhNa/gw09Bx83IH8ig==XD0k8MVIP56oN7ue'}
        payload = {'type': 'noun'}
        response = requests.get(api_url, params=payload, headers=key)
        if response.ok:
            # return response.json()['word']
            return 't'
        else:
            return None

    @classmethod
    def get_word_from_offline_word_list(cls) -> str:
        # TODO: IndexError
        try:
            return random.choice(cls.offline_word_list)
        except IndexError:
            raise IndexError('ERROR78')

    def is_finished(self) -> str:
        no_remained_try = self.remained_try == 0
        word_fully_guessed = all([letter is not None for letter in self.guessed_letters.values()])
        if word_fully_guessed:
            return 'win'
        elif no_remained_try:
            return 'loose'
        if not no_remained_try:
            raise TypeError('continue')

    def reset_game(self):
        self.remained_try = 0
        self.word = ''
        self.guessed_letters = {}

    def is_game_setup(self):
        cond1 = all([letter is not None for letter in self.guessed_letters.values()])
        cond2 = self.remained_try == 0
        cond3 = self.word == ''
        return not (cond1 and cond2 and cond3)

    def setup_game(self):
        self.word = self.get_word_from_api().upper()  # TODO: must return string
        if self.word is None:
            self.word = self.get_word_from_offline_word_list().upper()

        self.guessed_letters = {str(i): None for i in range(1, len(self.word) + 1)}
        self.remained_try = len(self.word) * 3

    def get_guessed_letters_str(self):
        return ''.join(
            [f'{letter if letter is not None else place} ' for place, letter in self.guessed_letters.items()])

    def evaluate_guess(self, place, letter):
        self.remained_try -= 1
        if self.word[int(place) - 1] == letter:
            self.guessed_letters[place] = letter
        else:
            raise ValueError('Your guess was wrong, try again')

    def replay(self):
        replay = input('Do you want to play again?(y/n) ')
        if replay.strip().lower() == 'y':
            self.reset_game()
            self.play()

    def play(self):
        if not self.is_game_setup():  # ?? where should I check this condition? (inside the method or here)
            self.setup_game()
        logging.warning(self.word)  # TODO: dELETE
        print(f'\nremained try: {self.remained_try}')
        print(f"guessed_letters: {self.get_guessed_letters_str()}")
        try:
            place = self.get_place()
            letter = self.get_letter()
            self.evaluate_guess(place, letter)
            result = self.is_finished()
        except (ValueError, TypeError) as e:
            msg = str(e)
            if msg in ['continue', "You've already guessed this letter correctly", 'Invalid place',
                       'Letter should be an single alphabetic character.', 'Your guess was wrong, try again']:
                print(msg if msg != 'continue' else '')
                self.play()
        else:
            print(f"You {result}!")
            self.replay()

    def get_place(self) -> str:
        place = input('place: ').strip()
        value = self.guessed_letters.get(place, 'Invalid place')
        if value is None:
            return place
        elif value == 'Invalid place':
            raise ValueError(value)
        else:
            raise ValueError("You've already guessed this letter correctly")

    @staticmethod
    def get_letter():
        letter = input('letter: ').strip()
        if letter.isalpha() and len(letter) == 1:
            return letter.upper()
        raise ValueError('Letter should be an single alphabetic character.')


g = HangmanGame()
g.play()
