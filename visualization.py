import matplotlib.pyplot as plt
from preporcessing import TimeSeries
from typing import List
from scipy.stats import shapiro
from scipy.stats import probplot


def plot(ts: TimeSeries):
    '''
    Plots one or more time series. The time axis is adjusted to display the data according to their time indices.
    Changed to just ts instead of ts_list as argument because of the operatorkeys.py file.

    ARGS:
        - ts_list: a list of one or more time series files to be plotted. The files will be of type str.

    SIDE EFFECTS:
        - produces a plot of one or more time series
    '''

    # Plot the ts data
    ts.data.plot()

    # Change the label of the x-axis and display the plot
    plt.xlabel("Date")
    plt.show()


def histogram(ts: TimeSeries):
    '''
    Computes the histogram of a given time series and then plots it. When it's plotted, the histogram is vertical
    and side to side with a plot of the time series.

    ARGS:
        - ts: a single time series file to run operations on. Should be a string containing a csv filename.

    SIDE EFFECTS:
        - produces a histogram based on ts
        - plots the ts
    '''
    # Create a subplot with 1 row and 2 columns (for formatting)
    fig, axes = plt.subplots(1, 2)

    # Create the histogram and plot, then display them side-by-side
    ts.data.hist(ax=axes[0])
    ts.data.plot(ax=axes[1])


def box_plot(ts: TimeSeries):
    '''
    Produces a Box and Whiskers plot of the given time series. Also prints the 5-number summary of the data.

    ARGS:
        - ts: a single time series file to run operations on. Should be a string containing a csv filename.

    SIDE EFFECTS:
        - prints the 5-number summary of the data; that is, it prints the minimum, maximum, first quartile, median,
        and third quartile
        - produces a Box and Whiskers plot of ts
    '''
    # Create and display the box plot
    ts.data.plot.box()
    plt.show()

    # Print the 5-number summary (plus a little extra)
    ts.data.describe()


def normality_test(ts: TimeSeries):
    '''
    Performs a hypothesis test about normality on the given time series data distribution using Scipy's
    Shapiro-Wilkinson. Additionally, this function creates a quantile plot of the data using qqplot from matplotlib.

    ARGS:
        - ts: a single time series file to run operations on. Should be a string containing a csv filename.

    SIDE EFFECTS:
        - produces a quantile plot of the data from ts
        - prints the results of the normality test by checking the p-value obtained by Shapiro-Wilkinson
    '''
    # Loop through each column in the dataframe
    for col in ts.data:
        # We want to run the shapiro test on the columns with numerical data
        if ts.data[col].dtype == 'float64':
            # Grab the column with the data we want
            results = ts.data[col]

    # Obtain the test statistics and the p-value using a Shapiro-Wilkinson test
    stats, p = shapiro(results)

    # Check to see if the data is normal or not
    if p > .05:
        print("Data is normal")
    else:
        print("Data is not normal")

    # Create and display the quantile plot
    probplot(results, plot=plt)
    plt.figure()


def mse(y_test: List, y_forecast: List) -> float:
    '''
    Computes the Mean Squared Error (MSE) error of two time series.

    RETURNS:
        - the MSE as a float

    ARGS:
        - y_test: the time series data being tested (represented as a list)
        - y_forecast: our forecasting model data (represented as a list)
    '''
    # Initialize a result variable
    
    result = 0

    # Calculate n
    n = len(y_forecast)
    # Loop through every data point in y_forecast and y_test
    for i in range(n):
        # Compute the difference between the actual data and our forecasting model
        diff = y_test[i] - y_forecast[i]
        # Square the difference and add it to result
        result += (diff ** 2)

    # Final multiplication step
    result *= (1 / n)
    if len(result) == 1:
        result = result[0]
    return result


def mape(y_test: List, y_forecast: List) -> float:
    '''
    Computes the Mean Absolute Percentage Error (MAPE) error of two time series.

    RETURNS:
        - the percentage error as a float

    ARGS:
        - y_test: the time series being tested
        - y_forecast: our forecasting model
    '''
    # Initialize a result variable
    result = 0

    # Calculate n
    n = len(y_forecast)

    # Loop through every data point in y_forecast and y_test
    for i in range(n):
        # Compute the difference between the actual data and our forecasting model
        diff = y_test[i] - y_forecast[i]
        # Calculate the difference divided by the test data
        inner = diff / y_test[i]
        # Take the absolute value of the difference divided by the test data and add it to the result
        result += abs(inner)

    # Final multiplication step
    result *= (1 / n)

    # Convert to percentage
    result *= 100

    return result


def smape(y_test: List, y_forecast: List) -> float:
    '''
    Computes the Symmetric Mean Absolute Percentage Error (SMAPE) error of two time series.

    RETURNS:
        - the percentage error as a float

    ARGS:
        - y_test: the time series being tested
        - y_forecast: our forecasting model
    '''
    # Initialize a result variable
    result = 0

    # Calculate n
    n = len(y_forecast)

    # Loop through every data point in y_forecast and y_test
    for i in range(n):
        # Compute the numerator of the SMAPE formula
        numerator = abs(y_test[i] - y_forecast[i])

        # Compute the absolute value of the test and forecast data for computational purposes
        test_data = abs(y_test[i])
        forecast_data = abs(y_forecast[i])

        # Compute the denominator of the SMAPE formula
        denominator = test_data + forecast_data

        # Add the inner part of the sum to the result
        result += (numerator / denominator)

    # Final multiplication step
    result *= (1 / n)

    # Convert to percentage
    result *= 100

    return result