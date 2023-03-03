# read input files

import numpy as np

def read_settings(file_name):

    f = open(file_name)
    lines = f.readlines()
    f.close()

    settings = [line.strip().split() for line in lines]

    return settings

def read_configurations(file_name, indexes):
    
    f = open(file_name)
    lines = f.readlines()
    f.close()
     
    dimensions = [line.strip().split() for line in lines[indexes[0]-1 : indexes[1]]]
    configurations = [line.strip().split() for line in lines[indexes[2]-1 : indexes[3]]]

    dimensions, configurations = np.array(dimensions).astype(np.float32), np.array(configurations).astype(np.float32)
     
    return dimensions, configurations
