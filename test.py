import os
import pandas as pd
import glob
import numpy as np
from sensitivity_store_analysis import read_gdat, extract_statistic

# Define the base directory and the output CSV path
base_dir = r'D:/CaMKII_hexa_bgnl_to_mcellcop2/data_output/noNMDAR/2025'
output_csv = r'D:/CaMKII_hexa_bgnl_to_mcellcop2/data_output/noNMDAR/2025/Parameters_Overview.csv'

# Initialize a list to store the data from all runs
data = []
molecule = "CaM_free"

# Iterate over each run folder in the base directory
for run_path in glob.glob(os.path.join(base_dir, 'run_*')):
    run_id = os.path.basename(run_path)
    date = "2025-02-27"  # Replace with actual date extraction logic if needed
    seed = "1234"  # Replace with actual seed extraction if needed

    param_dict = {}

    # Attempt to find the .gdat file in the current run folder
    gdat_files = glob.glob(os.path.join(run_path, "*.gdat"))
    if gdat_files:
        gdat_file_path = gdat_files[0]
        # Check if the .gdat file is empty
        if os.path.getsize(gdat_file_path) == 0:
            print(f".gdat file {gdat_file_path} is empty. Skipping.")
            param_dict[molecule] = np.nan
        else:
            gdat_data = read_gdat(gdat_file_path)
            stat = extract_statistic(gdat_data, molecule, stat_type="last")
            print(f"Extracted statistic for {molecule}: {stat}")
            param_dict[molecule] = stat
    else:
        print(f"No .gdat file found in {run_path}. Skipping.")
        param_dict[molecule] = np.nan

    run_data = {'Run ID': run_id, 'Date': date, 'Seed': seed}
    run_data.update(param_dict)
    data.append(run_data)

# Convert the collected data into a DataFrame
df = pd.DataFrame(data)

# Save the DataFrame to a CSV file
df.to_csv(output_csv, index=False)

print(f'Parameters overview has been saved to {output_csv}.')
