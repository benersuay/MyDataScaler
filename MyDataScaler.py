#!/usr/bin/env python

# Bener Suay
# December 2013
# benersuay@wpi.edu

# A simple python module that scales, saves, loads input data.
# The module loads / save the data from / to  a pickled array, and or
# a CSV file.
#
# Important Note: 
# This module depends on MyCSVLogger and MyLibsvmLogger modules.
#

from sklearn import preprocessing
import numpy as np
from copy import deepcopy
import pickle
from MyCSVLogger import *
from MyLibsvmLogger import *

class MyDataScaler():

    def __init__(self, miR=0, maR=1):
        self.minRange = miR
        self.maxRange = maR
        self.scaler =  preprocessing.MinMaxScaler(feature_range=(self.minRange, self.maxRange))

    def load_pickle(self,fname):
        # remove old data just in case
        self.data = []
        # load new data, handle if any errors occur
        try:
            self.data = np.array(pickle.load(open(fname+".p","rb")))
            print "Loaded pickle: "+fname+".p"
        except Exception, err:
            print "Error loading pickle file: "+fname+".p"
            print err

    def save_pickle(self, fname):
        # save data, handle if any errors occur
        try:
            pickle.dump(self.scaledData, open(fname+".p","wb"))
            print "Saved pickle: "+fname+".p"
        except Exception, err:
            print "Error saving pickle file: "+fname+".p"
            print err
            
    def load_csv(self, fname):
        # try to load the csv file
        # handle errors
        try:
            self.data = np.genfromtxt(fname+".csv", delimiter=',')
            print "Loaded data from: "+fname+".csv"
        except Exception, err:
            print "Error loading csv file: "+fname+".csv"
            print err

    def save_csv(self, fname):
        # save data, handle if any errors occur
        try:
            myCSV = MyCSVLogger('',fname)
            myCSV.open('w')
            for thisEntry in self.mergedData:
                myCSV.save(thisEntry)
            myCSV.close()
            print "Saved csv file: "+fname+".csv"
        except Exception, err:
            print "Error saving CSV file: "+fname+".csv"
            print err

    def save_libsvm(self, fname=None):
        libsvmLog = MyLibsvmLogger(fname)

        for thisEntry in self.mergedData:
            libsvmLog.append(thisEntry)

        libsvmLog.save_and_close()

    def scale(self,sfc = False):
        self.scaleFirstCol = sfc
        # Sometimes the first column is the label of the sample,
        # if we don't want to scale it, pass in False
        cols = range(int(not self.scaleFirstCol),self.data.shape[1])
        self.scaledData = self.scaler.fit_transform(self.data[:,cols])
        # the first column will be missing if we did not scale it
        if(not sfc):
            self.mergedData = self.merge(self.data, self.scaledData)
        else:
            # if we scaled the first column, we already have it in scaledData
            self.mergedData = deepcopy(self.scaledData)

    def save_params(self, fname):
        # open a txt file and save these values
        # handle errors
        try:
            myFile = open(fname+".txt", 'w')
            myFile.write(self.arr_to_line(self.scaler.min_))
            myFile.write(self.arr_to_line(self.scaler.scale_))
            myFile.write(str(self.minRange)+'\n')
            myFile.write(str(self.maxRange)+'\n')
            myFile.close()
        except Exception, err:
            print "Error saving parameters to: "+fname+".txt"
            print err
            

    def load_params(self, fname):
        # open a txt file and read these values myMin, myScale
        # handle errors
        try:
            myFile = open(fname+".txt", 'r')
            myMin = np.fromstring(myFile.readline().strip('\n'), dtype=float, sep=',')
            myScale = np.fromstring(myFile.readline().strip('\n'), dtype=float, sep=',')
            myMir = float(myFile.readline().strip('\n'))
            myMar = float(myFile.readline().strip('\n'))
            myFile.close()
            self.scaler.min_ = myMin
            self.scaler.scale_ = myScale
            self.minRange = myMir
            self.maxRange = myMar

            print "scaler.min_"
            print self.scaler.min_

            print "scaler.scale_"
            print self.scaler.scale_

            print "scaler min range:"
            print self.minRange

            print "scaler max range:"
            print self.maxRange
        except Exception, err:
            print "Error loading parameters from file: "+fname+".txt"
            print err

    def arr_to_line(self, arr):
        myLine = ""
        for e in arr[:-1]:
            myLine += str(e)+','
        myLine += str(arr[-1])+'\n'
        return myLine

    def merge(self, original, scaled):
        r, c = scaled.shape
        mergedArr = np.empty(shape=(r,c+1))
        for row, scaledEntry in enumerate(scaled):
            mergedArr[row] = np.append(original[row,0],scaledEntry)
        return mergedArr



