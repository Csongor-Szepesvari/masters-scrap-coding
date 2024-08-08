'''
This program calculates the number of different combinations in k bins with n items to split up into k bins
'''
import time as t
memo = {}
def num_combinations(num_items: int, num_bins: int) -> int:
    # Base case: if there are 2 bins, we have num_items + 1 options
    if num_bins == 2:
        return num_items + 1
    
    # If the problem was already solved elsewhere, just store it
    elif (num_items, num_bins) in memo:
        return memo[(num_items, num_bins)]
    
    # If the problem is unsolved, solve it by breaking it down into its components
    else:
        num_combos = 0
        for i in range(num_items+1):
            num_combos += num_combinations(num_items-i, num_bins-1)
        memo[(num_items, num_bins)] = num_combos
        print(num_items, "items distributed into", num_bins, "boxes has", num_combos, "combinations")
        return num_combos
    

begin = t.time()
val = num_combinations(200,4)
end = t.time()

print("Calculated the number of possible combinations for 50 items to go into 5 bins to be:", val)
print("This calculation took", end-begin, "seconds")
#print(memo)
