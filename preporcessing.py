"""
File that holds all the preprocessing methods
"""

import pandas as pd
import matplotlib.pyplot as plt
from datetime import date
from datetime import datetime, date, timedelta
import re
import janitor  # need to install


class TimeSeries:

    def __init__(self):
        self.data = None  # holds data from initial csv read
        self.clipped = None  # holds data from a clipped interval
        self.temp = None  # for impute missing
        self.dif = None   # for calculating difference

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
        self.clipped = self.data.filter_date(first_date, starting_date, final_date)
        print(self.clipped.head())

    def denoise(self):
        """
        Denoise a time series. Should be able to accomplish 
        this by calling cubic_root
        """

        pass

    def impute_missing(self):
        """
        Compute missing values such as NaN's
        https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.fillna.html
        Fills data to the right to NaNs
        """

        self.temp = self.data.fillna(method='ffill')
        self.data = self.temp

    def difference(self):
        """
        Calculate the difference between data rows
        """

        self.dif = self.data.copy()
