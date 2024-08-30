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
    def __init__(self, players:list[player], categories:list[category], game_mode_type:str):
        self.players = players
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
            
        
    def calc_collisions(self, cat_size):
        '''
        This function calculates the number of collisions in a category
        '''

game = Game(players=[Player(60), Player(40)], categories=[Category(size=12, std=1, mean=2, name="Q1"), Category(size=24, std=2, mean=1, name="Q2")])
for player in game.players:
    player.set_strategy(game, [0.5, 0.6])

game.simulate_game()
