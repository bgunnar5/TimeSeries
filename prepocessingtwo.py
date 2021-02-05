import pandas as pd
import math
import csv
import matplotlib.pyplot as plt
from datetime import date
from datetime import datetime, date, timedelta
import re
import janitor  # need to install

class TimeSeries:

    def __init__(self):
        self.data = None  # holds data from initial csv read
        self.train = [] #
        self.val = []
        self.test = []

    def scaling(self):
        """
        Produces a time series whose magnitudes are scaled so that the resulting
        magnitudes range in the interval [0,1].
        """
        df = pd.DataFrame(self.data)    # self.data could be any data type
        df_sca = (df - df.min()) / (df.max() - df.min())
        print(df_sca)

    def standardize(self):
        """
        Produces a time series whose mean is 0 and variance is 1.
        """
        df = pd.DataFrame(self.data)
        df_stand = df   # (df - 0)/sqrt(1)
        print(df_stand)

    def logarithm(self):
        """
        Produces a time series whose elements are the logarithm of the original
        elements.
        """
        df = pd.DataFrame(self.data)
        df_log = math.log(df)
        print(df_log)

    def cubic_root(self):
        """
        Produces a time series whose elements are the original elements’ cubic root.
        """
        df = pd.DataFrame(self.data)
        df_cu = df**( 1.0 / 3.0)
        print(df_cu)

    def split_data(self, perc_training =.8, perc_valid =.01, perc_test =.1,):
        """
        Splits a time series into training, validation, and testing according to the given percentages.
        """
        perc_valid += perc_training
        perc_test += perc_valid
        df = pd.DataFrame(self.data)
        array = df.values.tolist()
        timeList = []
        varList = []
        for index in array:
            timeList.append(index[0])
            varList.append(index[1])
        self.train = varList[0:int(len(array)*perc_training)-1]
        self.val = varList[int(len(array)*perc_training):int(len(array)*perc_valid)-1]
        self.test = varList[int(len(array)*perc_valid):int(len(array)*perc_test)-1]

    def design_matrix(self, input_index=0, output_index=25):
        trainingData = self.train
        X_train = ()
        y_train = ()
        trainingMatrix = []
        for i in range(len(trainingData)):
            j = 0
            while j < output_index:
                X_train.append(trainingData[i+j])
                j+=1
            y_train.append(trainingData[i+j])
            matrix.append([X_train,y_train])

        testData = self.test
        X_test = ()
        y_test = ()
        testMatrix = []
        for i in range(len(testData)):
            j = 0
            while j < output_index:
                X_train.append(trainingData[i+j])
                j+=1
            y_train.append(testData[i+j])
            matrix.append([X_test,y_test])
            
        return trainingMatrix, testMatrix
    
    
    def ts2db(input_filename, perc_training, perc_valid, perc_test, input_index,
              output_index, output_file_name):
        """read the file
            split data
            produce a new database"""
        read_from_file(input_filename)
        split_data(perc_training, perc_valid, perc_test)
        df = pd.DataFrame(self.train)
        df.to_csv(output_file_name)
