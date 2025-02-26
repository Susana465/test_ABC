import os
import pandas as pd

# Define the base directory and the output CSV path
# The 'r' before the string makes it a raw string, preventing escape sequences (e.g., \n or \t) from being processed
base_dir = r'D:/CaMKII_hexa_bgnl_to_mcellcop2/data_output/yesNMDAR/'
output_csv = r'D:/CaMKII_hexa_bgnl_to_mcellcop2/data_output/yesNMDAR/Parameters_Overview.csv'

# Initialize a list to store the data from all runs
data = []

# Iterate through each run directory
for run_folder in os.listdir(base_dir):
    run_path = os.path.join(base_dir, run_folder)
    if os.path.isdir(run_path):
        # Extract metadata from the folder name (date and seed)
        run_id = run_folder
        date, seed = run_id.split('_')[1], run_id.split('_')[-1]
        
        print(f"Processing run: {run_id}, Date: {date}, Seed: {seed}")  # Debug print
        
        # Locate the parameters.csv file
        param_file = [f for f in os.listdir(run_path) if f.endswith('_parameters.csv')]
        
        if param_file:
            param_file_path = os.path.join(run_path, param_file[0])
            print(f"Found parameters file: {param_file_path}")  # Debug print

            # Read parameters.csv into a DataFrame
            try:
                param_df = pd.read_csv(param_file_path, sep=',', header=None, names=['Value', 'Parameter'])
                print("Data from parameters.csv loaded successfully")  # Debug print
            except Exception as e:
                print(f"Error loading CSV file: {e}")
                continue
            
            # Debug: Show first few rows to verify contents
            print(f"First few rows of parameters CSV:\n{param_df.head()}")

            # Extract parameter-value pairs and store them in a dictionary
            param_dict = dict(zip(param_df['Parameter'], param_df['Value']))
            print(f"Extracted parameters for run {run_id}: {param_dict}")  # Debug print

            # Compile the data for this run, including the run metadata
            run_data = {
                'Run ID': run_id,
                'Date': date,
                'Seed': seed
            }
            run_data.update(param_dict)  # Add all parameters as columns

            # Add this run's data to the list
            data.append(run_data)

# Convert the collected data into a DataFrame
df = pd.DataFrame(data)

# Debug print to check the final DataFrame
print(f"Final DataFrame:\n{df.head()}")  # Debug print

# Save the DataFrame to a CSV file
df.to_csv(output_csv, index=False)

print(f'Parameters overview has been saved to {output_csv}.')