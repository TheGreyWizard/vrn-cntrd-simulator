import numpy as np

class EnvironmentDensity:
    gaussian_centers = None
    gaussian_multiplier = None

    environment_density = None

    def __init__(self, density_function_config, polygon_samples):
        self.gaussian_centers = density_function_config.gaussian_centers
        self.gaussian_multiplier = density_function_config.gaussian_multiplier

        self.environment_density = self.calculate_gaussian_cumulative_density(polygon_samples)

    def calculate_gaussian_cumulative_density(self, polygon_sample_points):
        all_phi = []
    
        for i in self.gaussian_centers:
            all_phi.append(self.calculate_gaussian(polygon_sample_points,i[0],i[1]))

        cumulative_density = np.sum(all_phi, axis=0)

        return cumulative_density

    def calculate_gaussian(self, points, x_center, y_center):
        phi = []

        for i in range(len(points)):
            sqdist_x = (points[i][0] - x_center)**2
            sqdist_y = (points[i][1] - y_center)**2
            phi.append(np.exp(self.gaussian_multiplier*(- sqdist_x - sqdist_y)))
        
        return np.asarray(phi)
