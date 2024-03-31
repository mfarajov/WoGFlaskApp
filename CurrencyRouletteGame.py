from Games import Game


class CurrencyRouletteGame(Game):
    def __init__(self, difficulty):
        super().__init__(difficulty)
        self.current_rate = 3.5

    def get_money_interval(self, amount_in_usd):
        total_value = amount_in_usd * self.current_rate
        return total_value - (5 - self.difficulty), total_value + (5 - self.difficulty)

    def play(self, user_guess, amount_in_usd):
        interval = self.get_money_interval(amount_in_usd)
        return interval[0] <= user_guess <= interval[1], interval

    def end_game(self, won):
        if won:
            return f'Congratulations! You won the Currency Roulette Game!'
        else:
            return f'Sorry! Unfortunately, you lost the Currency Roulette Game.'
