'''
This file contains functions to wrap sklearn regression models as well as their 'fit' and 'predict' methods.

Authors: Tyler Christenson & Sam Peters
'''

from sklearn.neural_network import MLPRegressor
from sklearn.ensemble import RandomForestRegressor
from preprocessing import TimeSeries
import numpy as np

def mlp_model(input_dimension=100, output_dimension=1, layers=10):
    '''
    Wrapper function for multilayer perceptron model.

    Parameters
    ----------
        - input_dimension: Dimension (number of neurons) in first layer. Comes from input_index of ts2db function.
                           Default 100.
        - output_dimension: Dimension out of output layer. Describes how many output elements the model calculates at a time.
                            Default 1.
        - [layers]: (optional) Number of layers in the neural network. Default 10.

    Returns
    -------
        - MLPRegressor object (uses same defaults as sklearn, but hidden_layer_sizes specified from
                                input and output dimensions)
    '''
    network = [input_dimension] * (layers - 2)
    return (MLPRegressor(hidden_layer_sizes=network))


def rf_model():
    '''
    Wrapper function for random forest model.

    Parameters
    ----------
        - None

    Returns
    -------
        - RandomForestRegressor object (uses same defaults as sklearn)
    '''
    return RandomForestRegressor()

def fit(model, x_train, y_train):
    '''
    Wrapper function for fit methods of RandomForestRegressor and MLPRegressor objects

    Parameters
    ----------
        - model: RandomForestRegressor or MLPRegressor object
        - x_train: training input data, derived from ts2db
        - y_train: training output data, derived from ts2db

    Returns
    -------
        - Trained model object
    '''
    y_train_array = np.ravel(y_train)
    model.fit(x_train, y_train_array)
    return model

def predict(model, X):
    '''
    Wrapper function for predict methods of RandomForestRegression and MLPRegressor objects

    Parameters
    ----------
        - model: RandomForestRegressor or MLPRegressor object
        - X: State of data beginning at input_index, input test data typically passed in (from ts2db)

    Returns
    -------
        - predictions: List of predicted data values from .predict() method in sklearn.
    '''
    predictions = model.predict(X)
    return predictions
