import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path
from scipy.spatial import Voronoi, voronoi_plot_2d
import numpy as np
import random

#Define Polygonal Environment

polygon_coords = [(0,0), (2.125,0),(2.9325,1.5),(2.975,1.6),
(2.9325,1.7),(2.295,2.1),(0.85,2.3),(0.17,1.2),(0,0)] #TODO: Make it customizable

resolution = 0.01 #TODO: Use it

environment_polygon = Path(polygon_coords) # make a polygon

fig, ax = plt.subplots()
patch = patches.PathPatch(environment_polygon, facecolor='None')
ax.add_patch(patch)
ax.set_xlim(-1, 4)
ax.set_ylim(-1, 4)

#Define agents

no_robots = 10

#Define pdf

def generate_sample_points(polygon):
    resultx = []
    resulty = []

    x, y = np.meshgrid(np.arange(0,3,0.01), np.arange(0,3,0.01))
    x, y = x.flatten(), y.flatten()
    points = np.vstack((x,y)).T

    grid = polygon.contains_points(points)

    for i in range(0,len(grid)):
            if(grid[i]):
                resultx.append(points[i][0])
                resulty.append(points[i][1])

    return resultx, resulty


x, y = generate_sample_points(environment_polygon)

robot_positions = []
for i in range(no_robots):
    index = random.randint(0,len(x))
    robot_positions.append([x[index], y[index]])

x, y = zip(*robot_positions)

plt.scatter(x,y)

vor = Voronoi(robot_positions)
vor_fig = voronoi_plot_2d(vor, show_vertices=False, line_colors='orange',
                line_width=2, line_alpha=0.6, point_size=2)

def calculate_centroid(vornoi_vertices):
    pass

plt.show()