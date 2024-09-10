# What is in this repository

This is a toy repo where I create equivalent models of my thesis project. I test the files here with models that run a lot faster and are much simpler than my dodecamer one. 

There might be some files that are saved as tests outside of the main ones, as I try out different things.

The important files to run the simulation are:

## Parameter files:
- [`mcell_params.py`](mcell_params.py): where variable mcell parameters are stored, and can be changed.
- [`test_ABC.bngl`](test_ABC.bngl)

## Run-the-model files:
- [`prepare_run_files.py`](prepare_run_files.py): script that prepares files to be copied, ran, and saved in a timestamped folder.
- [`run_python_files.py`](run_python_files.py): script executor that automates the execution of the other Python scripts.

## Output files
- `data_output/`: contains timestamped folders that are created with scripts mentioned above. Each timestamped folder contains the outputs from running the python scripts.

# How to use files in this repo

## Step 1
Have a look at the [`test_ABC.bngl`](test_ABC.bngl) file, are you happy with the parameters being used? 

Would you like to change something? You can make changes in this file, which will then be accessed via [`prepare_run_files.py`](prepare_run_files.py) to load its parameters and run them through mcell. More information on how this works can be found in this documentation [Loading a BNGL File](https://mcell.org/mcell4_documentation/bngl.html)

## Step 2
Once you are happy with parameters set in the .bngl file, go to the [`mcell_params.py`](mcell_params.py) file. You can change parameters in here too, if necessary. These are also accessed via [`prepare_run_files.py`](prepare_run_files.py).

## Step 3
After making sure parameters are all set up, the [`prepare_run_files.py`](prepare_run_files.py) file prepares a timestamped folder where a copy of the used files above are saved. It also saves visualisation data and a parameters.csv file that contains parameters extracted from the .bngl file used. 

You do not need to do anything here, but it is useful to have a look at what this file looks like to understand what is happening when the ode is being run. 

## Step 4
Run the following in your command line:

```python
python run_python_files.py
```

This works python magic to action all the instructions given in the other python scripts.