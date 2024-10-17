import Game

'''
The task of this file is to manage the high level execution of simulations and the finding of optimal strategies for particular games.

The sort of things we're interested in varying over:
    1. The number of players
    2. The number of rounds (in order to characterize what sort of conditions need to exist to make it worth it to devote resources to not be blind in the long run)
    3. The blindness of different players 
    4. The informational value of blindness (i.e. how much information is revealed by differentiating between categories)
        4.1. This is the relative value of the information added by disambiguating between unconvetional high and low variables, representing the variance.
    5. The level of players/their naivety, and its consequences
'''

Game.game(num_players=2, to_admit=2, players:list[Player], categories:dict[str:Category], game_mode_type:str, top_k=None)

'''
Set up the conditions for each type of game we're investigating
'''
# Game specific setup
pct_high_to_admit = [i/100 for i in range(40, 71, 10)] # this needs to be scaled so it's 0.1, 0.2, 0.3, ..., 0.7
game_modes = ["expected", "top_k"]

# Player relevant variables
win_values_underdog = [i/100 for i in range(5, 51, 5)] # this is scaled so it's 0.05, 0.1, 0.15, ..., 0.5
blind_combos = [[False, False], [False, True]]
levels = [[100,0], [100,100]]

# Category relevant variables
high_low_ratio_means = [i/10 for i in range(11, 21)] # this needs to be scaled so it's 1.1, 1.2, 1.3, ..., 2.0
high_low_ratio_variances = [i/10 for i in range(11, 21)] # this needs to be scaled so it's 1.1, 1.2, 1.3, ..., 2.0
mean_variance_ratios = [i/100 for i in range(125, 301, 25)] # this needs to be scaled so it's 1.25, 1.5, 1.75, ..., 3.0
high_mean_probs = [i/10 for i in range(1, 5)] # this needs to be scaled so it's 0.1, 0.2, 0.3, 0.4
high_variance_probs = [i/10 for i in range(1, 5)] # this needs to be scaled so it's 0.1, 0.2, 0.3, 0.4

def categories_generator(high_low_ratio_mean, high_low_ratio_variance, mean_variance_ratio, high_mean_probability, high_variance_probability):
    '''
    This function generates categories based on the parameters provided. The parameters are as follows:
    high_low_ratio_mean: The ratio of the means of *conventionally* high talented students and conventionally low talented students.
    high_low_ratio_variance: The ratio of the variances of *unconventionally* high talented students and conventionally low talented students.
    mean_variance_ratio: The ratio of the mean to the variance of the students in each category. (Ex. A mean of 10 and a variance of 1 would have a mean_variance_ratio of 10).
    high_mean_probability: The probability that a student is *conventionally* high talented.
    high_variance_probability: The probability that a student is *unconventionally* high talented.
    '''
    categories = {}
    default_mean = 10
    epsilon = 1/100
    default_population = 120
    categories["Q1"] = Game.Category.Category(name="Q1", mean=default_mean+epsilon, std=default_mean/mean_variance_ratio, size=int(default_population*high_mean_probability*high_variance_probability))
    categories["Q2"] = Game.Category.Category(name="Q2", mean=default_mean, std=default_mean/(mean_variance_ratio*high_low_ratio_variance), size=int(default_population*high_mean_probability*(1-high_variance_probability)))
    categories["Q3"] = Game.Category.Category(name="Q3", mean=default_mean*high_low_ratio_mean+epsilon, std=default_mean/mean_variance_ratio, size=int(default_population*(1-high_mean_probability)*high_variance_probability))
    categories["Q4"] = Game.Category.Category(name="Q4", mean=default_mean*high_low_ratio_mean, std=default_mean/(mean_variance_ratio*high_low_ratio_variance), size=int(default_population*(1-high_mean_probability)*(1-high_variance_probability)))

    return categories

# temporary placeholder, will extend to more players later
def generate_players(blind_combo, level, win_value_underdog):
    players = []
    players.append(Game.Player(blind=blind_combo[0], level=level[0], win_value=win_value_underdog))
    players.append(Game.Player(blind=blind_combo[1], level=level[1], win_value=1-win_value_underdog))
    return players
'''
We set up the multiprocessing process we're going to use
'''

from multiprocessing import Pool

for pct_admit in pct_high_to_admit:
    for win_value in win_values_underdog:
        for blind_combo in blind_combos:
            for level in levels:
                for high_low_ratio_mean in high_low_ratio_means:
                    for high_low_ratio_variance in high_low_ratio_variances:
                        for mean_variance_ratio in mean_variance_ratios:
                            for high_mean_probability in high_mean_probs:
                                for high_variance_probability in high_variance_probs:
                                    categories = categories_generator(high_low_ratio_mean, high_low_ratio_variance, mean_variance_ratio, high_mean_probability, high_variance_probability)
                                    players = generate_players(blind_combo, level, win_value)
                                    to_admit = int(pct_admit*120*high_mean_probability)
                                    
                                    # create the game
                                    game = Game.Game(num_players=2, to_admit=to_admit, players=players, categories=categories, game_mode_type="expected", top_k=0.2*to_admit)
                                    # find the strategies using iterated best response
                                    game.find_strategies_iterated_br()
                                    # simulate 100 games to find the relative expected value of the underdog
                                    with Pool(processes=12) as pool:
                                        results = pool.map(game.simulate_game, range(100))


with Pool(processes=4) as pool:
    answers = pool.map(change_global, range(10))
    print(answers)
