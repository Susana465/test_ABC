import subprocess

def run_script(script_path):
    subprocess.run(["python", script_path])

def main():
    # Specify the path to your Python script
    script_path = "run_test.py"
    
    # Run the script
    run_script(script_path)

if __name__ == "__main__":
    main()
