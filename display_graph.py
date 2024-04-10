import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Generating data
x = np.linspace(-5, 5, 100)
y = np.linspace(-5, 5, 100)
x, y = np.meshgrid(x, y)
z = np.sin(np.sqrt(x**2 + y**2))

# Creating figure and 3D axis
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plotting surface
surf = ax.plot_surface(x, y, z, cmap='viridis')

# Adding a color bar which maps values to colors
fig.colorbar(surf)

# Showing plot
plt.show()
