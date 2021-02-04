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

    def split_data(self, perc_training, perc_valid, perc_test, file_name: str):
        """
        Splits a time series into training, validation, and testing according to the given percentages.
        """
        results = []
        perone = perc_training
        pertwo = perc_training + perc_valid
        perthree = perc_training + perc_test + perc_valid
        with open(file_name) as csvfile:
            array = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC)  # change contents to floats
            for row in array:  # each row is a list
                results.append(row)
        self.train = results(0:len(results)*perone-1)
        self.val = results(len(results)*perc_training-1:len(results)*pertwo-1)
        self.test = results(len(results)*pertwo:len(results)*perthree)
