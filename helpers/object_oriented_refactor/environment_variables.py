
class Player():
    def __init__(self, win_chance):
        self.strategy = {"Q1":0, "Q2":0, "Q3":0, "Q4":0}
        self.win_chance = win_chance
        
class Category():
    def __init__(self,mean,std,size):
        self.mean = mean
        self.std = std
        self.size = size
    
    def get_sample()


class Game():
    def __init__(self, num_candidates:int, category_sizes:list, eval_type:function, win_chances: list):
        self.players = [Player(win_chances[i]) for i in range(num_candidates)]


    def simulate_game(strategies : dict, num_candidates: int, sizes: list, eval_type: function, break_vals: list) -> dict:
        '''
        Simulate game takes all of the variables which define an admissions game environment and simulates the actual outcomes.
        It returns a dictionary of the utilities achieved by each player
        '''