import unittest
from unittest.mock import patch, Mock

import requests

from hangmangame import constants as c
from hangmangame import exceptions as ex
from hangmangame.hangman_game import HangmanGame


class TestHangmanGame(unittest.TestCase):

    def setUp(self):
        self.game = HangmanGame()

    def test_game_instantiation(self):
        self.assertEqual(self.game.word, '')
        self.assertEqual(self.game.guessed_letters, dict())
        self.assertEqual(self.game.remained_try, 0)

    def test_get_word_from_api_success(self):
        with patch('hangmangame.hangman_game.requests.get') as mocked_get:
            # create mocked response
            mocked_response = Mock()
            mocked_response.raise_for_status.return_value = None
            mocked_response.json.return_value = {'word': 'success'}

            # pass the mocked response as return value to the mocked_get function
            mocked_get.return_value = mocked_response

            word = self.game.get_word_from_api()

            # assertions
            self.assertEqual(word, 'success')
            mocked_get.assert_called_once_with(c.API_URL, params=c.PAYLOAD, headers=c.API_KEY, timeout=1.5)

    def test_get_word_from_api_http_error(self):
        # https://requests.readthedocs.io/en/latest/_modules/requests/models/#Response.raise_for_status
        # raise_for_status raises requests.exceptions.HttpError or returns None
        # HttpError is for 400, 500, encoding
        with patch('hangmangame.hangman_game.requests.get') as mocked_get:
            mocked_response = Mock()
            mocked_response.raise_for_status.side_effect = requests.exceptions.HTTPError('HTTP Error')
            mocked_get.return_value = mocked_response

            word = self.game.get_word_from_api()

            self.assertIsNone(word)
            mocked_get.assert_called_once_with(c.API_URL, params=c.PAYLOAD, headers=c.API_KEY, timeout=1.5)

    def test_get_word_from_api_request_exception(self):
        # https://requests.readthedocs.io/en/latest/api/#exceptions
        # request.get requests.exceptions.ConnectTimeout
        # request.get requests.exceptions.RequestException
        with patch('hangmangame.hangman_game.requests.get') as mocked_get:
            mocked_response = Mock()
            mocked_response.raise_for_status.side_effect = requests.exceptions.RequestException('RequestException')
            mocked_get.return_value = mocked_response

            word = self.game.get_word_from_api()

            self.assertIsNone(word)
            mocked_get.assert_called_once_with(c.API_URL, params=c.PAYLOAD, headers=c.API_KEY, timeout=1.5)

    def test_get_word_from_offline_word_list_non_empty_list(self):
        with patch('hangmangame.hangman_game.c.OFFLINE_WORD_LIST', new_callable=list) as mocked_list:
            mocked_list.extend(['example1, example2'])
            word = self.game.get_word_from_offline_word_list()
            # print(mocked_list,'3333333333333333333333333333')
            self.assertIn(word, mocked_list)

    def test_get_word_from_offline_word_list_empty_list(self):
        with patch('hangmangame.hangman_game.c.OFFLINE_WORD_LIST', new_callable=list) as mocked_list:
            # mocked_list is empty
            word = self.game.get_word_from_offline_word_list()
            self.assertIsNone(word)

    def test_set_word(self):
        pass

    def test_setup_game(self):
        pass

    def test_is_finished_win(self):
        # if remained try is 0
        self.game.guessed_letters = {'1': 'B', '2': 'A'}
        result = self.game.is_finished()
        self.assertEqual(result, 'win')

        # if remained try is not 0
        self.game.remained_try = 10
        result = self.game.is_finished()
        self.assertEqual(result, 'win')

    def test_is_finished_lose(self):
        self.game.guessed_letters = {'1': None, '2': 'A'}
        # self.game.remained_try is 0 by default
        result = self.game.is_finished()
        self.assertEqual(result, 'lose')

    def test_is_finished_game_not_finished_error(self):
        self.game.guessed_letters = {'1': None, '2': 'A'}
        self.game.remained_try = 10
        with self.assertRaises(ex.GameNotFinishedError):
            self.game.is_finished()

    def test_reset_game(self):
        self.game.word = 'FOO'
        self.game.guessed_letters = {'1': 'F', '2': 'O', '3': 'O'}
        self.game.remained_try = 9

        self.game.reset_game()
        self.assertEqual(self.game.word, '')
        self.assertEqual(self.game.guessed_letters, {})
        self.assertEqual(self.game.remained_try, 0)

    def test_get_guessed_letters_str(self):
        self.game.guessed_letters = {'1': 'F', '2': None, '3': 'O'}
        guessed_letters_str = self.game.get_guessed_letters_str()
        self.assertEqual(guessed_letters_str, 'F 2 O')

        self.game.guessed_letters = {'1': None, '2': None, '3': None}
        guessed_letters_str = self.game.get_guessed_letters_str()
        self.assertEqual(guessed_letters_str, '1 2 3')

    def test_evaluate_guess_correct_guess(self):
        self.game.word = 'FOO'
        self.game.guessed_letters = {'1': None, '2': None, '3': None}
        self.game.evaluate_guess(place='1', letter='F')

        guessed_letters_str = self.game.get_guessed_letters_str()
        self.assertEqual(guessed_letters_str, 'F 2 3')

    def test_evaluate_guess_incorrect_guess(self):
        self.game.word = 'FOO'
        self.game.guessed_letters = {'1': None, '2': None, '3': None}
        kwargs = {'place': '1', 'letter': 'T'}

        self.assertRaises(ex.WrongGuessError, self.game.evaluate_guess, **kwargs)

    def test_replay(self):
        pass

    def test_play(self):
        pass

    def test_is_valid_place_valid_place(self):
        self.game.word = 'FOO'
        self.game.guessed_letters = {'1': None, '2': None, '3': None}
        for place in self.game.guessed_letters:
            return_place = self.game.is_valid_place(place)
            self.assertEqual(return_place, place)

    def test_is_valid_place_invalid_place(self):
        self.game.word = 'FOO'
        self.game.guessed_letters = {'1': None, '2': 'O', '3': None}

        already_guessed_place = '2'
        self.assertRaises(ex.InvalidInputError, self.game.is_valid_place, already_guessed_place)

        invalid_key = '0'
        self.assertRaises(ex.InvalidInputError, self.game.is_valid_place, invalid_key)

    def test_is_valid_letter_valid_letter(self):
        valid_letters = ['a', 'A']
        for letter in valid_letters:
            return_letter = self.game.is_valid_letter(letter)
            self.assertEqual(return_letter, 'A')

    def test_is_valid_letter_invalid_letter(self):
        invalid_letters = ['-', '2', '&', '_', 'ta', 'TA']
        for letter in invalid_letters:
            with self.assertRaises(ex.InvalidInputError):
                self.game.is_valid_letter(letter)

    def tearDown(self):
        del self.game


if __name__ == '__main__':
    unittest.main()
