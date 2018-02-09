from tqdm import tqdm
import click
import numpy as np
from scipy import ndimage


@click.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.argument("output_file", type=click.Path())
@click.option("--height_map_left",
              type=click.Path(exists=True))
@click.option("--height_map_right",
              type=click.Path(exists=True))
@click.option("--shape",
              nargs=3,
              type=int)
def main(input_file, output_file, height_map_left, height_map_right, shape):
    """
    (1) Read height maps
    """
    map_left = ndimage.imread(height_map_left)
    map_right = ndimage.imread(height_map_right)

    """
    (2) Load Distance ridge
    """
    vol_temp = np.memmap(input_file,
                         dtype=np.dtype(">f4"),
                         mode='readonly',
                         shape=shape,
                         order='C')
    
    """
    (3) Initialize new ridge
    """
    vol_temp_new = np.memmap(output_file,
                         dtype=np.dtype(">f4"),
                         mode='write',
                         shape=shape,
                         order='C')
    
    """
    (4) Write new Ridge
    """
    for z in tqdm(range(map_left.shape[0])):
        for y in range(map_left.shape[1]):
            # Write LEFT IMAGE
            vol_temp_new[z,y,:] = vol_temp[z,y,:]
            length = int(map_left[z, y])
            vol_temp_new[z,y,:length] = 0
            
            # Write RIGHT IMAGE
            length_r = int(map_right[z,y])
            vol_temp_new[z,y,length_r:] = 0
            
    
    print("writing")
    vol_temp_new.flush()


if __name__ == "__main__":
    main()
