import os
import numpy as np
import matplotlib.pyplot as plt

# Insert file you want to plot:
target_file = "2024-04-10_16-29-35_out.gdat"

# Function to search for the target file within directories containing "run_"
def find_target_file(root_dir, target_filename):
    for root, dirs, files in os.walk(root_dir):
        for directory in dirs:
            if "run_" in directory:
                target_filepath = os.path.join(root, directory, target_filename)
                if os.path.isfile(target_filepath):
                    return target_filepath
    return None

# Search for the target file within the current directory "."
target_filepath = find_target_file(".", target_file)

if target_filepath is not None:
    print("Using file:", target_filepath)

    data = np.loadtxt(fname=target_filepath)
    data_new = np.delete(data, 0, 1)

    plt.xlabel("Iterations")
    plt.ylabel("Molecule count")
    plt.title("A+B->C")

    plt.plot(data_new)

    plt.savefig("high_res.png", dpi=500)
    plt.show()
else:
    print(f"File '{target_file}' not found in any directory containing 'run_'")

