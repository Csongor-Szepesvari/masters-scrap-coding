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
    def __init__(self, num_players:int, to_admit: int, win_vals:list[float], categories:list[Category], game_mode_type:str):
        '''
        Initializes a game object based on:

            num_players->int : the number of players in a game
            to_admit->int : the number of students each player is admitting
            win_vals->list[float] : the associated "win value" with each player
            categories->list[Category] : a list of the categories of the students
            game_mode_type->str : the type of the game, either "top_k" or "expected"
        '''

        self.num_players = num_players
        self.populate_game(win_values=win_vals)
        self.to_admit = to_admit
        self.categories = categories
        self.game_mode_type = game_mode_type


    def populate_game(self, win_values:list[float]):
        '''
        Creates a list of blank players based on win_values. ONLY USED IN INITIALIZATION
        '''
        self.players = []
        for i in range(self.num_players):
            self.players.append(Player(win_value=win_values[i]))

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

game = Game(players=[Player(60), Player(40)], categories=[Category(size=12, std=1, mean=2, name="Q1"), Category(size=24, std=2, mean=1, name="Q2")])
for player in game.players:
    player.set_strategy(game, [0.5, 0.6])

game.simulate_game()
