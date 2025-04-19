import os
import pandas as pd
import matplotlib.pyplot as plt

# This plots all .gdat runs overlapped in one same png

def read_gdat(filename):
    # Read .gdat file into a DataFrame
    data = pd.read_table(filename, delim_whitespace=True)
    data.columns = data.columns[1:].append(pd.Index(["remove"]))
    return data.drop("remove", axis=1)

def plot_multiple_gdat(target_folder, selected_variables=None):
    # Loop through all .gdat files in the folder
    for root, dirs, files in os.walk(target_folder):
        for file in files:
            if file.endswith(".gdat"):
                target_filepath = os.path.join(root, file)
                print(f"Processing {file}...")

                # Load the data using read_gdat
                data = read_gdat(target_filepath)
                print(data.head())  # Print a preview of the data

                # Extract column names (headers)
                header = data.columns[1:]  # Exclude the first column (assumed to be time)

                # If no specific variables are selected, plot all
                if selected_variables is None:
                    selected_variables = header  # Plot all variables

                # Plot selected variables
                for var_name in selected_variables:
                    if var_name in data.columns:
                        plt.plot(data.iloc[:, 0], data[var_name], label=f"{file} - {var_name}")
                    else:
                        print(f"Variable '{var_name}' not found in {file}. Skipping.")
    # Customize the plot
    plt.xlabel("Time(s)")
    plt.ylabel("Molecule Count")
    plt.title("Molecules Interacting Throughout Time")
    plt.legend()

    # Save the plot as a PNG file, change name of output file here
    output_png_filepath = os.path.join(target_folder, "nmdar_camkii_complex_plot.png")
    plt.savefig(output_png_filepath, dpi=500)

    plt.show()
    print(f"Your combined plot has been saved as {output_png_filepath}")


if __name__ == "__main__":
    target_folder = input("Enter the path to the folder containing .gdat files: ")
    selected_variables = input("Enter variables to plot, separated by commas (or press Enter to plot all): ").split(",")
    selected_variables = [var.strip() for var in selected_variables if var.strip()]  # Clean whitespace

    plot_multiple_gdat(target_folder, selected_variables)
