import numpy as np

def print_min_max_values(p_var_d0_ma, p_var_d1_ma, p_lat, p_lon):
    """
    Prints the minimum and maximum values of the provided variable (masked Array)
    along with their corresponding coordinates for specified depth levels.
    """
    depth_levels = [
        "depth 0", 
        "depth 1",
    ]
    for depth_level, p_var_ma in zip(depth_levels, [p_var_d0_ma, p_var_d1_ma]):
        min_value = p_var_ma.min()
        print("--------------------")
        print(f"min value {depth_level}: ", min_value)
        # Find the indices of the minimum value
        min_indices = np.where(p_var_ma == min_value)
        print(min_indices)
        min_lats = p_lat[min_indices[0]]
        min_lons = p_lon[min_indices[1]]
        print(f"Coordinates of minimum value {depth_level}: {list(zip(min_lats, min_lons))}")

        print("--------------------")
        max_value = p_var_ma.max()
        print(f"max value: {depth_level}", max_value)
        # Find the indices of the maximum value
        max_indices = np.where(p_var_ma == max_value)
        print(max_indices)
        max_lats = p_lat[max_indices[0]]
        max_lons = p_lon[max_indices[1]]
        print(f"Coordinates of maximum value {depth_level}: {list(zip(max_lats, max_lons))}")