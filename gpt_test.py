import os
from datetime import datetime

def save_run_iteration(folder_name, timestamp):
    # Create the folder if it doesn't exist
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    
    # Generate the filename
    filename = f"{folder_name}/dodecamer_run_{timestamp}.py"
    
    # Save the content of the current script to the generated filename
    with open(__file__, 'r') as f:
        content = f.read()
        with open(filename, 'w') as new_f:
            new_f.write(content)

def main():
    # create a string name containing date to use for output files and folders
    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    # For demonstration, let's save a single iteration with timestamp
    save_run_iteration(f"run_{current_datetime}", current_datetime)

if __name__ == "__main__":
    main()
