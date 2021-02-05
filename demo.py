import preporcessing as preprocessing
import modelingAndForecasting as mf
import operatorkeys as ok
import visualization as vis
from tree import *
filename = "Project Description/Time Series Data/1_temperature_test.csv"
def main():
    t = TransformationTree(ok.operator_input_keys, ok.operator_output_keys)
    # Creating a single branch
    read = t.add_operator(preprocessing.TimeSeries.read_from_file,[filename], t.root, tag="read")
    assign_time = t.add_operator(preprocessing.TimeSeries.assign_time,["01/01/2000 12:30", 24], read )
    denoise = t.add_operator(preprocessing.TimeSeries.denoise, [], assign_time)
    ts2db = t.add_operator(preprocessing.TimeSeries.ts2db, [None, 0.8, 0.1, 0.1, 2, 1, None], denoise, tag="db", save_result=False)
    model = t.add_operator(mf.mlp_model, [], ts2db, tag="model")
    fit = t.add_operator(mf.fit, [],model)
    predict = t.add_operator(mf.predict, [], fit)
    mse = t.add_operator(vis.mse,[], predict, tag="mse", save_result=True)

    # Save then loading tree, and finding the ts2db operator in the branch we previously created
    save(t, "demo_tree.sav")
    t = load("demo_tree.sav")
    ts2db_operator = t.get_nodes_by_tag("db")[0]

    # Replicating the part of the branch at or below the ts2db operator
    db_operators = [t.replicate_subtree(ts2db_operator, tag_modifier=f"_{2+1+i}_features") for i in range(10)]
    
    # Looping through the new subtrees and modifying their ts2db operators to take in different number of datapoints as input 
    counter = 1
    for node in db_operators:
        t.replace_operator(preprocessing.TimeSeries.ts2db, [None, 0.8, 0.1, 0.1, 2+counter, 1, None], node)
        counter += 1

    # Executing tree
    t.execute_tree()

    sorted_results = sorted(t.results, key=lambda x: x[0])
    best_branch = sorted_results[0]
    print(f"Best MSE: {best_branch[0]}, from branch: {t.get_path_str(best_branch[1])}")    

main()
