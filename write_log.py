# write log file  
import time

def write_log(log_file, parameters):

    # step, step_time, vacancy_id, vacancy_type, vacany_x, vacancy_y, vacancy_z, neighbor_id, neighbor_type, neighbor_x, neighbor_y, neighbor_z
    
    # time_1 =  time.time()
    log_file.write("%d\t%f\t%d\t%d\t%f\t%f\t%f\t%d\t%d\t%f\t%f\t%f\n" % tuple(parameters))    
    # time_2 = time.time()
    
    # print(time_2 - time_1)

    return None
