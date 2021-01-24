"""
File that holds all the preprocessing methods
"""

import pandas as pd
import matplotlib.pyplot as plt
from datetime import date
from datetime import datetime, date, timedelta
import re

class TimeSeries:

    def __init__(self):
        self.data = None

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
        day=int(day.group(1)), hour=int(hour.group(1)), minute=int(minute.group(1)))
        
        # create the missing columns in the dataframe
        self.data['DATE (MM/DD/YYYY)'] = None
        self.data['MST'] = None

        """
        Assign each row data in the missing time and date columns.
        Increment time time by increment. .date() and .time()
        pull exactly what it sounds like
        """
        for i in range(len(self.data)):
            self.data['DATE (MM/DD/YYYY)'][i] = date.date()
            self.data['MST'][i] = date.time()
            date += timedelta(hours=int(increment))

        print(self.data)
