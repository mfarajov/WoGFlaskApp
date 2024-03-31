import random
from Games import Game


class MemoryGame(Game):

    def __init__(self, difficulty):
        super().__init__(difficulty)

    def generate_sequence(self):
        # Generate a sequence of random numbers based on the game's difficulty level
        return [random.randint(1, 101) for _ in range(self.difficulty)]

    @staticmethod
    def is_list_equal(list1, list2):
        # Check if two lists are equal
        return list1 == list2

    def play(self, sequence, user_sequence):
        # Determine if the game is won based on the sequence comparison
        return self.is_list_equal(sequence, user_sequence)

    def end_game(self, won):
        if won:
            return f'Congratulations! You won the Memory Game!'
        else:
            return f'Sorry! Unfortunately, you lost the Memory Game.'
