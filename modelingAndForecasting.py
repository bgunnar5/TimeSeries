from sklearn.neural_network import MLPRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from preporcessing import TimeSeries
import numpy as np

def mlp_model():
    '''
    Wrapper function for multilayer perceptron model.

    Parameters
    ----------
        - input_dimension: Dimension (number of neurons) in first layer. Comes from input vector of design_matrix function.
                           Default 25.
        - output_dimension: Dimension out of first layer, becomes new input_dimension for second layer, etc?
                            Default 25?
        - [layers]: (optional) Number of layers in the neural network.

    Returns
    -------
        - MLPClassifier object (uses same defaults as sklearn, but hidden_layer_sizes specified from
                                input and output dimensions)
    '''
    #network = [input_dimension] * (layers - 2)
    # MLPRegressor(hidden_layer_sizes=network)
    return MLPRegressor()


def rf_model():
    '''
    Wrapper function for random forest model.

    Parameters
    ----------
        - None

    Returns
    -------
        - RandomForestClassifier object (uses same defaults as sklearn)
    '''
    return RandomForestRegressor()

def fit(model, x_train, y_train):
    '''
    Wrapper function for fit methods of RandomForestClassifier and MLPClassifier objects

    Parameters
    ----------
        - model: RandomForestClassifier or MLPClassifier object
        - x_train: TODO
        - y_train: TODO

    Returns
    -------
        - RandomForestClassifier object (uses same defaults as sklearn)
    '''
    y_train_array = np.ravel(y_train)
    model.fit(x_train, y_train_array)
    return model

def predict(model, X):
    '''
    Wrapper function for predict methods of RandomForestClassifier and MLPClassifier objects

    Parameters
    ----------
        - model: RandomForestClassifier or MLPClassifier object
        - X: State of data beginning at input_index from design_matrix

    Returns
    -------
        - model.predict(X): List of predicted data values
    '''
    predictions = model.predict(X)
    return predictions
"""
ts = TimeSeries()
filename = 'Project Description/Time Series Data 2/wind_cointzio_10m_complete.csv'
input_index, output_index, X_train, y_train, X_test, y_test = ts.ts2db(filename, .8, .01, .19, 0, 25, None)


# TODO: modify to fit Yifeng's functional form
# X, y = make_classification(n_samples=100, random_state=1)
# input_index, output_index, X_train, X_test, y_train, y_test = train_test_split(X, y,
#                                                     random_state=1)

### EXAMPLE: ###
mlpDimension = output_index - input_index

# Classify the models:
mlp = mlp_model(mlpDimension, mlpDimension)
rf = rf_model()

# Create a fit using builtin method
fit(mlp, X_train, y_train)
fit(rf, X_train, y_train)

# Forecast using builtin method
mlp_prediction = predict(mlp, X_test)
rf_prediction = predict(mlp, X_test)

print(mlp_prediction)
print(rf_prediction)
"""
