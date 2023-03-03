# kinetic monte carlo simulation

import random
import numpy as np

class KMC():

    def __init__(self, attempt_frequency, boltzmann_constant, temperature, vacancy_id, time_scale):

        self.attempt_frequency = attempt_frequency
        self.boltzmann_constant = boltzmann_constant      
        self.temperature = temperature
        self.vacancy_id = vacancy_id
        self.time_scale = time_scale

    def jumping_rates(self, diffsuion_barriers):

        return list(self.attempt_frequency * np.exp(- np.array(diffsuion_barriers) / (self.boltzmann_constant * self.temperature)))
        
    def cumulative_function(self, rates):
        
        return [0] + [np.sum(rates[:i]) for i in range(1, len(rates) + 1)]

    def select_event(self, cumulative_rates):
        
        sample_rate = random.uniform(0, 1) * cumulative_rates[-1]
        for index in range(len(cumulative_rates) - 1):
            if (sample_rate >= cumulative_rates[index]) and (sample_rate < cumulative_rates[index + 1]):
                return index

    def update_time(self, overall_rate):
        
        return - np.log(random.uniform(0, 1)) / overall_rate * self.time_scale

    def update_configuration(self, configurations, neighbor_id):
        
        vacancy_coordinates = configurations[self.vacancy_id - 1, 2:5].copy()

        configurations[self.vacancy_id - 1, 2 : 5] = configurations[neighbor_id - 1, 2:5].copy()
        configurations[neighbor_id - 1, 2 : 5] = vacancy_coordinates
        
        return configurations
        
    def execute_KMC(self, configurations, pair_information):
        
        ids, diffusion_barriers = pair_information
        
        rates = self.jumping_rates(diffusion_barriers)
        cumulative_rates = self.cumulative_function(rates)
        index = self.select_event(cumulative_rates)

        neighbor_id = int(ids[index])
        neighbor_info = list(configurations[neighbor_id - 1, :])

        '''
        neighbor_info = [neighbor_id, 
                         configuration[neighbor_id - 1, 1], 
                         configuration[neighbor_id - 1, 2], 
                         configuration[neighbor_id - 1, 3], 
                         configuration[neighbor_id - 1, 4]]
        '''

        jumping_time = self.update_time(cumulative_rates[-1])
        updated_configuration = self.update_configuration(configurations, neighbor_id)
        
        return neighbor_info, jumping_time, updated_configuration
