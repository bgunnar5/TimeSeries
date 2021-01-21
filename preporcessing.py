"""
File that holds all the preprocessing methods
"""

import pandas as pd
import matplotlib.pyplot as plt

class TimeSeries:

    def __init__(self):
        self.data = None

    def read_from_file(self, file_name: str):
        """
        Read from a CSV file, the project description
        says the CSV files are ordered in (time, magnitude)
        but they're not?? So whatever, we're off to a great start.
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
