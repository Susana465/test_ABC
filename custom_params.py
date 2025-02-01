import os
import sys
import numpy as np
from datetime import datetime
import pandas as pd
from prepare_run_files import prepare_out_folder
import shutil  # for easier file copying

# Call the function "set_up_model" that runs mcell model with params specs from mcell_params.py
from mcell_params import set_up_model

MCELL_PATH = os.environ.get('MCELL_PATH', '')
sys.path.append(os.path.join(MCELL_PATH, 'lib'))

import mcell as m

print("Import of MCell was sucessful")

model = set_up_model()

print(model)

# Define the parameter overrides
parameter_overrides = {
    'kon': 1e8  # Override kon to 2e8 / NA_um3
}

# Define what files I am using here:
bngl_file = "test_ABC.bngl"
mcell_param_file = "mcell_params.py"

# Load the BNGL file and apply the parameter overrides
model.load_bngl(
    os.path.join(run_folder, bngl_file), 
    observables_path_or_file=os.path.join(run_folder, f"{timestamp}_out.gdat"),
    parameter_overrides=parameter_overrides
)

print("This is model_load: ", model.load_bngl("test_ABC.bngl"))
"""
def custom_argparse_and_parameters():
    # When uncommented, this function is called to parse
    # custom commandline arguments.
    # It is executed before any of the automatically generated
    # parameter values are set so one can override the parameter
    # values here as well.
    # To override parameter values, add or overwrite an item in dictionary
    shared.parameter_overrides['SEED'] = 10
    pass
"""


"""
def custom_config(model):
    # When uncommented, this function is called to set custom
    # model configuration.
    # It is executed after basic parameter setup is done and
    # before any components are added to the model.
    pass
"""

"""
def custom_init_and_run(model):
    # When uncommented, this function is called after all the model
    # components defined in CellBlender were added to the model.
    # It allows to add additional model components before initialization
    # is done and then to customize how simulation is ran.
    # The module parameters must be imported locally otherwise
    # changes to shared.parameter_overrides done elsewhere won't be applied.
    import Scene_parameters as parameters
    model.initialize()
    model.run_iterations(parameters.ITERATIONS)
    model.end_simulation()
"""