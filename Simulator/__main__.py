import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path
from scipy.spatial import Voronoi, voronoi_plot_2d
import numpy as np

#Define Polygonal Environment

polygon_coords = [(0,0), (2.125,0),(2.9325,1.5),(2.975,1.6),
(2.9325,1.7),(2.295,2.1),(0.85,2.3),(0.17,1.2),(0,0)] #TODO: Make it customizable

resolution = 0.01 #TODO: Use it

polygon = Path(polygon_coords) # make a polygon

fig, ax = plt.subplots()
patch = patches.PathPatch(polygon, facecolor='None')
ax.add_patch(patch)
ax.set_xlim(-1, 4)
ax.set_ylim(-1, 4)

#Define pdf

def density_gaussian(x_center, y_center):
    resultx = []
    resulty = []

    x, y = np.meshgrid(np.arange(0,3,0.01), np.arange(0,3,0.01)) # make a canvas with coordinates
    x, y = x.flatten(), y.flatten()
    points = np.vstack((x,y)).T
    print(points)

    grid = polygon.contains_points(points)

    for i in range(0,len(grid)):
            if(grid[i]):
                resultx.append(points[i][0])
                resulty.append(points[i][1])
    
    plt.scatter(resultx, resulty)

density_gaussian(0,0)

plt.show()