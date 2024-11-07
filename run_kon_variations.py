import os
import sys

# Ensure MCELL_PATH is set correctly before importing mcell
MCELL_PATH = os.environ.get('MCELL_PATH', '')
sys.path.append(os.path.join(MCELL_PATH, 'lib'))  # Add the MCell lib path to sys.path

# Now we can safely import mcell
import mcell as m
import pandas as pd

# Print the current sys.path to check if it includes the correct directory
print("System path:", sys.path)

# Add the current directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Now try importing Scene_parameters
import Scene_parameters as parameters


# Function to update the 'kon' value in the BNGL file
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

# Function to initialize the model and run the simulation
def custom_init_and_run(model):
    """
    Custom initialization and simulation running, iterating step-by-step.
    """
    try:
        # Find the predator count (or adjust to your model)
        predator_count = model.find_count('A')  # Replace 'A' with the species name if needed

        # Ensure predator_count is found
        if predator_count is None:
            raise Exception("Predator count object not found.")

        # Initialize the model
        model.initialize()

        # Run the simulation for the specified number of iterations
        for i in range(parameters.ITERATIONS):
            model.run_iterations(1)  # Run one iteration per loop

            # Get current predator count (replace 'A' with correct species if necessary)
            p = predator_count.get_current_value()

            # Print the predator count for feedback
            print(f"Iteration {i + 1} - Predator count (species A): {p} (kon = {parameters.kon})")

            # Check for a zero predator count and terminate if found
            if p == 0:
                sys.exit(f"Error: predator count is 0, terminating simulation at iteration {i + 1}.")

        # Finalize the simulation
        model.end_simulation()

    except Exception as e:
        print(f"Error during simulation: {e}")

# Set up the model
model = m.Model()

# Set simulation parameters
model.config.seed = 12345  # Example seed, replace as needed

# Define the BNGL file and its path
bngl_file = "test_ABC.bngl"
mcell_param_file = "mcell_params.py"

# Directory for storing results
run_folder = "data_output"
timestamp = "timestamp_example"  # Replace with actual timestamp logic if needed

# Load the original BNGL model
model.load_bngl(os.path.join(run_folder, bngl_file))

# Define kon values to test
kon_values = [0.1, 0.2, 0.5, 1.0, 2.0]  # Example values

# Loop over each kon value and run the simulation
for kon in kon_values:
    try:
        # Update the BNGL file with the new kon value
        modified_bngl_file = os.path.join(run_folder, f"modified_{kon}_{bngl_file}")
        update_kon_in_bngl(os.path.join(run_folder, bngl_file), kon, modified_bngl_file)

        # Reload the modified BNGL file with the new kon value
        model.load_bngl(modified_bngl_file)

        # Set the kon value for the simulation (in case it's needed in model)
        parameters.kon = kon  # Assuming Scene_parameters.py has the kon value

        # Run the simulation with custom initialization and iteration
        print(f"Running simulation for kon = {kon}...")
        custom_init_and_run(model)
        print(f"Simulation for kon = {kon} completed.")

    except Exception as e:
        print(f"Error during simulation for kon = {kon}: {e}")
