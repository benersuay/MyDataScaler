MyDataScaler
=============

A Python module that can scale data for preprocessing. The module can save / load the scaling parameters into / from a txt file, which makes it convenient to scale training and test data on different runs.

To see the module in action run

    python demo.py

## Usage ##

Import the class

    from MyDataScaler import *

Get an instance

    scaler = MyDataScaler()

Get an instance with min - max data range (default [0,1]):
    
    scaler = MyDataScaler(-1,1)

Load data from a pickled (binary) file:

    scaler.load_pickle("filename")

The call above assumes that your pickled file format is .p

Load data from a CSV file:

    scaler.load_csv("filename")

The call above assumes that your csv file format is .csv (duh).

Scale your training data (fits, and transforms):

    scaler.scale()

By default, the method assumes that the first column has labels for the samples. If you want to scale your training data including the first column:

    scaler.scale(True)

You can save your scaling parameters for future reference:

    scaler.save_params("params_filename")

The call above saves scaling parameters to params_filename.txt file.

In another script you can load the scaler parameters with:

   scaler.load_params("params_filename")

After you are done scaling your data, you can save the data either in CSV format (.csv) or libsvm format (.txt):

    scaler.save_csv("my_scaled_data")

    scaler.save_libsvm("my_scaled_data")

In addition, if you want to pickle the scaled data (.p):

    scaler.save_pickle("my_pickled_scaled_data")