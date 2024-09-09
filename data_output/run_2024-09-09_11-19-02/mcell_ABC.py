import os
import sys
import numpy as np
from datetime import datetime
import pandas as pd
import shutil  # for easier file copying

def save_run_iteration(folder_name, files_to_copy=["test_ABC.bngl", "mcell_ABC.py"]):
    
    # Generate the current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    folder_name = os.path.join(folder_name, f"run_{timestamp}")

    # Create the timestamped folder
    os.makedirs(folder_name)

    # Loop over each file and copy it to the destination folder
    for file_name in files_to_copy:
        dest_file = os.path.join(folder_name, file_name)  # Destination path with original name
        shutil.copy(file_name, dest_file)  # Copy the file with original name
    
    print(f"Files have been saved in {folder_name}.")

    return folder_name, timestamp

# Call the function and capture the path to the run folder and timestamp
run_folder, timestamp = save_run_iteration("data_output")

MCELL_PATH = os.environ.get('MCELL_PATH', '')
sys.path.append(os.path.join(MCELL_PATH, 'lib'))

import mcell as m

print("Import of MCell was sucessful")

viz_output = m.VizOutput(
    os.path.join(run_folder, f"viz_data/seed_00001/Scene_{timestamp}"),
    every_n_timesteps= 100
    )

# Creting geometry
vol_cp = 0.50588 # units of um3
r = (3*vol_cp/(4*np.pi))**(1/3.0) # units of microns

cp = m.geometry_utils.create_icosphere(
    'CP', radius = r, subdivisions=2)
cp.is_bngl_compartment = True
cp.surface_compartment_name = 'PM'

model = m.Model()

model.add_viz_output(viz_output)
model.add_geometry_object(cp)

model.load_bngl(
    'test_ABC.bngl', 
    observables_path_or_file = os.path.join(run_folder, f"{timestamp}_out.gdat"))

#open bngl file and load the parameters into a dictionary
param_dict = m.bngl_utils.load_bngl_parameters('test_ABC.bngl')
ITERATIONS = param_dict['ITERATIONS']

# Convert dictionary to DataFrame
df = pd.DataFrame.from_dict(param_dict, orient='index', columns=['Value'])
# Add a column for parameter names if needed
df['Parameter'] = df.index
# Save DataFrame to CSV within the timestamped folder to know what parameters were used for the output data
csv_filename = f"{run_folder}/{timestamp}_parameters.csv"
df.to_csv(csv_filename, index=False)

# Specifies periodicity of visualization output
for count in model.counts:
    count.every_n_timesteps = 1

#Do not use bng units:
model.config.use_bng_units = False

# Check to see if total iterations is defined as a global parameter
if 'ITERATIONS' not in globals():
    ITERATIONS = 100

# Total_Iterations if not defined explicitly default to 1e-6
model.config.total_iterations = ITERATIONS
model.config.time_step = 1e-4 # time steps taken by individual molecules. but this time step is still used by all output statements.

model.config.partition_dimension = 1.5 # 1.5 was before
model.config.subpartition_dimension = 0.05

model.initialize()

model.export_data_model()

model.run_iterations(ITERATIONS)

model.end_simulation()
