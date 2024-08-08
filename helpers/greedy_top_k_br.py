import numpy as np
import pandas as pd
import time as t
import math

df = pd.read_csv('mean_dict.csv', na_values=['', 'NA', 'N/A'], keep_default_na=True, na_filter=True)

'''
Notes:

'''
# we're going to have to localize these parameters to the individual games/cores
# GLOBAL PARAMETERS BELOW, WILL FIRST MAKE FOR SINGLE CORE PROCESSING THEN CHANGE IT UP FOR MULTIPROCESSING
categories = ["Q1","Q2","Q3","Q4"]
n = 120 # the number of students seeking admission
high_variance_frequency = 1/4 # the frequency of students displaying high talent in "unconvetional" traits
high_mean_frequency = 2/5 # the frequency of students displaying high talent by convetional metrics (like GPA, published papers, etc)
underdog_win_chance = 1/3 # the likelihood of the underdog winning if a student receives admissions from both
to_admit = int(.2 * n) # the number of students we wish to admit
top_k = int(.2 * to_admit)

def set_population_params(total_students: int, num_to_admit: int, prob_underdog: float, top_k_size: int) -> None:
    global n, to_admit, underdog_win_chance, top_k
    n = total_students
    to_admit = num_to_admit
    underdog_win_chance = prob_underdog
    top_k = top_k_size

size_dictionary = {}


# specify the sizes of each section in terms of integers
def set_dict_size():
    global size_dictionary
    f_sigma = high_variance_frequency # the percentage of students that are unconvetionally talented
    f_mu = high_mean_frequency # the percentage of students that are conventionally talented
    size_dictionary = {
        "Q1":round(f_sigma * f_mu * n),
        "Q2":round((1-f_sigma) * f_mu * n),
        "Q3":round(f_sigma * (1-f_mu) * n),
        "Q4":round((1-f_sigma) * (1-f_mu) * n)
    }

# specify the frequencies of each category type and then call the function to set the actual integers used
def set_freq(mu_high=2/5, sigma_high=1/4):
    global high_variance_frequency, high_mean_frequency
    high_variance_frequency=sigma_high
    high_mean_frequency=mu_high
    set_dict_size()



strategy_dictionary = {}

# set the strategies to zero between runs
def reset_strategies():
    # specify the agent strategies
    global strategy_dictionary
    strategy_dictionary = {
    "overdog":{
        "Q1":0,
        "Q2":0,
        "Q3":0,
        "Q4":0
    }, 
    "underdog":{
        "Q1":0,
        "Q2":0,
        "Q3":0,
        "Q4":0
    }}



# specify the parameters from distribution sampling
distribution_parameters = {}
category_to_distribution_values = {}
def set_distribution_parameters(mu_high: float, mu_low: float, sigma_high: float, sigma_low: float, sigma_high_bonus: float) -> None:
    '''High level function used to set our paramaters to whatever we like of the distributions of the different categories.
    
    Useful for running experiments with different proportions betweeen the different categories to model scenarios in which different features have greater benefits.
    
    Controlled by the ratio between mu_high and mu_low as well as sigma_high and sigma_low
    
    Inputs:
        mu_high: the mean value of a distribution that has the higher mu value
        mu_low: the mean value of a distribution that has the lower mu value
        sigma_high: the standard deviation of a distribution that has higher variance
        sigma_low: the standard deviation of a distribution that has a lower variance
        sigma_high_bonus: the bonus yielded to mu values from having a higher variance candidate
        
    Output:
        None: instead updates the dictionary that contains this information'''
    global distribution_parameters
    distribution_parameters = {
        "mu_high" : mu_high,
        "mu_low" : mu_low,
        "sigma_high" : sigma_high,
        "sigma_low" : sigma_low
    }

    distribution_parameters["sigma_high_bonus"] =  sigma_high_bonus * (distribution_parameters["mu_high"]-distribution_parameters["mu_low"])
    global category_to_distribution_values
    category_to_distribution_values = {
        "Q1" : [distribution_parameters["mu_high"]+distribution_parameters["sigma_high_bonus"],distribution_parameters["sigma_high"]],
        "Q2" : [distribution_parameters["mu_high"], distribution_parameters["sigma_low"]],
        "Q3" : [distribution_parameters["mu_low"]+distribution_parameters["sigma_high_bonus"],distribution_parameters["sigma_high"]],
        "Q4" : [distribution_parameters["mu_low"], distribution_parameters["sigma_low"]],
    }


set_distribution_parameters(mu_high=5.818,mu_low=4,sigma_high=2,sigma_low=1,sigma_high_bonus=0.1) # just use this for a default run, then later we can govern what goes on elsewhere
reset_strategies()
set_freq(mu_high=high_mean_frequency, sigma_high=high_variance_frequency)

'''
Alright population set up is done above.
'''


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
    #raise ValueError('df_lookup not currently implemented')



def time_testing():
    '''
    This function has no inputs and outputs and is only used to test how long a single search of the table takes
    '''
    st = t.time()
    for i in range(1, 51):
        for j in range(1, i+1):
            val = df_lookup(i, j)
    end = t.time()
    print("Doing a complete search of the relevant table takes", end-st, "seconds")


def convert_z_score(z_score:float, category:str) -> float:
    '''
    Converts a z_score to an actual value based on a category provided
    '''
    return category_to_distribution_values[category][0] + category_to_distribution_values[category][1]*z_score

'''
Generic helper functions are set up, now to get to the meat of the program
'''

def calc_collisions(category:str, strategies:dict)->float:
    '''
    This function calculates the number of collisions for a given category and the strategy dictionaries of both players as well as the sizes of each category
    '''
    try:
        return strategies["overdog"][category] * strategies["underdog"][category] / size_dictionary[category]
    except:
        raise ValueError('Some error occured, here were the strategy dictionaries', strategies, "\n And here are the conditions of collapse", to_admit)

def calc_max_size(strategies: dict[dict[str:int]], opposition_player: str) -> dict[str:int]:
    '''
    This function calculates the maximum number of students a player can possibly allocate to each category and returns it as a dictionary

    

    Math:
        For a given category with x candidates, if our opposition sends y invites the maximum we can admit for that category will be
            able_to_admit = (x - y) + (prob_winning * y)
    '''
    max_admitees = {}
    if opposition_player == "overdog":
        prob_win = underdog_win_chance
    else:
        prob_win = 1 - underdog_win_chance
    for key, value in strategies[opposition_player].items():
        # if we admit everyone, we will get

        # max_realized = size_dict - num_opp_selected*(opp_win_chance)
        max_admitees[key] = math.floor(size_dictionary[key] - value*(1-prob_win))

    return max_admitees

def opp(player):
    if player == "underdog":
        return "overdog"
    else:
        return "underdog"

def greedy_br(strategies, player, blind=False):
    '''
    This function calculates the approximate best response using a greedy method given an enemy strategy

    The best response functions takes:
        some enemy strategy (how much they're taking from each group)
        the number of desired students to admit
        and if we're best responding in a blind way
    '''
    
    '''
    Retrieve the maximum number of admittees per category based on the enemy strategy

    '''
    oppo = opp(player)
    max_admitees = calc_max_size(strategies, oppo)
    if player == "underdog":
        win_chance = underdog_win_chance
    else:
        win_chance = 1 - underdog_win_chance
    

    def eval_strat(strat:list[list[int]]) -> float:
        flattened_array = sorted(strat.reshape(-1), reverse=True)
        return sum(flattened_array[:top_k])


    '''
    Find the approximate best response by finding the marginal utility of putting one more weight onto each category for each admission
    '''
    strategy = [0,0,0,0]
    individual_top_ks = np.zeros((4 , top_k))
    value = 0
    best_increase = float('inf')
    #print(individual_top_ks)
    for i in range(to_admit):
        for j in range(4):
            cat = categories[j]
            print(cat, "category has", category_to_distribution_values[cat][0], "mean")
            print(cat, "category has", category_to_distribution_values[cat][1], "variance")
            print()
            max_cat_size = max_admitees[cat]
            if strategy[j] + 1 < max_cat_size:
                test_strat = strategy[:]
                test_strat[j] += 1
                # calculate the increase in valuation and compare
                test_indi_top_ks = individual_top_ks[:]
                for k in range(top_k):
                    # calculate the new valuation of the increased metric
                    if strategy[j]//2 >= k:
                        z_score = df_lookup(test_strat[j], k+1)
                        val = category_to_distribution_values[cat][0]+category_to_distribution_values[cat][1]*z_score
                        print(test_strat[j], "samples in", cat, "at k =", k+1, "has", val, "value")
                        print()
                        test_indi_top_ks[j][k] = val
                    else:
                        test_indi_top_ks[j][k] = 0
                        print(test_strat[j], "samples in", cat, "at k =", k+1, "has", 0, "value")
                        print()
                        break
                # evaluate the total value of the strategy
                print(test_indi_top_ks)
                test_val = eval_strat(test_indi_top_ks)
                # if its better, then store it for it later use
                if test_val >= value:
                    value = test_val
                    best_top_ks = test_indi_top_ks
                    best_increase = j
        
        print("It's best to increase", categories[best_increase], "by 1")
        print()
        individual_top_ks = best_top_ks
        strategy[best_increase] += 1

    print(size_dictionary)
    print(strategy_dictionary)
    print(max_admitees)
    print(player, "player thinks", strategy, "is best resposne")
    print()
        




    #print("the optimal strategy has been found and it is", strategies_array[max_index])
    # now that we found the optimal strategy set it equal to the players strategy dictionary

    # to do this we have to calculate this back to the strategies with collisions accounted for
    # admitees = x - # collisions + # collisions * prob_win
    # admitees = x - collisions(1-prob_win)
    # (admitees + collision(1-prob_win)) = x

    # realized = (invites - (1-win_chance)*collisions) because we subtract the number of collisions we lose
    # collisions needs to be calculated with invites
    # realized = invites - collisions + win_chance * collisions
    # collisions = invites/size * other_invites/size * size
    # so realized = invites - (1-win_chance)* invites * other_invites / size_category
    # realized = invites (1 - (1- win chance)*other_invites/size category)
    # realized / (1 - (other win)*other_rate)

    #print(strategies_array[max_index])
    for i in range(len(categories)):
        cat = categories[i]
        #if to_admit == 22 and top_k == 2:
        #    print(size_dictionary)
        #    num_collisions = calc_collisions(cat, strategy_dictionary)
        #    print(num_collisions)
        '''
        This line is not operating correctly, it should be able to max out a category from strategies_array, so we need to reverse the calcuation
        '''
        strategy_dictionary[player][cat] = min(size_dictionary[cat], round(strategy[i]/(1-(1-win_chance)*strategy_dictionary[oppo][cat]/size_dictionary[cat])))
    #print("successfully executed best response", strategy_dictionary)
    #print()

    #raise ValueError('best_response implementation not finished - current step is to calculate all possible admissions')



def evaluate_top_k(strategy: list[int], k: int) -> float:
    '''
    This function takes a possible strategy and evaluates the mean of the top k values of this strategy by using the lookup table and generating the top k for each category (where possible) and then evaluating the total top k
    Makes use of the global distribution_parameters dictionary which is used to get real values.
    '''

    # use df_lookup to recover top k for each category
    top_ks = []
    categories = ["Q1", "Q2", "Q3", "Q4"]
    for j in range(len(strategy)):
        sample_size = strategy[j]
        for i in range(k):
            if i+1<sample_size:
                # for the cases where k is less than the sample size, retrieve 
                z_score = df_lookup(sample_size, i+1)
                top_ks.append(convert_z_score(z_score, categories[j]))

    #print(top_ks)
    return sum(sorted(top_ks, reverse=True)[:k])/k

    
    #raise ValueError('assess_top_k not yet implemented')

def eval_game():
    under_val = evaluate_top_k(list(strategy_dictionary["underdog"].values()), top_k)
    over_val = evaluate_top_k(list(strategy_dictionary["overdog"].values()), top_k)
    #print("underdog achieved", under_val, "average top k score")
    #print("overdog achieved", over_val, "average top k score")
    return under_val/(over_val+under_val)

def play_game(epsilon=0.001):
    # uses player strategies and top_k to iterate best responses until convergence
    player1 = "underdog"
    player2 = opp(player1)
    #print(to_admit, top_k)
    difference1 = float('inf')
    difference2 = float('inf')
    iterations = 0
    while difference1 > epsilon or difference2 > epsilon:
        init1 = sum(strategy_dictionary[player1].values())
        greedy_br(strategy_dictionary, player1)
        difference1 = sum(strategy_dictionary[player1].values()) - init1
        
        
        init2 = sum(strategy_dictionary[player2].values())
        #print(strategy_dictionary[player2], init2)
        greedy_br(strategy_dictionary, player2)
        difference2 = sum(strategy_dictionary[player2].values()) - init2

        iterations += 1

        if iterations > 20:
            print("Potentially stuck")
            print(strategy_dictionary)
            break
        #print("After iteration, respective strategies are", strategy_dictionary)
        #print("difference between earlier strategy and cur strategy is", difference1, difference2)
        #print()

    percent_achieved_under = eval_game()
    """
    print(percent_achieved_under, "% achieved")
    print("respective strategies", strategy_dictionary)
    print("max sizes", size_dictionary)
    print()
    """
    return percent_achieved_under

def full_game(inputs: list) -> list:
    mean_to_std_diff_ratio:float = inputs[0]
    num_admit:int = inputs[1]
    prob_win_underdog:float = inputs[2]
    pop_frequencies:tuple[float,float] = inputs[3]
    # figure out distro params from the ratio
    # set the difference in mean to a standard 1
    # ratio * (hm-lm) = hv-lv
    # ratio * lm-hm + hv = lv
    hm = 1
    lm = 0
    # then use this as the basis for establishing the difference in variance
    hv = 1
    lv = mean_to_std_diff_ratio*(lm-hm) + hv
    
    set_distribution_parameters(mu_high=hm, mu_low=lm, sigma_high=hv, sigma_low=lv, sigma_high_bonus=.05)
    set_population_params(total_students=n, num_to_admit=num_admit, prob_underdog=prob_win_underdog, top_k_size=max(1, int(.2*num_admit)))
    set_freq(mu_high=pop_frequencies[0], sigma_high=pop_frequencies[1])

    print("playing game with", n, "students", num_admit, "admittees and ", top_k, "top k")
    print()
    pct_value = play_game()
    reset_strategies()
    return [prob_win_underdog, num_admit, pop_frequencies[0], pop_frequencies[1], mean_to_std_diff_ratio, pct_value]



#print(df_lookup(10, 3))
#best_response(strategy_dictionary, "underdog", blind=False)
#best_response(strategy_dictionary, "overdog", blind=False)
#print(strategy_dictionary)

from multiprocessing import Pool
#play_game()
#reset_strategies()


if __name__ == '__main__':
    # Setup the experiment to make the different runs, store the environment variables and the result as a line in a list
    mu_high_props = [i/100 for i in range(10, 80, 10)]
    sigma_high_props = mu_high_props[:]

    to_admit_prop = [i/100 for i in range(20, 100, 10)] # multiply this with the size of students and the frequency of mu_high to get the number of students to admit
    # if the value is stable in mu_high props in terms of proportion gained back we know we can ignore it

    p_underdogs = mu_high_props[:] # the probability of the underdog winning

    # the ratio of the difference between high mean - low mean vs high variance - low variance
    # ratio * (hm-lm) = (hv - lv)
    mean_to_std_difference_ratio = [i/100 for i in range(10, 100, 10)]


    reset_strategies()



    toExport = [["p_underdog", "proportion_mu_high_to_admit", "frequency_high_mu", "frequency_high_sigma", "mean_to_std_diff_ratio", "game_value"]]
    index = 1
    total = (len(p_underdogs)**3) * len(mean_to_std_difference_ratio) * len(to_admit_prop)
    #print(len(mu_high_props), total)
    games = []

    # probability that the underdog wins
    # for p in p_underdogs:

        # proportion of students to admit
    for admit_prop in to_admit_prop:

            # proportion of students that are high in talent by UNCONVENTIONAL metrics
            #for freq_hs in sigma_high_props:

                # proportion of students that are high in talent by CONVENTIONAL metrics
                #for freq_hm in mu_high_props:

                        # the ratio of the differences in values
                        for ratio in mean_to_std_difference_ratio:

                            # in order to use multiprocessing we have to localize all of our variables
                            # then we have to use Pool.map to get the results

                            # we create the array here to use for playing the game
                            
                            # the number of students we want to admit
                            to_admit_val = int(admit_prop * high_mean_frequency * n)
                            #print(admit_prop, freq_hm * n)

                            # add the game to the queue
                            games.append([ratio, to_admit_val, underdog_win_chance, (high_mean_frequency, high_variance_frequency)])
                            
                            
                            '''if index % 100 == 0:
                                print("Percentage done:", index/total*100)
                            index += 1'''


    num_games = len(games)
    print(num_games)
    games_high = []
    for i in range(0,num_games, num_games//4):
        games_high.append(games[i:min(num_games, i+(num_games//4))])

    # process them block by block to get a grasp on how well its operating
    pct = 0
    full_game(games[25])
    '''
    for games_block in games_high:
        print(pct, "% completed")
        with Pool(processes=20) as pool:
            toExport += pool.map(full_game, games_block)
        pct += 25
    '''
    '''
    with Pool(processes=20) as pool:
        results = pool.map(full_game, games)
    '''

    import csv

    def export_to_csv(data, filename):
        with open(filename, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            
            # Writing column names
            csv_writer.writerow(data[0])
            
            # Writing data rows
            for row in data[1:]:
                csv_writer.writerow(row)

    print("exporting to CSV")
    export_to_csv(toExport, "../results/output_top_k.csv")