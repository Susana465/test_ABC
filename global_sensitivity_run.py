from run_model import run_model
import itertools # is a module in Python that provides a set of fast, memory-efficient tools for working with iterators (objects that generate items one at a time).

import numpy as np

factors = np.array([0.001, 0.01, 0.1, 1, 10, 100, 1000])

# different 'kon' values to run through
kon_values = 1e8*factors
koff_values = 1e-2*factors

# Kd = [500]
# Kd = koff/kon
# kon = koff/Kd
# koff= Kd x kon

# # Note that if parameter_value does not match, this code currently will not throw an error and will just run with the preset value stated in the .bngl file. 
# # Check the .csv of values to see which 'kon' was used
# def parameter_sweep(constant, param_values):
#     # Create a list of parameter names (keys from the dictionary)
#     param_names = list(parameters_dict.keys())

#     for value in param_values:
        

def parameter_sweep(parameters_dict):
    """
    This (void) function does a parameter sweep by iterating over a list of values for a given parameter.

    It's primary goal is to perform an action (run model iteratively) rather than calculate and return a value.

    Arguments it takes:
    parameters_dict (dict): 
    A dictionary where -
    keys are param_names (e.g. 'kon', 'koff') 
    and param_value_combinations are lists of values to sweep through for those parameters.
    """
    # Create a list of parameter names (keys from the dictionary)
    param_names = list(parameters_dict.keys())

    # Generate all combinations of parameter values using itertools.product
    # The '*' unpacks the lists of values associated with each parameter, so they can be passed as separate arguments
    # This will generate all combinations of values for the parameters in the dictionary
    param_value_combinations = itertools.product(*parameters_dict.values())

    for param_values in param_value_combinations:
        # Create a dictionary of parameter overrides
        parameter_overrides = dict(zip(param_names, param_values))

        # Print out the parameters and their corresponding values for this run
        print(f"Starting run with parameters: {parameter_overrides}")
        
        # Call the model with the current parameter overrides
        run_model(parameter_overrides)
        
        print(f"Run completed for parameters: {parameter_overrides}")


# Define the parameters and their possible values
parameters = {
    'kon222': kon_values,  # Replace with the actual parameter name in the model
    'koff': koff_values  # Replace with the actual parameter name in the model
}

# Run the parameter sweep for kon and koff
parameter_sweep(parameters)