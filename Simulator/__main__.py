import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path
from scipy.spatial import Voronoi, voronoi_plot_2d
import numpy as np
import random

from Control_Law import calculate_centroid

#Define Polygonal Environment

polygon_coords = [(0,0), (2.125,0),(2.9325,1.5),(2.975,1.6),
(2.9325,1.7),(2.295,2.1),(0.85,2.3),(0.17,1.2),(0,0)] #TODO: Make it customizable

gaussian_centers = [(2.15,.75), (1.,.25), (.725,1.75), (.25,.7)]

resolution = 0.01

#Define agents

no_robots = 10

#Define pdf

def generate_sample_points(polygon):
    masked_points = []

    x, y = np.meshgrid(np.arange(0,3,resolution), np.arange(0,3,resolution))
    x, y = x.flatten(), y.flatten()
    points = np.vstack((x,y)).T

    grid = polygon.contains_points(points)

    for i in range(0,len(grid)):
            if(grid[i]):
                masked_points.append(points[i])

    return masked_points


def calculate_densityFunction(points, x_center, y_center):
    phi = []

    for i in range(len(points)):
        sqdist_x = (points[i][0] - x_center)**2
        sqdist_y = (points[i][1] - y_center)**2
        phi.append(np.exp(6*(- sqdist_x - sqdist_y)))
    
    return np.asarray(phi)

if __name__ == "__main__":

    environment_polygon = Path(polygon_coords) # make a polygon

    Q = generate_sample_points(environment_polygon)

    fig, ax = plt.subplots()
    patch = patches.PathPatch(environment_polygon, facecolor='None')
    ax.add_patch(patch)
    ax.set_xlim(-1, 4)
    ax.set_ylim(-1, 4)

    robot_positions = []
    for i in range(no_robots):
        index = random.randint(0,len(Q))
        robot_positions.append([Q[index][0], Q[index][1]])
    
    all_phi = []
    
    for i in gaussian_centers:
        all_phi.append(calculate_densityFunction(Q,i[0],i[1]))

    cumulative_phi = all_phi[0] #account for unimodal gaussian distribution
    for i in range(1,len(all_phi)):
        temp_phi = all_phi[i]
        cumulative_phi = np.sum([cumulative_phi, temp_phi], axis=0)

    x, y = zip(*Q)
    robot_x, robot_y = zip(*robot_positions)

    centroid = calculate_centroid(environment_polygon, Q, cumulative_phi)

    plt.scatter(x,y, c=cumulative_phi)
    plt.plot([centroid[0]], [centroid[1]], marker='o', markersize=3, color="red")

    vor = Voronoi(robot_positions)

    plt.show()