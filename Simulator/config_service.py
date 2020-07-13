import json

class EnvironmentConfig:
    """
    Summary: Configration data container for the environment
    """

    polygon_coords = None
    sample_resolution = None
    sample_mesh_bounds = None

    def __init__(self, node_config):
        self.polygon_coords = node_config['polygon_coords']
        self.sample_resolution = node_config['sample_resolution']
        self.sample_mesh_bounds = node_config['sample_mesh_bounds']

class DensityFunctionConfig:

    """
    Summary: Configration data container for the density function calculations
    """

    gaussian_centers = None
    variance_factor = None

    def __init__(self, server_config):
        self.gaussian_centers = server_config['gaussian_centers']
        self.variance_factor = server_config['variance_factor']

class SimulationControllerConfig:

    """
    Summary: Configration data container for the simulation controller
    """

    no_robots = None
    no_iterations = None
    k_prop = None

    def __init__(self, serial_config):
        self.no_robots = serial_config['no_robots']
        self.no_iterations = serial_config['no_iterations']
        self.k_prop = serial_config['k_prop']

class ConfigParser:

    """
    Summary: Parses the input json configuration file into data containers to be injected into further objects
    """

    environment_config = None
    density_function_config = None
    simulation_controller_config = None

    def __init__(self, config_file_path):
        self._read_config_file(config_file_path)

    def _read_config_file(self, config_file_path):
        with open(config_file_path) as config_file:
            json_data = json.load(config_file)
        
        self._read_environment_config(json_data)
        self._read_density_function_config(json_data)
        self._read_simulation_controller_config(json_data)

    def _read_environment_config(self, json_data):
        self.environment_config = EnvironmentConfig(json_data['environment_config'])

    def _read_density_function_config(self, json_data):
        self.density_function_config = DensityFunctionConfig(json_data['density_function_config'])

    def _read_simulation_controller_config(self, json_data):
        self.simulation_controller_config = SimulationControllerConfig(json_data['simulation_controller_config'])
