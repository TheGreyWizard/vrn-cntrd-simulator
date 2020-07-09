from scipy import integrate

def calculate_polygon_mass(polygon, points, density_vals):

    grid = polygon.contains_points(points)
    polygon_density_vals = []

    for i in range(0,len(grid)):
            if(grid[i]):
                polygon_density_vals.append(density_vals[i])
    
    #integrate along the clipped density function
    return integrate.simps(polygon_density_vals)

def calculate_centroid(polygon, points, density_vals):

    mass = calculate_polygon_mass(polygon, points, density_vals)
    grid = polygon.contains_points(points)

    x_density = []
    y_density = []

    for i in range(0,len(grid)):
            if(grid[i]):
                x_density.append(points[i][0] * density_vals[i])
                y_density.append(points[i][1] * density_vals[i])
    
    #integrate along the centroid calculation function
    centroidx = integrate.simps(x_density) / mass
    centroidy = integrate.simps(y_density) / mass
    
    return (centroidx, centroidy)
    