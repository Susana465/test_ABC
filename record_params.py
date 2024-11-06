
import pandas as pd

def read_gdat(filename):
    data = pd.read_table(filename,delim_whitespace=True)
    data.columns=data.columns[1:].append(pd.Index(["remove"]))
    return data.drop("remove",axis=1)

for kon in [10, 100, 1000, 10000]:
    #create function run_model, with all specified values in the model, except for this one here that i am interested in
    run_model(kon = kon)

# create a dataframe to store params 
params_stats = pd.DataFrame()

# read all the param files and data file, extract final [C] (use os.glob)
for files in all_files: #(use os.glob)
    parameters = pd.read_csv(parameter_file)
    data = read_gdat(data_file)
    statistic = extract_statistic(data)
    params_stats = pd.concat(params_stats,parameters,statistic)
    
#get stat out for any param - (kon vs statistic)
plot params_stats
