import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import pandas as pd

def import_csv_to_dataframe(csv_file):
    try:
        dataframe = pd.read_csv(csv_file)
        return dataframe
    except Exception as e:
        print("Error:", e)
        return None

df = import_csv_to_dataframe("results/output.csv")


df.info()

# make different types of selections
graph1 = df[(df["blind"]) & (df["mu_high"] == 0.35) & (df['sigma_high']==0.15) & (df["sigma_bonus"]==0.25)][["p_underdog", "proportion_mu_high_to_admit", "game_value"]]
graph2 = df[(df["blind"] == False) & (df["mu_high"] == 0.35) & (df['sigma_high']==0.15) & (df["sigma_bonus"]==0.25)][["p_underdog", "proportion_mu_high_to_admit", "game_value"]]
print(len(graph1))

# Generating data
X = np.array(graph1['p_underdog']).reshape((10, 10))
Y = np.array(graph1['proportion_mu_high_to_admit']).reshape((10,10))
#x, y = np.meshgrid(x, y)
Z = np.array(graph1['game_value']).reshape((10,10))

from matplotlib import cm
from matplotlib.ticker import LinearLocator


# set up a figure twice as wide as it is tall
fig = plt.figure(figsize=plt.figaspect(0.5))

# set up the axes for the first plot
ax = fig.add_subplot(1, 2, 1, projection='3d')

surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)
ax.set_zlim(0.25, 0.75)
# Labeling the axes
ax.set_xlabel('probability underdog winning collision')
ax.set_ylabel('proportion of high talent students to admit per school')
ax.set_zlabel('percent of total value acquired by underdog')

fig.colorbar(surf, shrink=0.5, aspect=10)



# ADD SECOND PLOT

ax = fig.add_subplot(1, 2, 2, projection='3d')

# Generating data
X = np.array(graph2['p_underdog']).reshape((10, 10))
Y = np.array(graph2['proportion_mu_high_to_admit']).reshape((10,10))
#x, y = np.meshgrid(x, y)
Z = np.array(graph2['game_value']).reshape((10,10))

surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)
ax.set_zlim(0.25, 0.75)
# Labeling the axes
ax.set_xlabel('probability underdog winning collision')
ax.set_ylabel('proportion of high talent students to admit per school')
ax.set_zlabel('percent of total value acquired by underdog')

fig.colorbar(surf, shrink=0.5, aspect=10)

plt.show()



