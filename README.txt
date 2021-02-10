TIME SERIES ANALYSIS SUPPORT

DESCRIPTION
This time series analysis support project supplies the user with an all-inclusive library that gives the ability to create a transformation tree and execution pipeline. These object-oriented data structures allow the user to create and modify the tree, and also to create pipelines that successively execute different processes regarding time series files. These processes include various preprocessing methods (such as file I/O, data massaging involving pandas DataFrame creation/manipulation, and more), modeling and forecasting, statistics, and visualization. As an overall job, the user would typically begin by reading in a time series data file and would then proceed to call zero or more data-massaging methods. This modified time series would then be passed into a time series-to-database method that parses the data into training, testing, and validation sets. These sets are used to pass into the models as arguments, which are then trained and used to forecast new data. This forecasted data can be compared to the test data through various statistical tests and then visualized graphically. Data scientists can then use this transformation tree design to run different pipelines and see which forecasting model works best.

AUTHORS
Tyler Christenson
Yifeng Cui
Brian Gunnarson
Sam Peters
Jacob Rammer

FILE CREATION DATE
These are the creation dates for files as they were pushed to GitHub:
preprocessing.py: January 20, 2021
tree.py: January 27, 2021
visualization.py: January 29, 2021
modelingAndForecasting.py: February 2, 2021
operatorkeys.py: February 3, 2021

COURSE NAME AND ASSIGNMENT
Course: CIS 422 - Software Methodologies I
Assignment: Project 1 - Time Series Analysis

STEPS TO COMPILE AND RUN
If you want to run this system using a virtual environment you can use the following steps at the command line:
Go to the project directory
Run the command: “python -m vena proj-1-env”
Depending on the system:
On Unix/macOS run: “source proj-1-env/bin/activate”
On Windows run: “proj-1-env\Scripts\activate.bat”
Finally, run: "pip install -r requirements.txt”

If you don’t care about using a virtual environment you can just install the packages for the program using: "pip install -r requirements.txt”

After installing all the requirements and (potentially) creating a virtual environment, all that’s left to do is to import “ts_analysis_support.py” at the top of your file. This file includes all of the components that build up this project (tree.py, preprocessing.py, operatorkeys.py, modelingAndForecasting.py, and visualization.py).

For Example Usage See demo.py

SOFTWARE DEPENDENCIES
See requirements.txt

DIRECTORY STRUCTURE
Top Level: source code files (preprocessing.py, modelingAndForecasting.py, visualization.py, tree.py, operatorkeys.py, and ts_analysis_support.py), README.txt, requirements.txt, demo.py, docs, data

Data Directory: contains “Time Series Data” and “Time Series Data 2” subdirectories that contain csv files of time series data

Docs Directory: SRS.pdf, SDS.pdf, Project_Plan.pdf, Programming_Documentation.pdf, Installation_Instructions.pdf, and User_Documentation.pdf