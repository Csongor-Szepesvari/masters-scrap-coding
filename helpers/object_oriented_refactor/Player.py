from Game import Game
from Category import Category
class Player():
    def __init__(self, win_value):
        self.strategy = {}
        self.win_value = win_value

    def calculate_win_chance(self, other_players):
        win_percent = self.win_value / (self.win_value + sum([player.get_win_value() for player in other_players]))
        return win_percent
    
    def set_strategy(self, game:Game, strat_numbers_list:list):
        assert len(strat_numbers_list) == len(game.categories)
        assert max(strat_numbers_list) <= 1
        assert min(strat_numbers_list) >= 0

        for i in range(len(strat_numbers_list)):
            category = game.categories[i]
            strategy = strat_numbers_list[i]
            name = category.get_name()
            self.strategy[name] = strategy

    def get_win_value(self):
        return self.win_value
    


def test_calculate_win_chance():
    players = set([Player(60), Player(20), Player(40), Player(50)])
    print([(player.get_win_value(), player.calculate_win_chance(players.difference([player]))) for player in players])

#test_calculate_win_chance()