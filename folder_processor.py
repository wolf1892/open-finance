import os
import json
from datetime import datetime
from dateutil.relativedelta import relativedelta
import calendar

def get_month(month_name):
    # Convert month name to its numeric representation
    month_num = list(calendar.month_name).index(month_name.capitalize())
    month_str = str(month_num).zfill(2)  # Zero-padding to ensure 2 digits (e.g., '03')

    # Path to the output_json folder
    output_json_folder = 'output_json'

    # Construct the filename based on the input month
    filename = f'2024-{month_str}-01.json'

    # Check if the file exists
    file_path = os.path.join(output_json_folder, filename)
    if os.path.exists(file_path):
        # Read contents of the JSON file
        with open(file_path, 'r') as file:
            month_data = json.load(file)
        return month_data
    else:
        return None  # File not found



def current_month():

    # Path to the output_json folder
    output_json_folder = 'output_json'

    # Step 1: Identify the latest month
    files = os.listdir(output_json_folder)
    latest_file = max(files)  # Get the latest file based on its name
    latest_month = latest_file.split('.')[0]  # Extract the month from the filename

    # Step 2: Read contents of the latest month's JSON file (current_month)
    current_month_file = os.path.join(output_json_folder, latest_file)
    with open(current_month_file, 'r') as file:
        current_month = json.load(file)

    return current_month

def last_six_month():
    # Path to the output_json folder
    output_json_folder = 'output_json'

    # Step 1: Identify the latest month
    files = os.listdir(output_json_folder)
    latest_file = max(files)  # Get the latest file based on its name
    latest_month = latest_file.split('.')[0]  # Extract the month from the filename

    # Step 2: Read contents of the latest month's JSON file (current_month)
    current_month_file = os.path.join(output_json_folder, latest_file)
    with open(current_month_file, 'r') as file:
        current_month = json.load(file)   

    # Step 3: Determine the last 6 months including the current month
    last_6_months = []
    current_date = datetime.strptime(latest_month, '%Y-%m-%d')
    for i in range(6):
        last_month = current_date - relativedelta(months=i)
        last_6_months.append(last_month.strftime('%Y-%m-01'))

    # Step 4: Read contents of JSON files for the last 6 months
    last_6_months_contents = {}
    for month in last_6_months:
        month_file = os.path.join(output_json_folder, f'{month}.json')
        if os.path.exists(month_file):
            with open(month_file, 'r') as file:
                last_6_months_contents[month] = json.load(file)
        else:
            print(f"File '{month_file}' not found.")


    return last_6_months_contents
    # for month, contents in last_6_months_contents.items():
    #     print(month, ":")
    #     print(contents)
def last_month():
    # Path to the output_json folder
    output_json_folder = 'output_json'

    # Get the list of files in the output_json folder
    files = os.listdir(output_json_folder)
    
    # Sort the files by name (which contains the date) to find the latest month
    sorted_files = sorted(files, reverse=True)
    
    # Check if there are any files in the folder
    if sorted_files:
        # Get the latest file (which represents the current month)
        current_month_file = sorted_files[0]
        
        # Extract the month from the current month file name
        current_month = current_month_file.split('.')[0]
        
        # Construct the path to the JSON file for the last month
        last_month_date = (datetime.strptime(current_month, '%Y-%m-%d') - relativedelta(months=1)).strftime('%Y-%m-01')
        last_month_file = os.path.join(output_json_folder, f'{last_month_date}.json')
        
        # Check if the file exists
        if os.path.exists(last_month_file):
            # Read the contents of the JSON file for the last month
            with open(last_month_file, 'r') as file:
                last_month_data = json.load(file)

            return last_month_data
        else:
            print(f"File '{last_month_file}' not found.")
    else:
        print("No JSON files found in the output_json folder.")
        return None


