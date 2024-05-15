import os
import pandas as pd
import json

from finance_process import process_excel

def process_json_output():
    # Define the directory paths
    salaryslips_dir = 'salaryslips'
    output_json_dir = 'output_json'
    yaml_dir = 'cat_yaml'
    # Ensure the output directory exists
    os.makedirs(output_json_dir, exist_ok=True)


    # Iterate over the .xls files in the salaryslips directory
    for filename in os.listdir(salaryslips_dir):
        if filename.endswith('.xls'):
            # Generate the full path to the file
            file_path = os.path.join(salaryslips_dir, filename)
            
            # Call the process_excel function to get the JSON output
            json_output = process_excel(file_path, yaml_dir)
            
            if json_output is not None:  # Check if JSON output is generated successfully
                # Access the value associated with the key 'Month'
                current_month = json_output['Month']
                
                # Generate the output JSON filename
                output_filename = os.path.join(output_json_dir, f'{current_month}.json')
                
                # Convert JSON output to a string
                json_string = json.dumps(json_output)
                
                # Write the JSON output string to a file
                with open(output_filename, 'w') as json_file:
                    json_file.write(json_string)
            else:
                print(f"Error processing Excel file '{file_path}'. JSON output is None.")