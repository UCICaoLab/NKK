# predicting diffusion barriers from machine learning model

import numpy as np

def linear_combination(data, parameters):

    weights, biases = parameters
    data = np.dot(data, weights) + biases
    
    # print(data.shape, weights.shape)
    return data

def batchnormalization(data, parameters):

    gamma, beta, mean, variance = parameters
    data = (data - mean)  / (variance + 0.001) ** 0.5 
    data = gamma * data + beta  

    return data

def relu(x):
    
    x[np.where(x < 0)] = 0
 
    return x

def predict(model_weights, input_data):
        
    # decode layer weights, each layer include weights, bias, gamma, beta, mean, variance
    number_of_layers = len(model_weights) // 6
    # print("number of layers", number_of_layers) 
    # reshape input 
    # input_data = image.reshape(1, -1)
    
    # hidden layers 
    for index in range(number_of_layers):
        # print(model_weights[index * 6 + 0].shape)
        # print(model_weights[index * 6 + 1].shape)
        linear_combination_output = linear_combination(input_data, (model_weights[index * 6 + 0], model_weights[index * 6 + 1]))
        batchnormalization_output = batchnormalization(linear_combination_output, (model_weights[index * 6 + 2], model_weights[index * 6 + 3], model_weights[index * 6 + 4], model_weights[index * 6 + 5])) 
        input_data = relu(batchnormalization_output)
    
    # output layer        
    linear_combination_output = linear_combination(input_data, (model_weights[number_of_layers * 6 + 0], model_weights[number_of_layers * 6 + 1]))
    
    return np.squeeze(linear_combination_output)[()]
