import os
from datetime import datetime

def save_run_iteration(folder_name, timestamp):
    # Create the folder if it doesn't exist
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    
    # Generate the filename
    filename = f"{folder_name}/dodecamer_run_{timestamp}.py"
    
    # Save the content of the current script to the generated filename
    with open(__file__, 'r') as f:
        content = f.read()
        with open(filename, 'w') as new_f:
            new_f.write(content)

# create a string name containing date to use for output files and folders
current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# Create the run folder
run_folder = f"run_{current_datetime}"
os.makedirs(run_folder)

# Modify these paths to save them under the run folder
viz_output_path = os.path.join(run_folder, f"viz_data/seed_00001/Scene_{current_datetime}")
gdat_output_path = os.path.join(run_folder, f"{current_datetime}_out.gdat")

# Here you would have your actual code
# viz_output = m.VizOutput(
#     viz_output_path,
#     every_n_timesteps=100
# )

# model.load_bngl(
#     'test_ABC.bngl', 
#     observables_path_or_file=gdat_output_path
# )

# For demonstration, let's save a single iteration with timestamp
save_run_iteration(run_folder, current_datetime)
