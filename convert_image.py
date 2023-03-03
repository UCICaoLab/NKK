# convert atomistic model to image

import time
import numpy as np
import pandas as pd
from scipy import spatial

class convert_image():
    
    def __init__(self, number_of_cpus):
        
        self.number_of_cpus = number_of_cpus

        pass    
    
    def crop_ball_data(self, vacancy_id, vacancy_coordinates, data, bounds, cutoff, remove_vacancy_flag):

        # kdtree search
        kdtree = spatial.cKDTree(data=data[:, 2:5], boxsize=bounds)
        neighbor_index = kdtree.query_ball_point(vacancy_coordinates, r=cutoff, workers=self.number_of_cpus)
        
        # print(neighbor_index)

        # print("neighbor_index:", neighbor_index)
        if remove_vacancy_flag == True:

            neighbor_index.remove(vacancy_id - 1) # this is only true when atom id is sorted
 
        return data[neighbor_index, :] # atoms within the cutoff distance
    
    def center_data(self, translation_vector, data, bounds):
        
        shifted_coordinates = data[:, 2:5] - translation_vector
        shifted_coordinates -= np.round(shifted_coordinates / bounds) * bounds
        
        return np.c_[data[:, :2], shifted_coordinates]
    
    def rotate_mirror_data(self, data, translation_vector, vector):
        
        x, y, z = vector # vector to be rotated
        
        data[:, 2:] = data[:, 2:] - translation_vector
        
        # rotation conditions
        if x >= 0:
            if y >= 0:
                theta = 0
            else:
                theta = np.pi / 2
        else:
            if y >= 0:
                theta = - np.pi / 2
            else:
                theta = np.pi
        
        rotation_matrix = [[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]]
        
        rotated_xy = np.dot(rotation_matrix, data[:, 2:4].T).T
        rotated_data = np.c_[data[:, :2], rotated_xy, data[:, -1]]
        
        # mirror conditions
        if z < 0:
            rotated_data[:, -1] = - rotated_data[:, -1]

        rotated_data[:, 2:] += translation_vector
        
        # vector connecting vacancy and neighor atom always points along [111] direction;
        return rotated_data
    
    def create_mesh(self, cutoff, voxel_size):
        
        number_of_voxels_in_one_side = np.round(cutoff / voxel_size - 0.5).astype(np.int32)
        mesh_shape = [2 * number_of_voxels_in_one_side + 1] * 3
        mesh_size = [(2 * number_of_voxels_in_one_side + 1) * voxel_size] * 3

        x = y = z = np.arange(-number_of_voxels_in_one_side, number_of_voxels_in_one_side + 1) * voxel_size + 0.5 * mesh_size[0]
        mesh_x, mesh_y, mesh_z = np.meshgrid(x, y, z) 
        mesh_x, mesh_y, mesh_z = mesh_x.reshape(-1, 1), mesh_y.reshape(-1, 1), mesh_z.reshape(-1, 1)    
        mesh = np.c_[mesh_x, mesh_y, mesh_z]

        return mesh, np.array(mesh_shape), np.array(mesh_size)

    def convert_data_to_image(self, data, mesh_info):
        
        mesh, mesh_shape, mesh_size = mesh_info 
        
        kdtree = spatial.cKDTree(data=mesh, boxsize=mesh_size)
        
        distance, index = kdtree.query(data[:, 2:5], k=1, workers=self.number_of_cpus)
        
        intensity = np.zeros(len(mesh))
        intensity[index] = data[:, 1] # using atom type to represent voxel intensity
        
        return intensity.reshape(tuple(mesh_shape)) # image intensity
