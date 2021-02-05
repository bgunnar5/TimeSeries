"""
File that holds all the preprocessing methods
"""

import pandas as pd
import csv
import matplotlib.pyplot as plt
from datetime import date
from datetime import datetime, date, timedelta
import numpy as np
import re
import janitor  # need to install


class TimeSeries:

    def __init__(self, df=None):
        self.data = None  # holds data from initial csv read
        if type(df) == pd.core.frame.DataFrame:
            self.data = df
        # self.clipped = None  # holds data from a clipped interval
        # self.temp = None  # for impute missing
        # self.dif = None   # for calculating difference

    def read_from_file(self, file_name: str):
        """
        Read from a CSV file, the project description
        says the CSV files are ordered in (time, magnitude)
        Index by time
        :param file_name: name of the csv file to open
        :return: void
        """

        try:
            self.data = pd.read_csv(file_name)
        except FileNotFoundError:
            print(f"File {file_name} not found.")

    def write_to_file(self, file_name: str):
        """
        Write data to a CSV file
        :param data: data to write to CSV file
        :param file_name: name of the output file
        :return: void
        """

        self.data.to_csv(file_name)

    def assign_time(self, start: datetime, increment: int):
        """
         If a csv file does not include a date section, this method adds it. 
        Accomplished by iterating over all rows and adding the date
        Expected input: 01/23/2021 12:30 (mm/dd/yyyy hh:mm)
        Use regex to extract date information to create a datetime object
        for easy time manipulation
        :param start: The starting date of the time series
        :type start: datetime
        :param increment: the time interval
        :type increment: int
        """

        month_reg = r"^([0-9]{2})"  # matches the month
        day_reg = r"\/([0-9]{2})\/"  # matches the day
        year_reg = r"\/([0-9]{4})"  # matches the year
        hour_reg = r"( [0-9]{2}):"  # matches the hour
        minute_reg = r":([0-9]{2})"  # matches the minute
        month = re.search(month_reg, start)  # extracted month
        day = re.search(day_reg, start)  # extracted day
        year = re.search(year_reg, start)  # extracted year
        hour = re.search(hour_reg, start)  # extracted hour
        minute = (re.search(minute_reg, start))  # extracted minute

        # datetime object for easy time manipulation over an interval
        date = datetime(year=int(year.group(1)), month=int(month.group(1)),
                        day=int(day.group(1)), hour=int(hour.group(1)),
                        minute=int(minute.group(1)))

        # create the missing columns in the dataframe
        # self.data['DATE (MM/DD/YYYY)'] = None
        # self.data['MST'] = None
        self.data.insert(0, "Date", None)
        self.data.insert(1, "Time", None)

        """
        Assign each row data in the missing time and date columns.
        Increment time time by increment. .date() and .time()
        pull exactly what it sounds like
        """
        for i in range(len(self.data)):
            self.data.at[i, self.data.columns[0]] = date.date()
            self.data.at[i, self.data.columns[1]] = date.time()
            date += timedelta(hours=int(increment))

        print(self.data)

    def clip(self, starting_date,  final_date):
        """
        Clip a time series from a specific date
        :param starting_date: date str in the form of mm/dd/yyyy
        :type starting_date: str
        :param final_date: ending date in the form of mm/dd/yyyy
        :type final_date: str
        """

        first_date = self.data.columns[0]  # copy the date header from csv
        clipped = self.data.filter_date(first_date, starting_date, final_date)
        print(clipped.head())
        return TimeSeries(clipped)

    def denoise(self):
        """
        Denoise a time series. Should be able to accomplish
        this by calling cubic_root
        """

        self.impute_missing()
        self.impute_outliers()

        return TimeSeries(self.data)

    def impute_missing(self):
        """
        Compute missing values such as NaN's
        https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.fillna.html
        Fills data to the right to NaNs
        """

        temp = self.data.fillna(method='bfill')
        self.data = temp

    def difference(self):
        """
        Calculate the difference between data rows
        """

        data_index = len(self.data.columns) - 1
        temp = self.data.copy()
        temp[temp.columns[data_index]] = \
            self.data[self.data.columns[data_index]] - \
            self.data[self.data.columns[data_index]].shift(-1)
        print(temp)
        return TimeSeries(temp)

    def impute_outliers(self):
        """
        Find and remove outlies from dataframe
        Referenced: https://stackoverflow.com/questions/23199796/
        detect-and-exclude-outliers-in-pandas-data-frame
        """

        temp = self.data.copy()


        data_index = len(self.data.columns) - 1

        q_low = self.data[self.data.columns[data_index]].quantile(.01)
        q_high = self.data[self.data.columns[data_index]].quantile(.99)
        self.data = self.data[(self.data[temp.columns[data_index]] < q_high) &
                        (self.data[temp.columns[data_index]] > q_low)]
        print(self.data)

    def longest_continuous_run(self):
        """
        This method finds the longest continuous run in a dataframe.
        A continuous run can be defined as rows that don't have
        any missing information (NaNs).
        df = dataframe
        :return: longest continuous run dataframe
        """

        temp = self.data.isna()  # find NaNs in df
        runs = []   # holds index of NaNs
        data_index = len(self.data.columns) - 1
        for i in range(len(temp)):
            if temp.at[i, temp.columns[data_index]] == True:
                runs.append(i + 1)

        runs.append(len(temp) + 1)  # end of file

        ret = self.data.iloc[0:0]  # blank df
        for i in range(len(runs) - 1):
            first = runs[i]
            last = runs[i + 1]
            temp = self.data.iloc[first : last - 1]
            if len(temp) > len(ret):
                '''
                This compares the length of the previous
                longest run represented by a dataframe
                '''
                ret = temp
        print(ret)

        return TimeSeries(ret)

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
        # Create a copy of the current DataFrame
        new_df = self.data.copy()

        # Loop through the columns in the DataFrame
        for col in new_df:
            # If the column contains floats or integers we can take the logarithm and store it
            if new_df[col].dtype == 'float64' or new_df[col].dtype == 'int64':
                new_df[col] = np.log10(new_df[col])

        # Return our new DataFrame
        return TimeSeries(new_df)

    def cubic_root(self):
        """
        Produces a time series whose elements are the original elements’ cubic root.
        """
        # Create a copy of the current DataFrame
        new_df = self.data.copy()

        # Loop through the columns in the DataFrame
        for col in new_df:
            # If the column contains floats or integers we can take the cubic root and store it
            if new_df[col].dtype == 'float64' or new_df[col].dtype == 'int64':
                new_df[col] = new_df[col] ** (1 / 3)

        # Return our new DataFrame
        return TimeSeries(new_df)

    def split_data(self, perc_training=.8, perc_valid=.01, perc_test=.19, ):
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
        self.train = varList[0:int(len(array) * perc_training) - 1]
        self.val = varList[int(len(array) * perc_training):int(len(array) * perc_valid) - 1]
        self.test = varList[int(len(array) * perc_valid):int(len(array) * perc_test) - 1]

    def design_matrix(self, input_index=0, output_index=25):
        trainingData = self.train
        trainingMatrix = []
        for i in range(len(trainingData)):
            j = 0
            X_train = []
            y_train = []
            if trainingData[i] == trainingData[-1]:
                break
            while j < output_index:
                X_train.append(trainingData[i+j])
                j+=1
            y_train.append(trainingData[i+j])
            trainingMatrix.append([X_train,y_train])

        testData = self.test
        testMatrix = []
        for i in range(len(testData)):
            j = 0
            X_test = []
            y_test = []
            if testData[i] == testData[-1]:
                break
            while j < output_index:
                X_test.append(testData[i+j])
                j+=1
            y_test.append(testData[i+j])
            testMatrix.append([X_test,y_test])

    def ts2db(self, input_file_name, perc_training, perc_valid, perc_test, input_index,
              output_index, output_file_name):
        """read the file
            split data
            produce a new database"""
        if input_file_name:
            self.read_from_file(input_file_name)

        self.split_data(perc_training, perc_valid, perc_test)
        trainingMatrix, testMatrix = self.design_matrix()

        x_train, y_train = zip(*trainingMatrix)
        x_test, y_test = zip(*testMatrix)

        return x_train, y_train, x_test, y_test
