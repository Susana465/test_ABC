# This is the script where I prepare folders to save model runs
import os
import sys
from datetime import datetime
import pandas as pd
import shutil  # for easier file copying
import mcell as m

MCELL_PATH = os.environ.get('MCELL_PATH', '')
sys.path.append(os.path.join(MCELL_PATH, 'lib'))

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

def process_parameters(file, folder, timestamp):
    """
    Load parameters from a (.bngl) file, convert them to a DataFrame, and save to a CSV file.

    Parameters:
    - file: The name of the .bngl file containing parameters.
    - folder: The directory where the .bngl file is located and where output should be saved.
    - timestamp: A string representing the current timestamp, used for naming the output CSV file.
    """
    # Load parameters from the .bngl file
    param_dict = m.bngl_utils.load_bngl_parameters(os.path.join(folder, file))
    ITERATIONS = param_dict.get('ITERATIONS', None)  # Handle cases where 'ITERATIONS' might not be present

    # Convert dictionary to DataFrame
    df = pd.DataFrame.from_dict(param_dict, orient='index', columns=['Value'])
    
    # Add a column for parameter names
    df['Parameter'] = df.index

    # Define the CSV filename and save the DataFrame to CSV
    csv_filename = os.path.join(folder, f"{timestamp}_parameters.csv")
    df.to_csv(csv_filename, index=False)

    return ITERATIONS, df  # return the ITERATIONS and DataFrame if needed
