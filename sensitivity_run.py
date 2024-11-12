
# General Workflow:
# Loop Over kon Values:
# need to run the model with different kon values. 
# Make a run_model() function responsible for running the simulation with the specified kon value.

# Reading Output Files:
# After each model run, need to read the resulting .gdat file, extract the statistic 
# (e.g., the final concentration [C]), and store this information in a DataFrame.

# Create a DataFrame:
# Store the statistics (kon and the extracted concentration) for each model run in a DataFrame.

# Plot the Results:
# After collecting all the statistics, plot how the concentration changes with respect to kon.


# open, whilst open, read bngl file
# find line where kon is defined
#change kon value
# save it as a specific new file copy with kon

import os
import pandas as pd
from mcell_params import set_up_model
import matplotlib.pyplot as plt
from new_test import run_model

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

# Create an empty dataframe to store stats
params_stats = pd.DataFrame(columns=['kon', 'statistic'])

#run model with different kon

for kon in [10, 100, 1000, 10000]:
    # Run the model with the current kon (this step doesn't repeat initialization)
    run_folder, timestamp, df = run_model(parameter_overrides={'kon': kon}, bngl_file="test_ABC.bngl")
    # Read output data and store statistics
    data_files = glob.glob(os.path.join(run_folder, "*_out.gdat"))
    for data_file in data_files:
        data = read_gdat(data_file)
        statistic = extract_statistic(data)

        # Store the parameters and statistic
        result = pd.DataFrame({
            'kon': [kon],
            'statistic': [statistic]
        })
        params_stats = pd.concat([params_stats, result], ignore_index=True)

# Plot the results
plt.figure(figsize=(10, 6))
plt.plot(params_stats['kon'], params_stats['statistic'], marker='o', linestyle='-')
plt.xlabel('kon')
plt.ylabel('Statistic')
plt.title('kon vs Statistic')
plt.grid(True)
plt.show()

# https://mcell.org/tutorials/scripting/customization.html 

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

# General Workflow:
# Loop Over kon Values:
# You'll need to run the model with different kon values. The run_model() function is responsible for running the simulation with the specified kon value.

# Reading Output Files:
# After each model run, you'll need to read the resulting .gdat file, extract the statistic (e.g., the final concentration [C]), and store this information in a DataFrame.

# Create a DataFrame:
# You’ll store the statistics (kon and the extracted concentration) for each model run in a DataFrame.

# Plot the Results:
# After collecting all the statistics, you'll plot how the concentration changes with respect to kon.