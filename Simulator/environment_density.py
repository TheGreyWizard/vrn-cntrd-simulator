import numpy as np

class EnvironmentDensity:
    
    """
    Summary: Calculates the gaussian density for the sampled enviroment and provides the values for simulation

    Gaussian center and variance factor configurable
    """

    def __init__(self, density_function_config, polygon_samples):
        self.gaussian_centers = density_function_config.gaussian_centers
        self.variance_factor = density_function_config.variance_factor

        self.environment_density = self.calculate_gaussian_cumulative_density(polygon_samples)

    def calculate_gaussian_cumulative_density(self, polygon_sample_points):

        """
        Summary: Calculate the gaussian density at all the sampled points in the polygon
        """

        all_phi = []

        # If no centers are provided, returns a uniform distribution
        if(len(self.gaussian_centers) == 0):
            return np.ones(len(polygon_sample_points))

        # Calculate and append gaussian values for each center
        for i in self.gaussian_centers:
            all_phi.append(self.calculate_gaussian(polygon_sample_points,i[0],i[1]))

        # Sum all gaussian functions
        cumulative_density = np.sum(all_phi, axis=0)

        return cumulative_density

    def calculate_gaussian(self, points, x_center, y_center):

        """
        Summary: Calculates the gaussian density at all the sampled points in the polygon for each gaussian center
        """

        phi = []

        for i in range(len(points)):
            sqdist_x = (points[i][0] - x_center)**2
            sqdist_y = (points[i][1] - y_center)**2
            phi.append(np.exp(self.variance_factor*(- sqdist_x - sqdist_y)))
        
        return np.asarray(phi)
