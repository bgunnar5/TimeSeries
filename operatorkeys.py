import preporcessing as preprocessing
import modelingAndForecasting as mf

operator_input_keys = {
    preprocessing.TimeSeries: [],
    preprocessing.TimeSeries.read_from_file: ["timeseries_data"],
    preprocessing.TimeSeries.write_to_file: ["timeseries_data"],
    preprocessing.TimeSeries.assign_time: ["timeseries_data"],
    preprocessing.TimeSeries.clip: ["timeseries_data"],
    preprocessing.TimeSeries.assign_time: ["timeseries_data"],
    preprocessing.TimeSeries.denoise: [],
    preprocessing.TimeSeries.impute_missing: [],
    preprocessing.TimeSeries.difference: [],

    mf.train_test_split: [] #TODO
    mf.mlp_model: [], # TODO
    mf.rf_model: [], # TODO
    mf.fit: ["model", "x_train", "y_train"]
    mf.predict: ["trained_model", "x_test"]
}

operator_output_keys = {
    preprocessing.TimeSeries: ["timeseries_withou_data"],
    preprocessing.TimeSeries.read_from_file: ["timeseries_data"],
    preprocessing.TimeSeries.write_to_file: ["timeseries_data"],
    preprocessing.TimeSeries.assign_time: ["timeseries_data"],
    preprocessing.TimeSeries.clip: ["timeseries_data"],
    preprocessing.TimeSeries.assign_time: ["timeseries_data"],

    mf.mlp_model: ["model"],
    mf.rf_model: ["model"],
    mf.fit: ["trained_model""]
    mf.predict: ["predicted_values"]
}
