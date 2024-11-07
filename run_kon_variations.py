import os
import pandas as pd
from mcell_params import set_up_model
from prepare_run_files import prepare_out_folder

# Function to update the kon values in the .bngl file
def update_kon_in_bngl(bngl_file, kon_value, output_bngl_file):
    """
    Update the 'kon' value in the given BNGL file.

    Parameters:
    - bngl_file: The path to the original BNGL file.
    - kon_value: The new kon value to replace in the BNGL file.
    - output_bngl_file: The path where the modified BNGL file will be saved.
    """
    with open(bngl_file, 'r') as file:
        bngl_data = file.read()

    # Replace all occurrences of 'kon' in the file with the new kon_value
    updated_bngl_data = bngl_data.replace("kon = ", f"kon = {kon_value}")

    # Save the modified BNGL file to the output path
    with open(output_bngl_file, 'w') as file:
        file.write(updated_bngl_data)

# Set up the model
model = set_up_model()

# Define a range of kon values to test
kon_values = [0.1, 0.2, 0.5, 1.0, 2.0]  # Example values; adjust as needed

# Define what files I am using here:
bngl_file = "test_ABC.bngl"
mcell_param_file = "mcell_params.py"

# Call the function and capture the path to the run folder and timestamp
run_folder, timestamp = prepare_out_folder("data_output", model.config.seed, [bngl_file, mcell_param_file])

# Run the simulation
model.initialize()

# Loop over each kon value
for kon in kon_values:
    try:
        # Modify the BNGL file with the new kon value
        modified_bngl_file = os.path.join(run_folder, f"modified_{kon}_{bngl_file}")
        update_kon_in_bngl(os.path.join(run_folder, bngl_file), kon, modified_bngl_file)

        # Load the modified BNGL model
        model.load_bngl(
            modified_bngl_file, 
            observables_path_or_file=os.path.join(run_folder, f"{timestamp}_out.gdat"))

        print(f"Simulation for kon = {kon} completed. Data exported.")

    except Exception as e:
        print(f"Error during simulation for kon = {kon}: {e}")

if 'ITERATIONS' not in globals():
        ITERATIONS = 100
        
model.initialize()

model.export_data_model()

model.run_iterations(ITERATIONS)

model.end_simulation()