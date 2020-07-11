from scipy import integrate
from scipy.spatial import Voronoi
import numpy as np

import matplotlib.pyplot as plt

from shapely.geometry import Polygon
from matplotlib.path import Path

import random

from FiniteVoronoiTesselection import voronoi_finite_polygons_2d

class SimulationController:

    robot_positions = []
    no_iterations = None
    Q = None
    polygon = None

    def __init__(self, polygon_coords, Q, no_robots, no_iterations):
        
        self.no_iterations = no_iterations
        self.Q = Q
        self.polygon = Polygon(polygon_coords)

        for i in range(no_robots):
            index = random.randint(0,len(Q))
            self.robot_positions.append([Q[index][0], Q[index][1]])

    def run_simulation(self, cumulative_density, resolution):

        for i in range(self.no_iterations):

            print("Iteration: ", i)

            vor = Voronoi(self.robot_positions)
            regions, vertices = voronoi_finite_polygons_2d(vor)
            robot_polygons = []

            for index in range(len(regions)):
                region = regions[index]
                poly = Polygon(vertices[region])
                # Clipping polygon
                poly = poly.intersection(self.polygon)
                polygon_vertices = [p for p in poly.exterior.coords]
                robot_polygons.append(np.array(polygon_vertices))
                polygon = Path(polygon_vertices)

                centroid = self.calculate_centroid(polygon, self.Q, cumulative_density, resolution)

                plt.plot([vor.points[index][0], centroid[0]], [vor.points[index][1], centroid[1]], color="yellow")

                self.robot_positions[index] = centroid
        
        print("Done")
        
        return self.robot_positions, robot_polygons
    


    def calculate_polygon_mass(self, polygon, points, density_vals, resolution):

        grid = polygon.contains_points(points)
        polygon_density_vals = []

        for i in range(0,len(grid)):
                if(grid[i]):
                    polygon_density_vals.append(density_vals[i])
        
        #integrate along the clipped density function
        return integrate.simps(polygon_density_vals, dx=resolution)

    def calculate_centroid(self, polygon, points, density_vals, resolution):

        mass = self.calculate_polygon_mass(polygon, points, density_vals, resolution)

        grid = polygon.contains_points(points)

        x_density = []
        y_density = []

        for i in range(0,len(grid)):
                if(grid[i]):
                    x_density.append(points[i][0] * density_vals[i])
                    y_density.append(points[i][1] * density_vals[i])
        
        #integrate along the centroid calculation function
        centroidx = integrate.simps(x_density, dx=resolution) / mass
        centroidy = integrate.simps(y_density, dx=resolution) / mass
        
        return (centroidx, centroidy)
        