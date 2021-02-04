from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
# from Yifeng's file import split_data, design_matrix

def mlp_model(input_dimension=25, output_dimenstion=25, layers=5):
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
    network = [input_dimension] * (layers - 2)
    return MLPClassifier(hidden_layer_sizes=network)


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
    return RandomForestClassifier()

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
    model.fit(x_train, y_train)
    return model

def predict(model, x_train, y_train):
    '''
    Wrapper function for predict methods of RandomForestClassifier and MLPClassifier objects

    Parameters
    ----------
        - model: RandomForestClassifier or MLPClassifier object
        - x_test: TODO

    Returns
    -------
        - TODO
    '''
    return model.predict(x_test)
    

# TODO: modify to fit Yifeng's functional form
X, y = make_classification(n_samples=100, random_state=1)
X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                    random_state=1)


### EXAMPLE: ###

# Classify the models:
mlp = mlp_model()
rf = rf_model()

# Create a fit using builtin method
mlp.fit(X_train, y_train)
rf.fit(X_train, y_train)

# Forecast using builtin method
mlp_prediction = mlp.predict(X_test)
rf_prediction = rf.predict(X_test)

print(mlp_prediction)
print(rf_prediction)
