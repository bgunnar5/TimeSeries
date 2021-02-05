import preporcessing as preprocessing
import modelingAndForecasting as mf
import operatorkeys as ok
import visualization as vis
from tree import *
filename = "Project Description/Time Series Data/1_temperature_test.csv"
def main():
    t = TransformationTree(ok.operator_input_keys, ok.operator_output_keys)
    read = t.add_operator(preprocessing.TimeSeries.read_from_file, t.root,args=[filename], tag="read")
    
    assign_time = t.add_operator(preprocessing.TimeSeries.assign_time, read, args=["01/01/2000 12:30", 24])
    denoise = t.add_operator(preprocessing.TimeSeries.denoise, read)
    ts2db = t.add_operator(preprocessing.TimeSeries.ts2db, denoise, args=[None, 0.8, 0.1, 0.1, 2, 1, None])
    model = t.add_operator(mf.mlp_model, ts2db,args=[10,1], tag="model")
    fit = t.add_operator(mf.fit, model)
    predict = t.add_operator(mf.predict, fit)
    mse = t.add_operator(vis.mse, predict, tag="mse", save_result=True)

    # Creating new branch with Random Forest model instead
    t.replicate_subtree(model, tag_modifier="_rf_branch")
    model_node_copy = t.get_nodes_by_tag("model_rf_branch")[0]
    t.replace_operator(mf.rf_model, model_node_copy)
    
    t.execute_tree()
    print(t.results)
    
    

main()


# = vis.mse([i+5 for i in range(100)],[i+10 for i in range(100)])
#print(a)