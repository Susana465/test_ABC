# This is the script where I prepare folders and call mcell and bngl params that may vary.
# Parameters are to be changed in the [define_simulation_params.py] file, not here.
import os
import sys
import numpy as np
from datetime import datetime
import pandas as pd
import shutil  # for easier file copying

# Call the function "set_up_model" that runs mcell model with params specs from define_simulation_params.py
from define_simulation_params import set_up_model

MCELL_PATH = os.environ.get('MCELL_PATH', '')
sys.path.append(os.path.join(MCELL_PATH, 'lib'))

import mcell as m

print("Import of MCell was sucessful")

def prepare_out_folder(folder_name, seed, files_to_copy=["file.bngl", "file.py"]):
    
    # Generate the current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    folder_name = os.path.join(folder_name, f"run_{timestamp}_seed_{seed}")

    # Create the timestamped folder
    os.makedirs(folder_name)

    # Loop over each file and copy it to the destination folder
    for file_name in files_to_copy:
        dest_file = os.path.join(folder_name, file_name)  # Destination path with original name
        shutil.copy(file_name, dest_file)  # Copy the file with original name
    
    print(f"Files will be saved in {folder_name}.")

    return folder_name, timestamp

model = set_up_model()

# Call the function and capture the path to the run folder and timestamp
run_folder, timestamp = prepare_out_folder("data_output", model.config.seed, ["test_ABC.bngl", "define_simulation_params.py"])

# Save viz_data under timestamped folder
viz_output = m.VizOutput(
    os.path.join(run_folder, f"viz_data/Scene_"),
    every_n_timesteps= 100
    )

model.add_viz_output(viz_output)

model.load_bngl(
    os.path.join(run_folder,'test_ABC.bngl'), 
    observables_path_or_file = os.path.join(run_folder, f"{timestamp}_out.gdat"))

# open bngl file and load the parameters into a dictionary
param_dict = m.bngl_utils.load_bngl_parameters(os.path.join(run_folder,'test_ABC.bngl'))
ITERATIONS = param_dict['ITERATIONS']

# Convert dictionary to DataFrame
df = pd.DataFrame.from_dict(param_dict, orient='index', columns=['Value'])
# Add a column for parameter names if needed
df['Parameter'] = df.index
# Save DataFrame to CSV within the timestamped folder to know what parameters were used for the output data
csv_filename = f"{run_folder}/{timestamp}_parameters.csv"
df.to_csv(csv_filename, index=False)

# Check to see if total iterations is defined as a global parameter
if 'ITERATIONS' not in globals():
        ITERATIONS = 100

# Total_Iterations if not defined explicitly default to 1e-6
model.config.total_iterations = ITERATIONS

model.initialize()

model.export_data_model()

model.run_iterations(ITERATIONS)

model.end_simulation()