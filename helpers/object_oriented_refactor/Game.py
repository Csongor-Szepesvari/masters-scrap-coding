'''
This module is dedicated to defining the Game object/class which contains all information needed to solve and simulate a particular game.

The information coming in is:
A list of the players of the game.
A list of different categories - what players draw their action sets from.
The game-mode, also known as the utility function, that players will optimize for in consideration of other players.
'''
from Category import Category
from Player import Player
import numpy as np

class Game():
    '''
    Game class meant for creating specific instances of games, both to find equilibrium points and also to simulate those games
    '''
    def __init__(self, num_players:int, to_admit: int, players:list[Player], categories:list[Category], game_mode_type:str):
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
        self.game_mode_type = game_mode_type

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
            
        
    def calc_collisions(self, category:str, player_list: list[Player]):
        '''
        This function calculates the number of collisions in a category
        '''

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
    
    def calc_expected_attendees(self, strategy, game):
        '''
        This method calculates the expected attendees from a particular strategy in context of all other player's strategies
        '''
        categories = game.categories
        other_players = [player for player in game.players if player != self]
        print(other_players)
        for category in categories:
            pass


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
            return_dict[category.get_name()] = 1

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
            pass


                

    


def test_calculate_win_chance():
    players = set([Player(60), Player(20), Player(40), Player(50)])
    print([(player.get_win_value(), player.calculate_win_chance(players.difference([player]))) for player in players])

categories = [Category("Q1", 0, 1, 20), Category("Q2", 1, 1, 25)]
player = Player(60, True, categories)
player2 = Player(40, True, categories)
player3 = Player(50, True, categories)
game = Game(3, 8, [player, player2, player3], categories, game_mode_type="expected")

player.calc_expected_attendees({"Q1":1, "Q2":1}, game=game)




game = Game(players=[Player(60), Player(40)], categories=[Category(size=12, std=1, mean=2, name="Q1"), Category(size=24, std=2, mean=1, name="Q2")])
for player in game.players:
    player.set_strategy(game, [0.5, 0.6])

game.simulate_game()
