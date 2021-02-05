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

    def split_data(self, perc_training =.8, perc_valid =.1, perc_test =.1,):
        """
        Splits a time series into training, validation, and testing according to the given percentages.
        """
        results = []
        perone = perc_training
        pertwo = perc_training + perc_valid
        perthree = perc_test + perc_training + perc_valid
        df = pd.DataFrame(self.data)
        array = df.values.tolist()
        for row in array:  # each row is a list
            results.append(row)
        self.train = results[0:int(len(results)*perone)-1]
        self.val = results[int(len(results)*perone):int(len(results)*pertwo)-1]
        self.test = results[int(len(results)*pertwo):int(len(results)*perthree)-1]

    def design_matrix(self, input_index, output_index):
        df = pd.DataFrame(self.data)
        newData = df.select_dtypes(include=['number']).values.to_list()
        row = len(newData)-(output_index+1)
        col = output_index - input_index
        matrix = []
        for i in range(row):
            a = []
            for j in range(col):
                a.append(newData(i+input_index))
            matrix.append(a)
        return matrix
    
    
    def ts2db(input_filename, perc_training, perc_valid, perc_test, input_index,
              output_index, output_file_name):
        """read the file
            split data
            produce a new database"""
        read_from_file(input_filename)
        split_data(perc_training, perc_valid, perc_test)
        df = pd.DataFrame(self.train)
        df.to_csv(output_file_name)
