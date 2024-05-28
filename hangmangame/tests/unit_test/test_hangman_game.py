import unittest

from ...hangman_game import HangmanGame


class TestHangmanGame(unittest.TestCase):

    def setUp(self):
        self.game = HangmanGame()

    def test_game_instantiation(self):
        self.assertEqual(self.game.word, '')
        self.assertEqual(self.game.guessed_letters, dict())
        self.assertEqual(self.game.remained_try, 0)

    def test_get_word_from_api_real(self):
        pass

    def test_get_word_from_api_mocked(self):
        pass

    # def


if __name__ == '__main__':
    unittest.main()
