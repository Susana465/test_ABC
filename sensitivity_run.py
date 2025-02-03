import os

from run_model import run_model

# different 'kon' values to run through
kon_values = [2e1]
koff_values = [] 

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

#parameter_name argument needs to match the name of the parameter_kon/koff in the bngl file (as its saved into a dictionary that is later used to access this value)
parameter_sweep(kon_values, 'kon')