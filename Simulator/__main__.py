import matplotlib.pyplot as plt

import argparse
import os

from config_service import ConfigParser
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

    config = ConfigParser(config_file_path)

    environment = SimulationEnvironment(config.environment_config)
    density = EnvironmentDensity(config.density_function_config, environment.sample_points)
    controller = SimulationController(config.simulation_controller_config, environment)

    fig, axes = plt.subplots(1,3)
    for axis in axes:
        environment.plot_polygon_bounds(axis)

    x, y = zip(*environment.sample_points)

    axes[0].scatter(x,y, c=density.environment_density)
    axes[2].scatter(x,y, c=density.environment_density)

    controller.initialize_robots(axes[0])
    robot_polygons = controller.run_simulation(density.environment_density, axes[1])
    
    robot_x, robot_y = zip(*controller.robot_positions)
    axes[1].scatter(robot_x, robot_y, marker='o', color='red')
    axes[2].scatter(robot_x, robot_y, marker='o', color='red')

    for polygon in robot_polygons:
        axes[2].plot(*zip(*polygon), color='black')

    plt.tight_layout()
    plt.show()