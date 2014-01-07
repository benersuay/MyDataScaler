#!/usr/bin/env python
#
# Bener Suay
# December 2013
# benersuay@wpi.edu
#
# This script demonstrates the usage of MyDataScaler class.
# The script is split into two function calls to show the possibility
# of calling the scaler in two sessions: training and testing. 
# 
# The two function calls could be made in two separate files, and 
# scaling would work the same way.
#
# The intended usage of this class is to load a previously saved experiment data,
# apply scaling for preprocessing (e.g. for machine learning), and save the data
# in different formats. Keeping the scaler parameters in a file makes possible to 
# apply the same transform to your test data in the future when you need to.
#
# MyDataScaler depends on the following modules:
#
# 1) MyLibsvmLogger, and,
# 2) MyCSVLogger
# 

from MyDataScaler import *
import numpy as np

def generate_my_training_data():
    return np.array([[1.0, -10.0, 20.0], [2.0, 0.0, 0.0], [-1.0, 10.0, -10.0]])

def generate_my_test_data():
    return np.array([[0.0, 7.0, -5.0], [1.0, -2.4, -3.5]])

def process_my_training_data(data):
    # scale data
    s = MyDataScaler(0,1)
    s.data = data

    # do not scale the first column:
    # assume the first column has our data label
    s.scale(False)

    # save scaled training data in libsvm format
    s.save_libsvm("scaled_training_data")

    # save scaled training data in csv format
    s.save_csv("scaled_training_data")
    
    # save scaling parameters    
    s.save_params("scaling_params")

def process_my_test_data(data):
    # load scaling parameters
    s = MyDataScaler()
    s.load_params("scaling_params")
    s.data = data

    # scale data, do not scale the first column
    # assume the first column has our data label
    s.scale(False)

    # save scaled test data in libsvm format
    s.save_libsvm("scaled_test_data")
    
    # save scaled training data in csv format
    s.save_csv("scaled_test_data")

if __name__ == "__main__":
    
    # Part 1: Training
    trainingData = generate_my_training_data()
    process_my_training_data(trainingData)
    
    # Part 2: Testing
    testData = generate_my_test_data()
    process_my_test_data(testData)
