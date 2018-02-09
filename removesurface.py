import numpy as np
from scipy import ndimage

if __name__ == "__main__":
    """
    (0) Define constants
    """
    height_map_left  = '/sls/X02DA/data/e13657/Data10/matteo_high_resolution/stitched_datasets/heightmaps/WT353_LL_smoke_left.tif' 
    height_map_right = '/sls/X02DA/data/e13657/Data10/matteo_high_resolution/stitched_datasets/heightmaps/WT353_LL_smoke_right.tif'
    
    distance_ridge = '/sls/X02DA/data/e13657/Data10/matteo_high_resolution/distance_ridges/WT353_LL_smoke_stitched_noncropped_EDT_5962x2558x2160.raw'
    distance_ridge_new = '/sls/X02DA/data/e13657/Data10/matteo_high_resolution/distance_ridges/WT353_LL_smoke_stitched_masked_EDT_5962x2558x2160.raw'
    
    ridge_shape = [2160,2558,5962]
    
    """
    (1) Read height maps
    """
    map_left = ndimage.imread(height_map_left)
    map_right = ndimage.imread(height_map_right)

    """
    (2) Load Distance ridge
    """
    vol_temp = np.memmap(distance_ridge,
                         dtype=np.float32,
                         mode='readonly',
                         shape=(ridge_shape[0],ridge_shape[1],ridge_shape[2]),
                         order='C')
    
    """
    (3) Initialize new ridge
    """
    vol_temp_new = np.memmap(distance_ridge_new,
                         dtype=np.float32,
                         mode='write',
                         shape=(ridge_shape[0],ridge_shape[1],ridge_shape[2]),
                         order='C')
    
    """
    (4) Write new Ridge
    """
    for z in range(0, map_left.shape[0]):
        for y in range(0, map_left.shape[1]):
            # Write LEFT IMAGE
            vol_temp_new[z,y,:] = vol_temp[z,y,:]
            length = int(map_left[z,y])
            vol_temp_new[z,y,0:length] = 0
            
            # Write RIGHT IMAGE
            length_r = int(map_right[z,y])
            vol_temp_new[z,y,length_r:ridge_shape[2]] = 0
            
    
    print("writing")
    vol_temp_new.flush()
    
