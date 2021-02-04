import preporcessing as preprocessing
import modelingAndForecasting as mf
import visualization as vs

operator_input_keys = {
    preprocessing.TimeSeries: [],
    preprocessing.TimeSeries.read_from_file: ["timeseries_data"],
    preprocessing.TimeSeries.write_to_file: ["timeseries_data"],
    preprocessing.TimeSeries.assign_time: ["timeseries_data"],
    preprocessing.TimeSeries.clip: ["timeseries_data"],
    preprocessing.TimeSeries.assign_time: ["timeseries_data"],
    preprocessing.TimeSeries.denoise: ["timeseries_data"],
    preprocessing.TimeSeries.impute_missing: ["timeseries_data"],
    preprocessing.TimeSeries.difference: ["timeseries_data"],

    mf.train_test_split: [] #TODO,
    mf.mlp_model: [], # TODO,
    mf.rf_model: [], # TODO,
    mf.fit: ["model", "x_train", "y_train"],
    mf.predict: ["trained_model", "x_test"],

    vs.plot: ["ts_list"],
    vs.histogram: ["ts"],
    vs.box_plot: ["ts"],
    vs.normality_test: ["ts"],
    vs.mse: ["y_test", "y_forecast"],
    vs.mape: ["y_test", "y_forecast"],
    vs.smape: ["y_test", "y_forecast"]
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
    mf.fit: ["trained_model"],
    mf.predict: ["predicted_values"],

    vs.plot: [],
    vs.histogram: [],
    vs.box_plot: [],
    vs.normality_test: [],
    vs.mse: ["mse_float"],
    vs.mape: ["mape_percentage"],
    vs.smape: ["smape_percentaget"]
}
