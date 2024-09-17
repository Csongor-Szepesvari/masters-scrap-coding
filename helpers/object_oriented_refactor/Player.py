from Game import Game
from Category import Category
class Player():
    def __init__(self, win_value:float, categories:list[Category]):
        self.strategy = {}
        for category in categories:
            self.strategy[category.get_name()] = 0 # a floating point representation of the percentage of students to admit from a particular category
        self.win_value = win_value

    def calculate_win_chance(self, players):
        win_percent = self.win_value / (sum([player.get_win_value() for player in players]))
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
    
    def best_response(game:Game):
        '''
        This method calculates the best response in response to a game class and updates the strategy based on the best response type
        '''
        if game.game_mode_type == "top_k":
            # use the top k algorithm to evaluate what the expected best response would be
            # c(game) = sum(top_k) - (num_attendees-desired_attendees)^2
            # first term wants you to maximize the number of students you admit, the second term caps it

            # in order to maximize this we keep building up students by student until the marginal value gained from having additional students is less than the chance of finding someone better
            # this is a greedy method

            # the perfect method 
        elif game.game_mode_type == "expected":
            # use the expected case algorithm to evaluate what the expected best response would be in this setting
            
            # what are we trying to maximize in this setting?
            # c(game) = sum(attendees) - (num_attendees-desired_attendees)^2
            # first term wants you to maximize the number of students you admit, the second term caps it

            # in order to maximize this, we look at other players' allocation or occupancy in each category and calculate how many admissions to give out in order of best to worst

    


def test_calculate_win_chance():
    players = set([Player(60), Player(20), Player(40), Player(50)])
    print([(player.get_win_value(), player.calculate_win_chance(players.difference([player]))) for player in players])

#test_calculate_win_chance()