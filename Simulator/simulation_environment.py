from matplotlib.path import Path
import matplotlib.patches as patches
import numpy as np

class SimulationEnvironment:

    polygon_coords = None
    polygon_bounds = None
    sample_points = None
    resolution = None
    mesh_bounds = None

    def __init__(self, environment_config):
        
        self.polygon_coords = environment_config.polygon_coords
        self.resolution = environment_config.sample_resolution
        self.mesh_bounds = environment_config.sample_mesh_bounds

        self.polygon_bounds = Path(self.polygon_coords) # make a polygon
        self.sample_points = self.generate_sample_points()

        self.plot_polygon_bounds

    def generate_sample_points(self):
        masked_points = []

        x, y = np.meshgrid(np.arange(self.mesh_bounds[0],self.mesh_bounds[1],self.resolution), np.arange(self.mesh_bounds[0],self.mesh_bounds[1],self.resolution))
        x, y = x.flatten(), y.flatten()
        points = np.vstack((x,y)).T

        grid = self.polygon_bounds.contains_points(points)

        for i in range(0,len(grid)):
            if(grid[i]):
                masked_points.append(points[i])

        return masked_points

    def plot_polygon_bounds(self):

        fig, ax = plt.subplots()
        patch = patches.PathPatch(self.polygon_bounds, facecolor='None')
        ax.add_patch(patch)
        ax.set_xlim(-1, 4)
        ax.set_ylim(-1, 4)
