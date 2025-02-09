import pandas as pd
import math  # To check for NaN
import matplotlib.pyplot as plt

def plot_parameter_vs_statistic(csv_file, param_column):
    """
    Plots the specified parameter against the statistic and displays the plot.

    Arguments:
        csv_file (str): The CSV file path that contains the data.
        param_column (str): The name of the parameter column to plot (e.g., 'kd', 'koff', 'kon').

    """
    # Load the CSV file
    df = pd.read_csv(csv_file)

    # Check if the required columns exist
    if param_column not in df.columns or "statistic" not in df.columns:
        raise ValueError(f"CSV file must contain '{param_column}' and 'statistic' columns.")
    
    # Scatter plot
    plt.figure(figsize=(8, 6))
    plt.scatter(df[param_column], df["statistic"], color="blue", alpha=0.7)
    plt.xlabel(f"{param_column} Value")
    plt.ylabel("Statistic Value")
    plt.title(f"{param_column} vs Statistic")
    
    # Apply log scale if the values are highly varied
    plt.xscale("log")
    plt.yscale("log")
    
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    
    # Show the plot
    plt.show()


# plot_parameter_vs_statistic("kd_stats.csv", "kon222")

def generate_markdown_table(csv_file):
    # Read the CSV file
    df = pd.read_csv(csv_file)
    
    # Extract unique kon and koff values
    kon_values = sorted(df['kon222'].unique())  # Sorting for better table structure
    koff_values = sorted(df['koff'].unique())
    
    # Create a dictionary to store Kd values
    kd_table = {koff: {kon: koff / kon if koff / kon == koff / kon else None for kon in kon_values} for koff in koff_values}
    
    # Remove columns (kon values) that have any NaN values
    valid_kon_values = [kon for kon in kon_values if all(kd_table[koff].get(kon) is not None for koff in koff_values)]
    
    # Generate Markdown table header
    header = "|   | " + " | ".join([f"kon = {kon}" for kon in valid_kon_values]) + " |"
    separator = "|" + "-------|" * (len(valid_kon_values) + 1)
    
    # Generate table rows
    rows = []
    for koff in koff_values:
        row = f"| koff = {koff} | " + " | ".join([f"{kd_table[koff][kon]:.6g}" if kd_table[koff][kon] is not None else "" for kon in valid_kon_values]) + " |"
        rows.append(row)
    
    # Combine everything into a markdown string
    markdown_table = "\n".join([header, separator] + rows)
    
    return markdown_table

# # Example usage
# csv_file = "extracted_statsparams.csv"  # Replace with your actual CSV file
# markdown_output = generate_markdown_table(csv_file)
# print(markdown_output)
