import matplotlib.pyplot as plt
import csv
import pandas as pd
import numpy as np

csv_file_path = "mean_dict.csv"
path2 = "std_dict.csv"
# first we have to import the data from 'nested_dict.csv'
# Read the CSV file into a DataFrame, handling missing values
# You can specify parameters like 'na_values', 'keep_default_na', 'na_filter' to handle missing data
# For example, 'na_values' can be used to specify additional strings to recognize as NaN (Not a Number)
# 'keep_default_na' can be set to False to prevent default NaN recognition
# 'na_filter' can be set to False to prevent converting any values to NaN
# You can adjust these parameters based on how your missing data is represented in the CSV file
df = pd.read_csv(csv_file_path, na_values=['', 'NA', 'N/A'], keep_default_na=True, na_filter=True)
df2 = pd.read_csv(path2, na_values=['', 'NA', 'N/A'], keep_default_na=True, na_filter=True)
print(df.head())

def translate_vals(z_scores:np.array, mu:float, std:float):
    return (z_scores * std) + mu



x_values = [i+1 for i in range(14)]
line_types = [i for i in range(5,28,3)]
colours = ["deepskyblue", "orange", "lime", "magenta", "crimson", "blue", "yellow", "forestgreen"]


print(line_types)

select = list(map(lambda x: x+"th largest", map(str, x_values)))
print(select)


for i in range(len(line_types)):
    #print(df[df["num_samples"] == line_types[i]])
    y_values = np.array(df[df["num_samples"] == line_types[i]][select])
    y_values = y_values[~np.isnan(y_values)]
    y_values = translate_vals(y_values)
    #print(y_values)

    y_up = np.array(df2[df2["num_samples"] == line_types[i]][select])
    y_up = y_up[~np.isnan(y_up)]
    
    y_down = y_values - 2 * y_up
    y_up = y_values + 2 * y_up
    
    x_vals = x_values[:len(y_values)]
    # plot them, making sure to cut it back where nan appears for the values
    plt.plot(x_vals, y_values, label="# of samples: "+str(line_types[i]), color=colours[i])
    plt.scatter(x_vals, y_values, color=colours[i])

    # add error bars
    #plt.fill_between(x_vals, y_down, y_up, alpha=0.1, color=colours[i])


# labeling the plot
plt.xlabel('The k-th largest')
plt.ylabel("Z-score achieved")
plt.title("Mapping z-score achieved against number of samples")


# add a legend
plt.legend()

# and finally show
plt.show()


