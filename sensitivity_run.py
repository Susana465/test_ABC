import os
from prepare_run_files import prepare_out_folder
# Call the function "set_up_model" that runs mcell model with params specs from mcell_params.py
from mcell_params import set_up_model, process_parameters

def run_model(parameter_overrides, bngl_file="test_ABC.bngl"):
    # Define the parameter overrides and put it into a dict
    # Create a string that summarizes the parameter overrides for folder naming
    # override_str = '_'.join([f"{key}_{value}" for key, value in parameter_overrides.items()])

    # Set up the model described in mcell_params.py under the function set_up_model()
    model = set_up_model()

    # Define your MCell parameter files
    mcell_param_file = "mcell_params.py"

    # Call the function and capture the path to the run folder and timestamp
    run_folder, timestamp = prepare_out_folder("data_output", model.config.seed, files_to_copy=[bngl_file, mcell_param_file])

    # This wont run now, will run if set to True. Save viz_data under timestamped folder
    if False:
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

    # Process the parameters and save them to CSV
    ITERATIONS, df = process_parameters(bngl_file, run_folder, timestamp, parameter_overrides)

    # Check to see if total iterations is defined as a global parameter
    if ITERATIONS is None:
        ITERATIONS = 100

    # Set the total iterations (use the ITERATIONS from the BNGL or the overridden one)
    model.config.total_iterations = ITERATIONS

    # Initialize, export, and run the model
    model.initialize()
    model.run_iterations(ITERATIONS)
    model.end_simulation()

    return run_folder, timestamp, df

# different 'kon' values to run through
kon_values = [1e5,2e5,3e5,4e5,5e5,6e5,7e5,8e5,9e5,1e6]
koff_values = [1e-2, 1e1, 1e3, 1e5, 1e8]  

def parameter_sweep(values, parameter_name):
    """
    This (void) function does a parameter sweep by iterating over a list of values for a given parameter.

    It's primary goal is to perform an action (run model iteratively) rather than calculate and return a value.

    Arguments it takes:
    values (list): A list of values to sweep through for the specified parameter.
    parameter_name (str): The name of the parameter to override in each iteration.
    """
    for value in values:
        print(f"Starting run for {parameter_name} = {value}")
        parameter_overrides = {parameter_name: value}
        run_model(parameter_overrides)
        print(f"Run completed for {parameter_name} = {value}")

parameter_sweep(kon_values, 'kon')

# Iterate over the kon values and run the model
# for kon in kon_values:
#     print(f"Starting run for kon = {kon}") 
#     parameter_overrides = {'kon': kon}
#     run_model(parameter_overrides)
#     print(f"Run completed for kon = {kon}")

# # Iterate over the kon values and run the model
# for koff in koff_values:
#     print(f"Starting run for koff = {koff}") 
#     parameter_overrides = {'koff': koff}
#     run_model(parameter_overrides)
#     print(f"Run completed for koff = {koff}")

# def run_multiple_parameters(param_names, param_values_list):
#     """
#     Run the model for each combination of parameters in param_values_list.

#     param_names: List of parameter names (e.g., ['kon', 'koff'])
#     param_values_list: List of lists, where each list contains values for one parameter

#     """
#     # Determine the number of iterations (assumes all lists have the same length)
#     for param_combination in zip(*param_values_list):
#         parameter_overrides = {param_names[i]: param_combination[i] for i in range(len(param_names))}
#         print(f"Starting run with parameters: {parameter_overrides}")
#         run_model(parameter_overrides)
#         print(f"Run completed with parameters: {parameter_overrides}")

# # Run the model for both kon and koff values
# run_multiple_parameters(['kon', 'koff'], [kon_values, koff_values])