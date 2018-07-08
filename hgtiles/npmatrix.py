import math
import numpy as np

def tileset_info(grid):
    '''
    Get the tileset info for the grid
    '''
    bin_size = 256
    max_dim = max(grid.shape)
    max_zoom = math.ceil(math.log(max_dim / bin_size) / math.log(2))
    max_width = 2 ** max_zoom * bin_size
    
    if len(grid.shape) > 2:
        raise ValueError("Grid's shape is not conducive to plotting", grid.shape)
    return {
        "max_width": max_width,
        "min_pos": [0,0],
        "max_pos": grid.shape,
        "max_zoom": max_zoom,
        "mirror_tiles": "false",
        "bins_per_dimension": bin_size
    }

def tiles(grid, z, x, y, nan_grid=None, bin_size=256):
    '''
    Return tiles at the given positions.
    
    Parameters
    -----------
    grid: np.array
        An nxn array containing values
    z: int
        The zoom level (0 corresponds to most zoomed out)
    x: int
        The x tile position
    y: int
        The y tile position
    bin_size: int
        The number of values per bin
    '''
    max_dim = max(grid.shape)
    print("max_dim", max_dim)
    
    max_zoom = math.ceil(math.log(max_dim / bin_size) / math.log(2))
    max_width = 2 ** max_zoom * bin_size
    
    print("max_width:", max_width)
    
    tile_width = 2 ** (max_zoom - z) * bin_size
    print("tile_width", tile_width)
    x_start = x * tile_width
    y_start = y * tile_width
    
    x_end = min(grid.shape[0], x_start + tile_width)
    y_end = min(grid.shape[1], y_start + tile_width)
    
    print("x_start:", x_start, x_end)
    print("y_start:", y_start, y_end)
    
    num_to_sum = 2 ** (max_zoom - z)
    print("num_to_sum", num_to_sum)
    
    data = grid[x_start:x_end,y_start:y_end]
    
    # add some data so that the data can be divided into squares
    divisible_x_width = num_to_sum * math.ceil(data.shape[0] / num_to_sum)
    divisible_y_width = num_to_sum * math.ceil(data.shape[1] / num_to_sum)

    divisible_x_pad = divisible_x_width - data.shape[0]
    divisible_y_pad = divisible_y_width - data.shape[1]
    print("data.shape", data.shape)
    
    a = np.pad(data, ((0, divisible_x_pad),(0,divisible_y_pad)), 'constant', constant_values=(0,0))
    b = np.nansum(a.reshape((a.shape[0],-1,num_to_sum)),axis=2)
    ret_array = np.nansum(b.T.reshape(b.shape[1],-1,num_to_sum),axis=2).T    
    
    if nan_grid is not None:
        print("normalizing")
        # we want to calculate the means of the data points
        not_nan_data = not_nan_grid[x_start:x_end,y_start:y_end]
        na = np.pad(not_nan_data, ((0, divisible_x_pad),(0,divisible_y_pad)), 'constant', constant_values=(0,0))
        nb = np.nansum(na.reshape((na.shape[1],-1,num_to_sum)), axis=2)    
        norm_array = np.nansum(nb.T.reshape(nb.shape[1],-1,num_to_sum),axis=2).T
        
        ret_array = ret_array / norm_array
    
    # determine how much to pad the array
    x_pad = bin_size - ret_array.shape[0]
    y_pad = bin_size - ret_array.shape[1]
    
    print("ret_array:", ret_array.shape)
    print("x_pad:", x_pad, "y_pad:", y_pad)

    return np.pad(ret_array, ((0,x_pad),(0,y_pad)), 'constant', constant_values=(np.nan, np.nan))