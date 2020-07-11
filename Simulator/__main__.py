import matplotlib.pyplot as plt
import numpy as np

import argparse
import os

from config_service import ConfigService
from simulation_environment import SimulationEnvironment
from environment_density import EnvironmentDensity
from control_law import SimulationController

parser = argparse.ArgumentParser(description='Start simulation based on provided config')
parser.add_argument('--config', type=str, help='path of config file to override default')

dir_path = os.path.dirname(os.path.realpath(__file__))
config_file_path = dir_path + '/config.json'

if __name__ == "__main__":

    args = parser.parse_args()
    if args.config:
        config_file_path = args.config

    config = ConfigService(config_file_path)

    environment = SimulationEnvironment(config.environment_config)
    density = EnvironmentDensity(config.density_function_config, environment.sample_points)

    #TODO: Cleanup this area
    x, y = zip(*environment.sample_points)

    plt.scatter(x,y, c=density.environment_density)

    #TODO: Use config variables
    no_iterations = 10
    no_robots = 10

    controller = SimulationController(environment.polygon_coords, environment.sample_points, no_robots, no_iterations)
    robot_positions, robot_polygons = controller.run_simulation(density.environment_density, environment.resolution)
    
    robot_x, robot_y = zip(*robot_positions)
    plt.scatter(robot_x, robot_y, marker='o', color='red')

    for polygon in robot_polygons:
        plt.fill(*zip(*polygon), alpha=0.4)

    # plt.fill(*zip(*polygon_vertices), alpha=0.4)
    plt.show()