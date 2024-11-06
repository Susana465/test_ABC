import pandas as pd

# read gdat file output and put it into a dataframe
def read_gdat(filename):
    data = pd.read_table(filename, delim_whitespace=True)
    data.columns = data.columns[1:].append(pd.Index(["remove"]))
    return data.drop("remove", axis=1)

# Call the function with the path to .gdat file
filename = 'data_output/run_2024-11-06_10-45-17_seed_2/2024-11-06_10-45-17_out.gdat'  # Replace with your actual file path
data = read_gdat(filename)

# Now `data` holds the DataFrame returned by read_gdat
print(data)  # Print or use `data` as needed

# Out of which I want to extract the stat I am interested in, such as:
# Final molecule count 'C'
# iloc[-1] is used to select the last row in the DataFrame 
stat = data['C'].iloc[-1]

def extract_statistic(data):
    # Dummy function for extracting final concentration [C]
    stat = data['C'].iloc[-1]
    return stat

print("Final molecule count for column C:")
print(stat)

#i want mcell to run with different kon that i input here, 
# for kon in [10, 100, 1000, 10000]:
#     #create function run_model, with all specified values in the model, except for this one here that i am interested in
#     run_model(kon = kon)

# # read all the param files and data file, extract final [C] (use os.glob)
# for files in all_files: #(use os.glob)
#     parameters = pd.read_csv(parameter_file)
#     data = read_gdat(data_file)
#     statistic = extract_statistic(data)
#     params_stats = pd.concat(params_stats,parameters,statistic)

#give me a .gdat file output
# access each gdat stat for each kon, create a dataframe which stores the stats I am interested in recording