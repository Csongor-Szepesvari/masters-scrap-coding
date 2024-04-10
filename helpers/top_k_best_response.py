import numpy as np
import pandas as pd
import time as t

df = pd.read_csv('mean_dict.csv', na_values=['', 'NA', 'N/A'], keep_default_na=True, na_filter=True)


def df_lookup(num_samples:int, top_k:int)->float:
    '''
    Uses global dataframe containing z-scores to do a lookup of what the expected z score is with a given number of samples at the k-th position
    /params/
        num_samples : int; The number of students to admit
        top_k : int; The k-th largest to get
    /returns/
        z-score : float; The sampled z-score of that lookup
    '''
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


def best_resposne(enemy_strategy, to_admit, blind=False) -> dict[str, float]:
    '''
    
    '''
    raise ValueError('best_response not implemented as it requires some other functions to be implemented first')

def construct_search