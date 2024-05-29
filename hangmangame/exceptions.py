class GameNotFinishedError(Exception):
    pass


class WrongGuessError(Exception):
    pass


class InvalidInputError(ValueError):
    pass

class CanNotSetWord(Exception):
    pass
