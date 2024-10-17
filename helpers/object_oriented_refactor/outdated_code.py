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
    for category in game.categories.values():
        self.strategy[category.get_name()] = strategy[category.get_name()]/(1-self.calculate_percentage_lost_to_others(other_players=other_players, category=category))
    




def numbers_to_pct(self, strategy, game):
    '''
    Converts a strategy dictionary with numbers into percentages
    '''
    strat = {}
    for category in game.categories.values():
        strat[category.get_name()] = strategy[category.get_name()]/category.get_size()

    return strat

def pct_to_numbers(self, strategy, game):
    '''
    Converts a strategy dictionary with percentages into numbers
    '''
    strat = {}
    for category in game.categories.values():
        strat[category.get_name()] = strategy[category.get_name()]*category.get_size()

    return strat