'''
This module is dedicated to defining the Game object/class which contains all information needed to solve and simulate a particular game.

The information coming in is:
A list of the players of the game.
A list of different categories - what players draw their action sets from.
The game-mode, also known as the utility function, that players will optimize for in consideration of other players.
'''
from Category import Category, CombinedCategory

import numpy as np
import pandas as pd

df = pd.read_csv('modified_mean_dict.csv', na_values=['', 'NA', 'N/A'], keep_default_na=True, na_filter=True)

def df_lookup(num_samples:int, top_k:int)->float:
    '''
    Uses global dataframe containing z-scores to do a lookup of what the expected z score is with a given number of samples at the k-th position
    /params/
        num_samples : int; The number of students to admit
        top_k : int; The k-th largest to get
    /returns/
        z-score : float; The sampled z-score of that lookup
    '''
    assert(top_k<=num_samples)
    translated = str(top_k)+"th largest"
    return float(df[df["num_samples"] == num_samples][translated].iloc[0])

class Player():
    def __init__(self, win_value:float, blind:bool, level:int, name:str):
        '''
        Initializer for a Player object, takes in the following parameters:
        win_value: the value used to calculate the probability of victory for player collisions
        blind: a boolean value that determines if the player is blind or not
        level: an integer value that determines the level of the player, with 0 not optimizing past the single-player level and 1+ optimizing for multiple iterations
        '''
        self.strategy = {"Q1":0, "Q2":0, "Q3":0, "Q4":0}
        self.blind_strategy = {"high":0, "low":0}
        self.win_value = win_value
        self.blind = blind
        self.level = level
        self.name = name

    def update_blind_strategy(self, strategy, game):
        '''
        To update the blind strategy with these categories we have to multiply the probabilities with the category sizes to get the total occupancy and convert it into low and high
        '''
        self.blind_strategy["high"] = strategy["Q1"] * game.categories["Q1"].get_size() + strategy["Q2"] * game.categories["Q2"].get_size() / (game.categories["Q1"].get_size() + game.categories["Q2"].get_size())
        self.blind_strategy["low"] = strategy["Q3"] * game.categories["Q3"].get_size() + strategy["Q4"] * game.categories["Q4"].get_size() / (game.categories["Q3"].get_size() + game.categories["Q4"].get_size())


    def update_strategy(self, blind_strategy):
        '''This method updates the player strategy based on the blind strategy given'''
        self.strategy["Q1"] = blind_strategy["high"]
        self.strategy["Q2"] = blind_strategy["high"]
        self.strategy["Q3"] = blind_strategy["low"]
        self.strategy["Q4"] = blind_strategy["low"]
        

    def calculate_win_chance(self, players):
        win_percent = self.win_value / (sum([player.get_win_value() for player in players]))
        return win_percent
    
    def calc_expected_attendees(self, strategy, game):
        '''
        This method calculates the expected attendees from a particular strategy in context of all other player's strategies
        '''
        other_players = [player for player in game.players if player != self]
        print(other_players)
        achieved_result_pct = {}
        for category in game.categories.values():
            # the meat
            achieved_result_pct[category.get_name()] = strategy[category.get_name()] * (1 - self.calculate_percentage_lost_to_others(other_players, category))
        return achieved_result_pct

    
    def calculate_percentage_lost_to_others(self, other_players, category):
        '''
        This method returns the percentage of a category lost to others regardless of our own strategic occupation.
        Parameters:
        1. other_players: a list of all other players in the game
        2. category: the category we're looking at
        '''
        def helper(occupancy_list, index):

            _occ = occupancy_list
            #print(_occ)
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

    def eval_optimal_top_k(self,strategy_numbers:dict[str:int],categories:dict[str:Category], k:int)->float:
        '''
        This method finds the optimal distribution of top k over a strategy and returns the expected value of that distribution
        Inputs:
        strategy_numbers: a dictionary describing the number of attending students
        categories: a dictionary of the categories themselves
        k: the top k number
        Returns:
        total_value: the expected value of the top k students under this strategy
        '''
        k_vals = {category.get_name():0 for category in categories.values()}
        total_value = 0
        max_category = ""
        for i in range(k):
            max_val = float('-inf')
            for category in categories.values():
                _k_val = df_lookup(num_samples=strategy_numbers[category.get_name()], num_success=min(k_vals[category.get_name()]+1, strategy_numbers[category.get_name()]))
                if _k_val > max_val:
                    max_val = _k_val
                    max_category = category.get_name()
            
            total_value += max_val
            k_vals[max_category] += 1

        return total_value

    def greedy_top_k_br(self, game, feasible_strategy_numbers:dict[str:float], k:int, blind=False):
        to_admit = game.to_admit
        new_strategy = {category.get_name():0 for category in game.categories.values()}
        if not blind:
            for i in range(to_admit):
                max_val = float('-inf')
                max_cat = ""
                for category in game.categories.values():
                    if 1 + new_strategy[category.get_name()] <= feasible_strategy_numbers[category.get_name()]:
                        name = category.get_name()
                        temp_strat = new_strategy.copy()
                        temp_strat[name] += 1
                        _val_strat = self.eval_optimal_top_k(strategy_numbers=temp_strat, categories=game.categories, k=k)
                        if _val_strat > max_val:
                            max_val = _val_strat
                            max_cat = name
    
                new_strategy[max_cat] += 1

            self.strategy = {category.get_name():new_strategy[category.get_name()]/feasible_strategy_numbers[category.get_name()] for category in game.categories.values()}
            self.update_blind_strategy(strategy=self.strategy, game=game)    

        else:
            # the blind agent just takes the high mean players
            high_nums = feasible_strategy_numbers["Q1"] + feasible_strategy_numbers["Q2"]
            low_nums = feasible_strategy_numbers["Q3"] + feasible_strategy_numbers["Q4"]

            high_admit = min(to_admit, high_nums)
            remainder = to_admit-high_admit

            blind_strategy = {"high":high_admit/high_nums, "low":remainder/low_nums}
            self.update_strategy(blind_strategy=blind_strategy)
        
           



    def best_response(self, game):
        assert type(game) == Game
        '''
        This method calculates the best response in response to a game class and updates the strategy based on the best response type
        '''
        category_sizes = [category.get_size() for category in game.categories.values()]
        max_admit = game.to_admit
        admits = 0

        # calculate the maximum number of students we can get
        max_strat = {}
        for category in game.categories.values():
            max_strat[category.get_name()] = 1
        feasible_strat = self.calc_expected_attendees(strategy=max_strat, game=game)

        
        feasible_strategy_numbers = {}
        for category in game.categories.values():
            feasible_strategy_numbers[category.get_name()] = feasible_strat[category.get_name()]*category.get_size()
        
            
        if game.game_mode_type == "expected":
            # use the expected case algorithm to evaluate what the expected best response would be in this setting
            
            # what are we trying to maximize in this setting?
            # c(game) = sum(attendees) - (num_attendees-desired_attendees)^2
            # first term wants you to maximize the number of students you admit, the second term caps it

            # in order to maximize this, we look at other players' allocation or occupancy in each category 
            # and calculate how many admissions to give out in order of best to worst


            if not self.blind:
                new_strat = {}
                # follow the simple logic of increasing admittances to Q1 > Q2 > Q3 > Q4 etc
                for cat_name in ["Q1", "Q2", "Q3", "Q4"]:
                    if feasible_strategy_numbers[cat_name] <= max_admit:
                        # maxing out the category, so we just admit everyone
                        max_admit -= feasible_strategy_numbers[cat_name]
                        new_strat[cat_name] = 1
                    else:
                        # we can't max out the category, so we admit as many as desired and then stop
                        new_strat[cat_name] = max_admit/feasible_strategy_numbers[cat_name]
                        break
                
                # convert new strat numbers to percentages and then project
                
                self.strategy = new_strat
                self.update_blind_strategy(strategy=self.strategy, game=game)
                

            elif self.blind:
                # if our player is blind then we just have Q1 + Q2 > Q3 + Q4
                
                # so we add together category Q1 and Q2 as well as Q3 and Q4
                high_numbers = feasible_strategy_numbers["Q1"] + feasible_strategy_numbers["Q2"]
                low_numbers = feasible_strategy_numbers["Q3"] + feasible_strategy_numbers["Q4"]
                new_strat = {}
                
                # we want to admit in high, h
                high_admit = min(high_numbers, max_admit)
                low_admit = min(low_numbers, max_admit-high_admit)

                real_strat_high = high_admit/high_numbers
                real_strat_low = low_admit/low_numbers

                self.blind_strategy['high'] = real_strat_high
                self.blind_strategy['low'] = real_strat_low
                self.update_strategy(strategy=self.blind_strategy)


        elif game.game_mode_type == "top_k":
            # use the top k algorithm to evaluate what the expected best response would be
            # c(game) = sum(top_k) - (num_attendees-desired_attendees)^2
            # first term wants you to maximize the number of students you admit, the second term caps it

            # in order to maximize this we keep building up students by student until the marginal value gained from having additional students is less than the chance of finding someone better
            # this is a greedy method

            # the perfect method is to literally find
            '''
            greedy top_k best response process
            '''
            if not self.blind:
                self.greedy_top_k_br(game=game, k=game.top_k, blind=False)
            else:
                self.greedy_top_k_br(game=game, k=game.top_k, blind=True)


class Candidate():
    '''
    Candidate objects, has a value generated from a category.
    '''

    def __init__(self, category:Category):
        self.value = category.get_samples(1)
        self.competitors = []


    def add_competitor(self, player:Player):
        self.competitors.append(player)

    def simulate_winner(self)->Player:
        # randomly sample between 0-1

        # normalize their values and turn them into cumulative values
        comp_values = np.array([player.win_value for player in self.competitors])
        normalized_values = comp_values/np.sum(comp_values)
        # set cumulative limits
        cumulative_probs = np.cumsum(normalized_values)
        # get random value
        random_value = np.random.rand()
        # find winner
        for i in range(len(cumulative_probs)):
            if random_value < cumulative_probs[i]:
                return self.competitors[i]


class Game():
    '''
    Game class meant for creating specific instances of games, both to find equilibrium points and also to simulate those games
    '''
    def __init__(self, num_players:int, to_admit: int, players:list[Player], categories:dict[str:Category], game_mode_type:str, top_k=None):
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
        self.player_dict = {player.name:player for player in self.players}
        self.to_admit = to_admit
        self.categories = categories
        self.category_keys = ["Q1", "Q2", "Q3", "Q4"]
        self.blind_categories = self.generate_blind_cat()
        self.game_mode_type = game_mode_type
        self.top_k = top_k

    def generate_blind_cat(self):
        high = CombinedCategory(
            name="high", mean1=self.categories["Q1"].get_mean(), mean2=self.categories["Q2"].get_mean(), 
            std1=self.categories["Q1"].get_std(), std2=self.categories["Q2"].get_std(), 
            size1=self.categories["Q1"].get_size(), size2=self.categories["Q2"].get_size()
        )
        low = CombinedCategory(
            name="low", mean1=self.categories["Q3"].get_mean(), mean2=self.categories["Q4"].get_mean(), 
            std1=self.categories["Q3"].get_std(), std2=self.categories["Q4"].get_std(),
            size1=self.categories["Q3"].get_size(), size2=self.categories["Q4"].get_size()
        )
        return {"high":high, "low":low}

    def get_game_utility(self, attendees:dict[str:float], game_type:str, top_k=None)->dict[str:float]:
        '''evaluates a game based on our two utility functions and returns the utility of each player in a dictionary
        structure of dictionary is player.name : utility
        '''
        results = {}
        if game_type=="top_k":
            # the utility function in this case will add up the top k values and subtract the difference with desired
            for player in self.players:
                utility = sum(sorted(attendees[player.name], reverse=True)[:top_k]) - (len(attendees[player.name])-self.to_admit)**2
                results[player.name] = utility
        else:
            # straight sum minus the difference
            for player in self.players:
                utility = attendees[player.name] - (len(attendees[player.name])-self.to_admit)**2
                results[player.name] = utility

        return results


    def simulate_game(self, garbage):
        '''
        This method simulates a game as it would actually play out based on the players' strategies.

        It steps through each category, generates random sets of admittees for each player based on their strategies, resolves collisions and gets actual attendants
        '''
        _garbage = garbage

        attendees = {player.name:[] for player in self.players}
        for category in self.categories:
            # for each category generate a list of admittees
            candidates = [Candidate(category) * category.get_size()]
            
            admittees = []
            

            for player in self.players:
                # we want to highlight a selection of candidates, for each player we want to give 0 or 1 for each candidate
                player_selection = set(np.random.Generator.choice(a=category.get_size(), size=player.strategy[category.get_name()]*category.get_size(), replace=False))
                temp = []
                for i in range(self.category.get_size()):
                    if i in player_selection:
                        temp.append(1)
                    else:
                        temp.append(0)
                admittees.append(temp)
                

            '''
            Loop through candidates, then for each player in admittees check who is in on sweepstakes
            Then simulate the chance breakdown and add the candidate value to the winning players attendees
            '''
            for i in range(len(candidates)):
                candidate = candidates[i]
                for j in range(len(self.players)):
                    can_player = admittees[j][i]
                    if can_player == 1:
                        candidate.add_competitor(self.players[j])
                winning_player = candidate.simulate_winner()
                attendees[winning_player.name].append(candidate.value)

        '''Calculate the utilities for the game and return it'''
        return self.get_game_utility(attendees=attendees, game_type=self.game_mode_type, top_k=self.top_k)

            

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
        looped = 0
        while last_strats != self.get_strat_list():
            # update last strats to the current strats before updating our strategies in the inner loop
            last_strats = self.get_strat_list()
            for player in self.players:
                if player.level >= looped:
                    player.best_response(self)
            looped += 1

        print("Woohoo! Converged!")

    def get_strat_list(self):
        '''
        This method loops through the player list and gets a list of their respective strategies
        '''
        return [player.strategy for player in self.players]

