from matplotlib.path import Path
import matplotlib.patches as patches
import numpy as np
import matplotlib.pyplot as plt

class SimulationEnvironment:

    """
    Summary: Creates the outer boundary for the simulation and generates samples within the environment for the simulation

    The bounds and sampling resolution are configurable, along with choosing the bounds of the sampling
    """

    def __init__(self, environment_config):
        
        self.polygon_coords = environment_config.polygon_coords
        self.resolution = environment_config.sample_resolution
        self.mesh_bounds = environment_config.sample_mesh_bounds

        self.polygon_bounds = Path(self.polygon_coords) # make a polygon
        self.sample_points = self.generate_sample_points()

    def generate_sample_points(self):
        
        """
        Summary: Generates sample points within the polygon
        """

        masked_points = []

        # Uses the provided mesh bounds and resolution to create a mesh of to encompass the polygon with points

        x, y = np.meshgrid(np.arange(self.mesh_bounds[0],self.mesh_bounds[1],self.resolution), np.arange(self.mesh_bounds[0],self.mesh_bounds[1],self.resolution))
        x, y = x.flatten(), y.flatten()
        points = np.vstack((x,y)).T

        # Based on the polygon bounds provided, filters and returns the points in the mesh that are contained within the polygon

        grid = self.polygon_bounds.contains_points(points)

        for i in range(0,len(grid)):
            if(grid[i]):
                masked_points.append(points[i])

        return masked_points

    def plot_polygon_bounds(self, plt_axis):

        # Receives a matplotlib axis to patch the polygon path to plot other simulation results

        patch = patches.PathPatch(self.polygon_bounds, facecolor='None')
        plt_axis.add_patch(patch)
        plt_axis.set_xlim(self.mesh_bounds[0] - 0.5, self.mesh_bounds[1] + 0.5)
        plt_axis.set_ylim(self.mesh_bounds[0] - 0.5, self.mesh_bounds[1] + 0.5)
