# preprocess the settings for simulation

class preprocess():

    def __init__(self):

        pass 

    def begin_of_program(self, settings):

        # int parameter list
        int_parameter_list = ["number_of_atoms",
                              "dimensions_start_line",
                              "dimensions_end_line",
                              "coordinates_start_line",
                              "coordinates_end_line",
                              "vacancy_id",
                              "initial_step",
                              "number_of_steps",
                              "number_of_log_steps",
                              "number_of_dump_steps",
                              "number_of_steps_updating_vacancy",
                              "dump_initial_configuration_flag",
                              "vacancy_update_flag",
                              "random_vacancy_generation_flag",
                              "number_of_cpus"]

        float_parameter_list = ["image_cutoff",
                                "first_nearest_neighbor_cutoff",
                                "voxel_size",
                                "temperature"]
     
        string_parameter_list = ["initial_configuration",
                                 "model_weights",
                                 "units",
                                 "log_file",
                                 "output_file"]

        # list all required parameters
        name_list = int_parameter_list + float_parameter_list + string_parameter_list
    
        print(type(int(settings["number_of_steps"]))) 
        print("number of steps", int(settings["number_of_steps"]))
        for name in name_list:
            print("%-40s" % name, settings[name])

        # convert type of parameters
        for name in int_parameter_list:
            settings[name] = int(settings[name])
        for name in float_parameter_list:
            settings[name] = float(settings[name])
        
        scale = {"Ms" : 1e-6, "Ks" : 1e-3, "s" : 1e0, "ms" : 1e3, "us" : 1e6, "ns" : 1e9, "ps" : 1e12, "fs" : 1e15}
        settings["time_scale"] = scale[settings["units"]]   

        # open files 
        settings["log_file"] = open(settings["log_file"], 'a')
    
        return settings

    def end_of_program(self, log_file):

        # close files
        log_file.close()

        return None
