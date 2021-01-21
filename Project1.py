import pandas as pd
import matplotlib.pyplot as plt
from preporcessing import *


def read_from_file(file_name: str):
    """
    Read from a CSV file, the project description
    says the CSV files are ordered in (time, magnitude)
    but they're not?? So whatever, we're off to a great start
    TODO change this docstring lol
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
    Project specification says file_name is the only parameter?
    Is data supposed to be a global variable?
    TODO figure that out
    Write data to a CSV file
    :param data: data to write to CSV file
    :param file_name: name of the output file
    :return: void
    """

    data.to_csv(file_name, sep='\n', index=False)


def main():

    # bs = read_from_file("Project Description/Time Series Data 2/AtmPres2005NovMin.csv")
    # write_to_file(bs, "hi.csv")
    # print(bs['DATE (MM/DD/YYYY)'])

    test = TimeSeries()
    test.read_from_file("Project Description/Time Series Data 2/example.csv")
    print(test.data.head())
    test.write_to_file("new_csv.csv")

main()
