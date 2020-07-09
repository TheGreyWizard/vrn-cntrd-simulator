def calculate_polygon_mass(polygon, points, density_vals):

    grid = polygon.contains_points(points)
    mass = 0

    for i in range(0,len(grid)):
            if(grid[i]):
                mass = mass + density_vals[i]
    
    return mass

def calculate_centroid(polygon, points, density_vals):

    mass = calculate_polygon_mass(polygon, points, density_vals)
    grid = polygon.contains_points(points)

    centroidx = 0
    centroidy = 0

    for i in range(0,len(grid)):
            if(grid[i]):
                centroidx = centroidx + (points[i][0] * density_vals[i])
                centroidy = centroidy + (points[i][1] * density_vals[i])
    
    centroidx = centroidx / mass
    centroidy = centroidy / mass
    
    return (centroidx, centroidy)
    