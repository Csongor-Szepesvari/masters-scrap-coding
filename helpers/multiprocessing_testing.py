from multiprocessing import Pool

some_global = 10

def change_global(to_add):
    global some_global
    some_global += to_add
    def square():
        return some_global**2
    return square()

with Pool(processes=4) as pool:
    answers = pool.map(change_global, range(10))
    print(answers)