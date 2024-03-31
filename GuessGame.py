import random
from Games import Game


class GuessGame(Game):

    def __init__(self, difficulty):
        super().__init__(difficulty)
        self.secret_number = random.randint(1, self.difficulty)

    def play(self, guess):
        if guess == self.secret_number:
            return True, self.secret_number
        else:
            return False, self.secret_number

    def end_game(self, won):
        if won:
            return f'Congratulations! You won the Guess Game!'
        else:
            return f'Sorry! Unfortunately, you lost the Guess Game.'
