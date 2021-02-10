'''
This module contains the dictionaries associated with operator inputs and outputs. It's used to help build branches
of the tree in tree.py.
Authors: Brian Gunnarson and Sam Peters
Group name: The Classy Coders
Most recent modification: 2/4/21
'''

# Import necessary components
import preprocessing
import modelingAndForecasting as mf
import visualization as vs

# Dictionary for the input keys
operator_input_keys = {
    # Inputs for preprocessing component
    preprocessing.TimeSeries: [],
    preprocessing.TimeSeries.read_from_file: ["timeseries_without_data"],
    preprocessing.TimeSeries.write_to_file: ["timeseries_data"],
    preprocessing.TimeSeries.assign_time: ["timeseries_data"],
    preprocessing.TimeSeries.clip: ["timeseries_data"],
    preprocessing.TimeSeries.denoise: ["timeseries_data"],
    preprocessing.TimeSeries.impute_missing: ["timeseries_data"],
    preprocessing.TimeSeries.difference: ["timeseries_data"],
    preprocessing.TimeSeries.impute_outliers: ["timeseries_data"],
    preprocessing.TimeSeries.longest_continuous_run: ["timeseries_data"],
    preprocessing.TimeSeries.scaling: ["timeseries_data"],
    preprocessing.TimeSeries.standardize: ["timeseries_data"],
    preprocessing.TimeSeries.logarithm: ["timeseries_data"],
    preprocessing.TimeSeries.cubic_root: ["timeseries_data"],
    preprocessing.TimeSeries.split_data: ["timeseries_data", "perc_training", "perc_valid", "perc_test"],
    preprocessing.TimeSeries.ts2db: ["timeseries_data"],

    # Inputs for modelingAndForecasting component
    mf.mlp_model: [],
    mf.rf_model: [],
    mf.fit: ["model", "x_train", "y_train"],
    mf.predict: ["trained_model", "x_test"],

    # Inputs for visualization component
    vs.plot: ["timeseries_data"],
    vs.histogram: ["timeseries_data"],
    vs.box_plot: ["timeseries_data"],
    vs.normality_test: ["timeseries_data"],
    vs.mse: ["y_test", "y_forecast"],
    vs.mape: ["y_test", "y_forecast"],
    vs.smape: ["y_test", "y_forecast"]
}

# Dictionary for the output keys
operator_output_keys = {
    # Outputs for the preprocessing component
    preprocessing.TimeSeries: ["timeseries_without_data"],
    preprocessing.TimeSeries.read_from_file: ["timeseries_data"],
    preprocessing.TimeSeries.write_to_file: [],
    preprocessing.TimeSeries.assign_time: [],
    preprocessing.TimeSeries.clip: ["timeseries_data"],
    preprocessing.TimeSeries.denoise: ["timeseries_data"],
    preprocessing.TimeSeries.impute_missing: [],
    preprocessing.TimeSeries.difference: [],
    preprocessing.TimeSeries.impute_outliers: [],
    preprocessing.TimeSeries.longest_continuous_run: ["timeseries_data"],
    preprocessing.TimeSeries.scaling: [],
    preprocessing.TimeSeries.standardize: ["timeseries_data"],
    preprocessing.TimeSeries.logarithm: ["timeseries_data"],
    preprocessing.TimeSeries.cubic_root: ["timeseries_data"],
    preprocessing.TimeSeries.split_data: [],
    preprocessing.TimeSeries.design_matrix: ["training_matrix", "test_matrix"],
    preprocessing.TimeSeries.ts2db: ["x_train", "y_train", "x_test", "y_test"],

    # Outputs for the modelingAndForecasting component
    mf.mlp_model: ["model"],
    mf.rf_model: ["model"],
    mf.fit: ["trained_model"],
    mf.predict: ["y_forecast"],

    # Outputs for the visualization component
    vs.plot: [],
    vs.histogram: [],
    vs.box_plot: [],
    vs.normality_test: [],
    vs.mse: ["error_val"],
    vs.mape: ["error_val"],
    vs.smape: ["error_val"]
}
