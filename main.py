# python program for diffusion simulations 

# import packages
import time
import random
import numpy as np
import pandas as pd
import scipy

# import user defined packages
import read_input
import write_output
import write_log
import preprocess
import convert_image
import predict_diffusion_barriers
import KMC

def main():
    
    # predefined physic constant
    attempt_frequency = 1e13
    boltzmann_constant = 8.617333e-5
    
    process_data = preprocess.preprocess()

    # read simulation settings
    settings = read_input.read_settings("INPUT")
    settings = {settings[i][0] : settings[i][1] for i in range(len(settings))}

    # preprocess settings
    settings = process_data.begin_of_program(settings)
    
    # simulation box & initial configuration
    indexes = (settings["dimensions_start_line"],
               settings["dimensions_end_line"], 
               settings["coordinates_start_line"],
               settings["coordinates_end_line"])

    dimensions, configurations = read_input.read_configurations(settings["initial_configuration"], indexes)
    
    simulation_box_lengths = dimensions[:, 1] - dimensions[:, 0]
    simulation_box_lengths = simulation_box_lengths.reshape((1, -1))

    # load model weights
    model_weights = np.load(settings["model_weights"], allow_pickle=True)

    '''    
    for i in range(10):
        path = "../../datasets/data/"
        print(predict_diffusion_barriers.predict(model_weights, np.load(path+"0-"+str(i)+".npy")))
    
    '''
    # generate a vacancy
    if settings["random_vacancy_generation_flag"] == True:
        vacancy_id = random.randint(1, settings["number_of_atoms"])
    else: 
        vacancy_id = settings["vacancy_id"]
    
    # dump the initial configuration
    if settings["dump_initial_configuration_flag"] == True:

        write_output.dump(settings["output_file"], 0, settings["number_of_atoms"], dimensions, configurations)

    # create instances
    image_conversion = convert_image.convert_image(settings["number_of_cpus"])
    KMC_process = KMC.KMC(attempt_frequency, boltzmann_constant, settings["temperature"], vacancy_id, settings["time_scale"])
    
    # mesh
    mesh_info = image_conversion.create_mesh(settings["image_cutoff"], settings["voxel_size"])
     
    # diffusion simulation   
    for step in range(settings["initial_step"], settings["number_of_steps"] + settings["initial_step"]):
        
        time_1 = time.time()
 
        # variables for log file
        variables = [step] + list(configurations[vacancy_id - 1, :])
        
        # 1. crop data with a ball
        cropped_data = image_conversion.crop_ball_data(vacancy_id,
                                                      configurations[vacancy_id - 1, 2 : 5],
                                                      configurations,
                                                      simulation_box_lengths[0],
                                                      settings["image_cutoff"],
                                                      True)
        
        # 2. move vacancy to origin with PBC       
        centered_data = image_conversion.center_data(configurations[vacancy_id - 1, 2 : 5], 
                                                     cropped_data,
                                                     simulation_box_lengths)

        # 3. adjust vacancy to center of mesh
        centered_data[:, 2 : 5] += 0.5 * mesh_info[-1]
            
        # 4. crop data with a ball to find nearest neighbors
        cropped_centered_data = image_conversion.crop_ball_data(0,
                                                               0.5 * mesh_info[-1], 
                                                               centered_data,
                                                               mesh_info[-1],
                                                               settings["first_nearest_neighbor_cutoff"],
                                                               False)
        
        neighbor_ids = cropped_centered_data[:, 0].astype(np.int32)
        
        # 5. get the diffusion direction vector
        vector_array = cropped_centered_data[:, 2:5] - 0.5 * mesh_info[-1]

        # 6. align the vector to [111] direction through proper rotation and mirror
        rotated_data_list = [image_conversion.rotate_mirror_data(centered_data.copy(), 0.5 * mesh_info[-1], vector_array[index, :]) for index in range(len(vector_array))]
        
        # 7. convert the local chemistry to image through on lattice representation
        image_array = np.array([image_conversion.convert_data_to_image(rotated_data, mesh_info).flatten() for rotated_data in rotated_data_list])
        
        # 8. predict diffusion barriers
        energy_barriers = predict_diffusion_barriers.predict(model_weights, image_array)
        
        pair_information = [neighbor_ids, energy_barriers]
        
        print(pair_information)        
        # kinetic Monte Carlo step 
        neighbor_info, jumping_time, configurations = KMC_process.execute_KMC(configurations, pair_information) 
        
        # update variables for log file 
        variables.insert(1, jumping_time)
        variables += neighbor_info
        
        time_2 = time.time()

        # print("time is ", time_2 - time_1)        
        # write log file
        if step % settings["number_of_log_steps"] == 0:
            
            write_log.write_log(settings["log_file"], variables)            
        
        # write dump file
        if step % settings["number_of_dump_steps"] == 0:
            
            write_output.dump(settings["output_file"], step, settings["number_of_atoms"], dimensions, configurations)            
        
        # modify vacancy id
        if "vacancy_update_flag" == True:
            if step % settings["number_of_steps_updating_vacancy"] == 0:     
   
                vacancy_id = random.randint(1, settings["number_of_atoms"])
        
    # close files    
    process_data.end_of_program(settings["log_file"])

    return 0

if __name__ == "__main__":
    
    main()
