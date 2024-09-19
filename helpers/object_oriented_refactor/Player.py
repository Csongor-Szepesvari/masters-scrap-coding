from Game import Game
from Category import Category
class Player():
    def __init__(self, win_value:float, blind:bool, categories:list[Category]):
        self.strategy = {}
        for category in categories:
            self.strategy[category.get_name()] = 0 # a floating point representation of the percentage of students to admit from a particular category
        self.win_value = win_value
        self.blind = blind

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
    
    def find_feasible_limits(self, game:Game)->dict[str:float]:
        '''
        Projects a desired strategy out to the realisable game space based on other's strategies.
        Inputs:

            game->Game : the game object that contains the categories and other player's strategies so that we can find our feasible space.

        Outputs:
            max_category_values:dict[str:float] : a dictionary representing the maximum values for each category
        '''
        return_dict = {}
        for category in game.categories:
            return_dict[category.get_name()] = 

    def best_response(self, game:Game):
        '''
        This method calculates the best response in response to a game class and updates the strategy based on the best response type
        '''
        category_sizes = [category.get_size() for category in game.categories]
        max_admit = game.to_admit

        
        if game.game_mode_type == "expected":
            # use the expected case algorithm to evaluate what the expected best response would be in this setting
            
            # what are we trying to maximize in this setting?
            # c(game) = sum(attendees) - (num_attendees-desired_attendees)^2
            # first term wants you to maximize the number of students you admit, the second term caps it

            # in order to maximize this, we look at other players' allocation or occupancy in each category and calculate how many admissions to give out in order of best to worst
            

            # follow the simple logic of increasing admittances to Q1 > Q2 > Q3 > Q4 etc
            if self.blind:
                # if our player is blind then we just have Q1 + Q2 > Q3 + Q4
                
                # calculate our target distribution first and then scale it based on calc_collisions
                # our target is to have max_admit
                combined_high_size = sum(category_sizes[:2])
                combined_low_size = sum(category_sizes[2:])

                high_admissions = min(combined_high_size, max_admit)
                low_admissions = min(combined_low_size, max_admit-high_admissions)

                desired_strategy = [high_admissions/combined_high_size, low_admissions/combined_low_size]
                self.project_strategy(self, desired_strategy, game)

        elif game.game_mode_type == "top_k":
            # use the top k algorithm to evaluate what the expected best response would be
            # c(game) = sum(top_k) - (num_attendees-desired_attendees)^2
            # first term wants you to maximize the number of students you admit, the second term caps it

            # in order to maximize this we keep building up students by student until the marginal value gained from having additional students is less than the chance of finding someone better
            # this is a greedy method

            # the perfect method is to literally find


                

    


def test_calculate_win_chance():
    players = set([Player(60), Player(20), Player(40), Player(50)])
    print([(player.get_win_value(), player.calculate_win_chance(players.difference([player]))) for player in players])

#test_calculate_win_chance()