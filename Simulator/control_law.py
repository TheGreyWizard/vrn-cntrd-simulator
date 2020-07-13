from scipy import integrate
from scipy.spatial import Voronoi
import numpy as np

import matplotlib.pyplot as plt

from shapely.geometry import Polygon
from matplotlib.path import Path

import random

from FiniteVoronoiTesselection import voronoi_finite_polygons_2d

class SimulationController:

    """
    Summary: Controller for the simulation. Initializes the robots and runs the VRN-CNTRD calculations
    """

    robot_positions = []

    def __init__(self, simulation_controller_config, simulation_environment):
        
        self.Q = simulation_environment.sample_points
        self.no_iterations = simulation_controller_config.no_iterations
        self.k_prop = simulation_controller_config.k_prop
        self.no_robots = simulation_controller_config.no_robots

        self.polygon = Polygon(simulation_environment.polygon_coords)
        self.resolution = simulation_environment.resolution
    
    def get_voronoi_region_in_environment(self, region, vertices):

        """
        Summary: Clips the received voronoi region with the outer polygon to get voronoi's external vertices
        """

        poly = Polygon(vertices[region])
        # Clipping voronoi region to outer polygon
        poly = poly.intersection(self.polygon)
        polygon_vertices = [p for p in poly.exterior.coords]

        return polygon_vertices

    def initialize_robots(self, initial_plt):

        """
        Summary: Initializes robot agents and calculates voronoi tesselection at t=0
        """

        for i in range(self.no_robots):
            index = random.randint(0,len(self.Q))
            self.robot_positions.append(self.Q[index])
        
        robot_x, robot_y = zip(*self.robot_positions)
        initial_plt.scatter(robot_x, robot_y, marker='x', color='white')

        vor = Voronoi(self.robot_positions)
        regions, vertices = voronoi_finite_polygons_2d(vor)

        for index in range(len(regions)):
            polygon_vertices = self.get_voronoi_region_in_environment(regions[index], vertices)
            initial_plt.plot(*zip(*polygon_vertices), color='black')

    def run_simulation(self, cumulative_density, plt_axes):

        """
        Summary: Runs the simulation
        """
        
        for i in range(self.no_iterations):

            print("Iteration: ", i)

            # Conduct finite voronoi tesselection of robot positions
            vor = Voronoi(self.robot_positions)
            regions, vertices = voronoi_finite_polygons_2d(vor)
            robot_polygons = []

            cost = 0

            for index in range(len(regions)):

                # Get voronoi partition wrt the environment
                polygon_vertices = self.get_voronoi_region_in_environment(regions[index], vertices)
                robot_polygons.append(polygon_vertices)
                
                # Mask the overall environment sample to the voronoi polygon
                polygon_boundary = Path(polygon_vertices)
                voronoi_mask = polygon_boundary.contains_points(self.Q)

                # Calculate centroid
                centroid = self.calculate_centroid(voronoi_mask, cumulative_density)

                # Implementing the continuous time equation: pi = pi - kprop * (pi - Cvi)
                new_position = list(map(lambda i, j: i - self.k_prop * (i - j), self.robot_positions[index], centroid)) 

                # Plot movement and update position
                plt_axes.plot([self.robot_positions[index][0], new_position[0]], [self.robot_positions[index][1], new_position[1]], color="blue")
                self.robot_positions[index] = new_position

                cost += self.calculate_cost(voronoi_mask, cumulative_density, new_position)

            print("Cost: ", cost)

        print("Final Cost: ", cost)
        print("Done")

        return robot_polygons

    def calculate_polygon_mass(self, voronoi_mask, density_vals):
        
        """
        Summary: Polygon mass calculation for a voronoi polygon
        """

        polygon_density_vals = []
        
        # Get all density values inside the polygon
        for i in range(0,len(voronoi_mask)):
                if(voronoi_mask[i]):
                    polygon_density_vals.append(density_vals[i])
        
        # Integrate along the clipped density function
        return integrate.simps(polygon_density_vals, dx=self.resolution)

    def calculate_centroid(self, voronoi_mask, density_vals):

        """
        Summary: Centroid calculation for a voronoi polygon with given density function
        """

        # Calculate mass
        mass = self.calculate_polygon_mass(voronoi_mask, density_vals)

        x_density = []
        y_density = []

        # Calculate x and y surface density values for voronoi region
        for i in range(0,len(voronoi_mask)):
                if(voronoi_mask[i]):
                    x_density.append(self.Q[i][0] * density_vals[i])
                    y_density.append(self.Q[i][1] * density_vals[i])
        
        # Integrate along the centroid calculation function
        centroidx = integrate.simps(x_density, dx=self.resolution) / mass
        centroidy = integrate.simps(y_density, dx=self.resolution) / mass
        
        return (centroidx, centroidy)
        
    def calculate_cost(self, voronoi_mask, density_vals, robot_position):

        """
        Summary: Polar moment of inertia calculation to monitor the overall cost of the deployment
        """

        d_cost = []

        # Calculate the polar moment of inertia for each sample
        for i in range(0,len(voronoi_mask)):
                if(voronoi_mask[i]):
                    distance = (self.Q[i][0] - robot_position[0])**2 + (self.Q[i][1] - robot_position[1])**2
                    d_cost.append(distance * density_vals[i])
        
        # Integrate along the function
        cost = integrate.simps(d_cost, dx=self.resolution)
        
        return cost