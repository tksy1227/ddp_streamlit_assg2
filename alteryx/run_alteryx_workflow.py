import os
import subprocess

def refresh_bus_data(bus_code):
    workflow_path = "alteryx/assg2_workflow.yxmd"  # Update with the path to your .yxmd file
  #  output_file = f"output_{bus_code}.csv"  # Example: specify an output file if needed
    print(f"Running Alteryx workflow for bus code: {bus_code}")
    
    # Command to run the workflow
    command = f'"C:\Users\User\AppData\Local\Alteryx\bin\\AlteryxEngineCmd.exe" "{workflow_path}"'
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    # Check the result of the execution
    if result.returncode == 0:
        print(f"Workflow ran successfully for bus code {bus_code}")
    else:
        print(f"Error running workflow: {result.stderr}")

if __name__ == "__main__":
    import sys
    bus_code = sys.argv[1] if len(sys.argv) > 1 else "12101"
    refresh_bus_data(bus_code)
