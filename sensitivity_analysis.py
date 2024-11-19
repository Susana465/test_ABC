import os
import pandas as pd
import matplotlib.pyplot as plt
import glob

# read gdat file output and put it into a dataframe
def read_gdat(filename):
    data = pd.read_table(filename, delim_whitespace=True)
    data.columns = data.columns[1:].append(pd.Index(["remove"]))
    return data.drop("remove", axis=1)

# Call the function with the path to .gdat file
# filename = 'data_output/run_2024-11-06_10-45-17_seed_2/2024-11-06_10-45-17_out.gdat'  # Replace with your actual file path
# data = read_gdat(filename)

# Now `data` holds the DataFrame returned by read_gdat
#print(data)  # Print or use `data` as needed

# Out of which I want to extract the stat I am interested in, such as:
# Final molecule count 'C'
# iloc[-1] is used to select the last row in the DataFrame 

def extract_statistic(data):
    # function for extracting final concentration [C]
    stat = data['C'].iloc[-1]
    print("Final molecule count for column C:")
    print(stat)
    return stat

# Create an empty dataframe to store stats
params_stats = pd.DataFrame(columns=['kon', 'statistic'])
print(params_stats)

# for any directory structure, pull all params we've used an the stats we have defined as above

for run_folder in [os.path.join('data_output', dir) for dir in os.listdir('data_output')]:
    try:
        # Read output data and store statistics
        data_files = glob.glob(os.path.join(run_folder, "*_out.gdat"))
        if len(data_files) > 1:
            raise Exception(f"More than one .gdat file in directory {run_folder}")
        if len(data_files) == 0:
            raise Exception(f"No .gdat file in directory {run_folder}")
        
        param_files = glob.glob(os.path.join(run_folder, "*_parameters.csv"))
        if len(param_files) > 1:
            raise Exception(f"More than one .csv file in directory {run_folder}")
        if len(param_files) == 0:
            raise Exception(f"No .csv file in directory {run_folder}")
        
        # If files are found, proceed with processing
        data = read_gdat(data_files[0])
        params = pd.read_csv(param_files[0])

        statistic = extract_statistic(data)
        kon_value = params.get('kon', [None])[0]
        params_stats = params_stats.append({'kon': kon_value, 'statistic': statistic}, ignore_index=True)  

    # Continue to the next folder despite the error    
    except Exception as e:
        print(f"Error in folder {run_folder}: {e}")
        continue

params_stats.to_csv('extracted_statistics.csv', index=False)

#     #for data_file in data_files:
#         # data = read_gdat(data_file)
#         # statistic = extract_statistic(data)
#         # # Store the parameters and statistic
#         # result = pd.DataFrame({
#         #     'kon': [kon],
#         #     'statistic': [statistic]
#         # })
#         # params_stats = pd.concat([params_stats, result], ignore_index=True)

# # Plot the results
# # plt.figure(figsize=(10, 6))
# # plt.plot(params_stats['kon'], params_stats['statistic'], marker='o', linestyle='-')
# # plt.xlabel('kon')
# # plt.ylabel('Statistic')
# # plt.title('kon vs Statistic')
# # plt.grid(True)
# # plt.show()

# # https://mcell.org/tutorials/scripting/customization.html 

# #i want mcell to run with different kon that i input here, 
# # for kon in [10, 100, 1000, 10000]:
# #     #create function run_model, with all specified values in the model, except for this one here that i am interested in
# #     run_model(kon = kon)

# # # read all the param files and data file, extract final [C] (use os.glob)
# # for files in all_files: #(use os.glob)
# #     parameters = pd.read_csv(parameter_file)
# #     data = read_gdat(data_file)
# #     statistic = extract_statistic(data)
# #     params_stats = pd.concat(params_stats,parameters,statistic)

# #give me a .gdat file output
# # access each gdat stat for each kon, create a dataframe which stores the stats I am interested in recording

# # General Workflow:
# # Loop Over kon Values:
# # You'll need to run the model with different kon values. The run_model() function is responsible for running the simulation with the specified kon value.

# # Reading Output Files:
# # After each model run, you'll need to read the resulting .gdat file, extract the statistic (e.g., the final concentration [C]), and store this information in a DataFrame.

# # Create a DataFrame:
# # You’ll store the statistics (kon and the extracted concentration) for each model run in a DataFrame.

# # Plot the Results:
# # After collecting all the statistics, you'll plot how the concentration changes with respect to kon.