import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, date, timedelta
from preporcessing import *
import re


def read_from_file(file_name: str):
    """
    Read from a CSV file, the project description
    says the CSV files are ordered in (time, magnitude)
    :param file_name: name of the csv file to open
    :return: list of all data point
    """

    try:
        csv_file = pd.read_csv(file_name)
        return csv_file
    except FileNotFoundError:
        print(f"File {file_name} not found.")


def write_to_file(data, file_name: str):
    """
    Write data to a CSV file
    :param data: data to write to CSV file
    :param file_name: name of the output file
    :return: void
    """

    data.to_csv(file_name, sep='\n', index=False)


def main():

    while(1):
        print("Enter file location")
        file_location = input()
        ts = TimeSeries()
        ts.read_from_file(file_location)
        print(ts.data)

        print("Available commands for Time Series:")
        print("A: assign time. Adds missing time data to a time series\n",
            "W: write time series data to csv file.\n",
            "P: print data frame\n""Enter a command")
        command = input().upper()
        if command == "A":  # assign time
            print("Enter the starting time in the format mm/dd/yyyy hr:mm")
            time = input()
            print("Enter the time increment in hours")
            increment = input()
            ts.assign_time(time, increment)
        elif command == "P":  # print data frame
            print(ts.data)
        



main()
