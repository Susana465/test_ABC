import pandas as pd
import math  # To check for NaN

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

# Example usage
csv_file = "extracted_statsparams.csv"  # Replace with your actual CSV file
markdown_output = generate_markdown_table(csv_file)
print(markdown_output)
