'''
This module is dedicated to defining the Game object/class which contains all information needed to solve and simulate a particular game.

The information coming in is:
A list of the players of the game.
A list of different categories - what players draw their action sets from.
The game-mode, also known as the utility function, that players will optimize for in consideration of other players.
'''
from Category import Category, CombinedCategory

import numpy as np

class Player():
    def __init__(self, win_value:float, blind:bool):
        self.strategy = {"Q1":0, "Q2":0, "Q3":0, "Q4":0}
        self.blind_strategy = {"high":0, "low":0}
        self.win_value = win_value
        self.blind = blind

    def update_blind_strategy(self, strategy, game):
        categories = game.categories
        for category in categories.keys():
            strategy[category]

    def calculate_win_chance(self, players):
        win_percent = self.win_value / (sum([player.get_win_value() for player in players]))
        return win_percent
    
    def calc_expected_attendees(self, strategy, game):
        '''
        This method calculates the expected attendees from a particular strategy in context of all other player's strategies
        '''
        categories = game.categories
        other_players = [player for player in game.players if player != self]
        print(other_players)
        achieved_result_pct = {}
        for category in categories:
            # the meat
            achieved_result_pct[category.get_name()] = strategy[category.get_name()] * (1 - self.calculate_percentage_lost_to_others(other_players, category))
        return achieved_result_pct

    
    def calculate_percentage_lost_to_others(self, other_players, category):
        '''
        This method returns the percentage of a category lost to others regardless of our own strategic occupation.
        '''
        def helper(occupancy_list, index):

            _occ = occupancy_list
            print(_occ)
            # start adding up the probabilities of the event
            prob_event = 1
            # include things in the denominator
            denom = self.win_value

            # check if we're at the bottom
            if index == len(_occ)-1:
                # calculate the value of this event
                for i in range(len(_occ)):
                    occupies = _occ[i]
                    if occupies:
                        prob_event *= other_players[i].strategy[category]
                        denom += other_players[i].win_value
                    else:
                        prob_event *= (1-other_players[i].strategy[category])
                # actual value calculation for a loss
                return prob_event * (1 - self.win_value/denom)

            else:
                _index = index + 1
                false_val = helper(occupancy_list=_occ, index=_index)
                _occ[_index] = True
                true_val = helper(occupancy_list=_occ, index=_index)
                return false_val + true_val

        f_start = [False for i in range(len(other_players))]
        print(f_start)
        f_val = helper(f_start, 0)
        print(f_val)
        f_start[0] = True
        t_val = helper(f_start, 0)

        return f_val + t_val

    def project_desired_to_real(self, strategy, game)->dict[str:float]:
        '''
        Projects a desired strategy out to the realisable game space based on other's strategies.
        Inputs:

            game->Game : the game object that contains the categories and other player's strategies so that we can find our feasible space.

        Outputs:
            max_category_values:dict[str:float] : a dictionary representing the strategy to play in order to get our desired strategy
        '''
        assert type(game) == Game
        other_players = [player for player in game.players if player != self]
        for category in game.categories:
            self.strategy[category.get_name()] = strategy[category.get_name()]/(1-self.calculate_percentage_lost_to_others(other_players=other_players, category=category))
        

    


    def numbers_to_pct(self, strategy, game):
        '''
        Converts a strategy dictionary with numbers into percentages
        '''
        strat = {}
        for category in game.categories:
            strat[category.get_name()] = strategy[category.get_name()]/category.get_size()

        return strat

    def pct_to_numbers(self, strategy, game):
        '''
        Converts a strategy dictionary with percentages into numbers
        '''
        strat = {}
        for category in game.categories:
            strat[category.get_name()] = strategy[category.get_name()]*category.get_size()

        return strat

    def best_response(self, game):
        assert type(game) == Game
        '''
        This method calculates the best response in response to a game class and updates the strategy based on the best response type
        '''
        category_sizes = [category.get_size() for category in game.categories]
        categories = [category.get_name() for category in game.categories]
        max_admit = game.to_admit
        admits = 0

        # calculate the maximum number of students we can get
        max_strat = {}
        for category in game.categories:
            max_strat[category.get_name()] = 1
        feasible_strat = self.calc_expected_attendees(strategy=max_strat, game=game)

        
        feasible_strategy_numbers = {}
        for category in game.categories:
            feasible_strategy_numbers[category.get_name()] = feasible_strat[category.get_name()]*category.get_size()
        
            
        if game.game_mode_type == "expected":
            # use the expected case algorithm to evaluate what the expected best response would be in this setting
            
            # what are we trying to maximize in this setting?
            # c(game) = sum(attendees) - (num_attendees-desired_attendees)^2
            # first term wants you to maximize the number of students you admit, the second term caps it

            # in order to maximize this, we look at other players' allocation or occupancy in each category 
            # and calculate how many admissions to give out in order of best to worst


            if not self.blind:
                new_strat_numbers = {}
                # follow the simple logic of increasing admittances to Q1 > Q2 > Q3 > Q4 etc
                for cat_name in ["Q1", "Q2", "Q3", "Q4"]:
                    if feasible_strategy_numbers[cat_name] <= max_admit:
                        # maxing out Q1
                        max_admit -= feasible_strategy_numbers[cat_name]
                        new_strat_numbers[cat_name] = feasible_strategy_numbers[cat_name]
                    else:
                        new_strat_numbers[cat_name] = max_admit
                        break
                
                # convert new strat numbers to percentages and then project
                expected_outcome = self.numbers_to_pct(strategy=new_strat_numbers, game=game)
                self.strategy = self.project_desired_to_real(expected_outcome, game=game)
                

                

            elif self.blind:
                # if our player is blind then we just have Q1 + Q2 > Q3 + Q4
                
                # so we add together category Q1 and Q2 as well as Q3 and Q4
                high_numbers = feasible_strategy_numbers["Q1"] + feasible_strategy_numbers["Q2"]
                low_numbers = feasible_strategy_numbers["Q3"] + feasible_strategy_numbers["Q4"]
                new_strat = {}
                if high_numbers <= max_admit:
                    new_strat["Q1"] = 1
                    new_strat["Q2"] = 1
                else:
                    # if it's not combined
                    feasible_strat[]
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
            pass




class Game():
    '''
    Game class meant for creating specific instances of games, both to find equilibrium points and also to simulate those games
    '''
    def __init__(self, num_players:int, to_admit: int, players:list[Player], categories:dict[str:Category], game_mode_type:str):
        '''
        Initializes a game object based on:

            num_players->int : the number of players in a game
            to_admit->int : the number of students each player is admitting
            win_vals->list[float] : the associated "win value" with each player
            categories->list[Category] : a list of the categories of the students
            game_mode_type->str : the type of the game, either "top_k" or "expected"
        '''

        self.num_players = num_players
        self.players = players
        self.to_admit = to_admit
        self.categories = categories
        self.blind_categories = self.generate_blind_cat()
        self.game_mode_type = game_mode_type

    def generate_blind_cat(self):
        categories = ["Q1","Q2","Q3","Q4"]
        high = CombinedCategory(
            name="high", mean1=categories["Q1"].get_mean(), mean2=categories["Q2"].get_mean(), 
            std1=categories["Q1"].get_std(), std2=categories["Q2"].get_std(), 
            size1=categories["Q1"].get_size(), size2=categories["Q2"].get_size()
        )
        low = CombinedCategory(
            name="low", mean1=categories["Q3"].get_mean(), mean2=categories["Q4"].get_mean(), 
            std1=categories["Q3"].get_std(), std2=categories["Q4"].get_std(),
            size1=categories["Q3"].get_size(), size2=categories["Q4"].get_size()
        )
        return {"high":high, "low":low}

    def simulate_game(self):
        '''
        This method simulates a game as it would actually play out based on the players' strategies.

        It steps through each category, generates random sets of admittees for each player based on their strategies, resolves collisions and gets actual attendants
        '''
        for category in self.categories:
            realized_strategies = []
            for player in self.players:
                # grab the strategy for the player in this category
                percentage_reprentation = player.get_strategy(category.get_name())
                # generate the realized strategy for each player
                realized_strategies.append(np.random.choice(size=category.get_size(), replace=False))
            print(realized_strategies)
            

    def find_strategies_iterated_br(self):
        '''
        This method finds the stable strategies for each player based on iterated best response. If a stable profile is found it is a Nash Equilibrium

        The method works by iterating through the list of players and asking each off them to best respond to the game object as it stands.
        If after one iteration of going through all players, no players' strategies change, we have found a stable point and exit. The loop.

        Has no inputs. But the resultant strategies are updated in the strategy dictionaries of the players contained in the list.
        '''
        last_strats = None
        
        # while last strats aren't the same as the current updated list, loop (detects if there's no change from looping)

        # NOTE: straight equality (==) CAN be used here, because python does an element-wise equality check of lists, which then does an equality check on the nested dictionaries, very cool!
        while last_strats != self.get_strat_list():
            # update last strats to the current strats before updating our strategies in the inner loop
            last_strats = self.get_strat_list()
            for player in self.players:
                player.best_response(self)

        print("Woohoo! Converged!")

    def get_strat_list(self):
        '''
        This method loops through the player list and gets a list of their respective strategies
        '''
        return [player.get_strat() for player in self.players]

