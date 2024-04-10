'''
This program calculates the number of different combinations in k bins with n items to split up into k bins
'''
import time as t
memo = {}
def num_combinations(num_items: int, num_bins: int) -> int:
    if num_bins == 2:
        return num_items + 1
    
    elif (num_items, num_bins) in memo:
        return memo[(num_items, num_bins)]
    
    else:
        num_combos = 0
        for i in range(num_items+1):
            num_combos += num_combinations(num_items-i, num_bins-1)
        memo[(num_items, num_bins)] = num_combos
        return num_combos
    

begin = t.time()
val = num_combinations(50,5)
end = t.time()

print("Calculated the number of possible combinations for 50 items to go into 5 bins to be:", val)
print("This calculation took", end-begin, "seconds")
#print(memo)
