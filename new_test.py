import os
import sys
import numpy as np
from datetime import datetime
import pandas as pd
import shutil  # for easier file copying

# Call the function "set_up_model" that runs mcell model with params specs from mcell_params.py
from mcell_params import set_up_model

MCELL_PATH = os.environ.get('MCELL_PATH', '')
sys.path.append(os.path.join(MCELL_PATH, 'lib'))

import mcell as m

# Define the parameter overrides and put it into a dict
parameter_overrides = {
    'kon': 1e8  # Override kon to 2e8 / NA_um3
}

# Create a string that summarizes the parameter overrides for folder naming
override_str = '_'.join([f"{key}_{value}" for key, value in parameter_overrides.items()])

print(parameter_overrides)
print("Import of MCell was successful")

def prepare_out_folder(folder_name, seed, override_str="", files_to_copy=["file.bngl", "file.py"]):
    # Generate the current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    # Modify the folder name to include the override string
    if override_str:
        folder_name = os.path.join(folder_name, f"run_{timestamp}_seed_{seed}_overrides_{override_str}")
    else:
        folder_name = os.path.join(folder_name, f"run_{timestamp}_seed_{seed}")

    # Create the timestamped folder
    os.makedirs(folder_name)

    # Loop over each file and copy it to the destination folder
    for file_name in files_to_copy:
        dest_file = os.path.join(folder_name, file_name)  # Destination path with original name
        shutil.copy(file_name, dest_file)  # Copy the file with original name
    
    print(f"Files will be saved in {folder_name}.")

    return folder_name, timestamp

# Set up the model as before
model = set_up_model()

# Define your BNGL and MCell parameter files
bngl_file = "test_ABC.bngl"
mcell_param_file = "mcell_params.py"

# Call the function and capture the path to the run folder and timestamp
run_folder, timestamp = prepare_out_folder("data_output", model.config.seed, override_str=override_str, files_to_copy=[bngl_file, mcell_param_file])

# Save viz_data under timestamped folder
viz_output = m.VizOutput(
    os.path.join(run_folder, f"viz_data/Scene_"),
    every_n_timesteps=100
)
model.add_viz_output(viz_output)

# Load the BNGL file and apply the parameter overrides
model.load_bngl(
    os.path.join(run_folder, bngl_file), 
    observables_path_or_file=os.path.join(run_folder, f"{timestamp}_out.gdat"),
    parameter_overrides=parameter_overrides
)

# Process parameters and save the results to CSV
def process_parameters(file, folder, timestamp, parameter_overrides):
    """
    Load parameters from a (.bngl) file, convert them to a DataFrame, and save to a CSV file.
    Includes the override parameters to track what was changed.

    Parameters:
    - file: The name of the .bngl file containing parameters.
    - folder: The directory where the .bngl file is located and where output should be saved.
    - timestamp: A string representing the current timestamp, used for naming the output CSV file.
    - parameter_overrides: The dictionary of parameters to override.
    """
    # Load original parameters from the .bngl file
    param_dict = m.bngl_utils.load_bngl_parameters(os.path.join(folder, file))
    ITERATIONS = param_dict.get('ITERATIONS', None)  # Handle cases where 'ITERATIONS' might not be present

    # Convert dictionary to DataFrame
    df = pd.DataFrame.from_dict(param_dict, orient='index', columns=['Value'])
    
    # Add a column for parameter names
    df['Parameter'] = df.index

    # Append override parameters to the DataFrame for tracking
    for param, value in parameter_overrides.items():
        df.loc[param] = value  # Add the override value to the DataFrame (with param as index)

    # Define the CSV filename and save the DataFrame to CSV
    csv_filename = os.path.join(folder, f"{timestamp}_parameters_with_overrides.csv")
    df.to_csv(csv_filename, index=False)

    return ITERATIONS, df  # return the ITERATIONS and DataFrame if needed

# Process the parameters and save them to CSV
ITERATIONS, df = process_parameters(bngl_file, run_folder, timestamp, parameter_overrides)

# Check to see if total iterations is defined as a global parameter
if 'ITERATIONS' not in globals():
    ITERATIONS = 100

# Set the total iterations (use the ITERATIONS from the BNGL or the overridden one)
model.config.total_iterations = ITERATIONS

# Initialize, export, and run the model
model.initialize()
model.export_data_model()
model.run_iterations(ITERATIONS)
model.end_simulation()
