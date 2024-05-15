import pandas as pd
import yaml
import re
import csv
import os
from datetime import datetime
import json

def process_excel(excel_name,yaml_dir):
    # Read the Excel file
    df = pd.read_excel(excel_name)

    # Write the DataFrame to a CSV file
    df.to_csv('output_file.csv', index=False)

    processed = set()
    misc = set()


    def extract_month():
        # Define a regular expression pattern to match the date format (dd/mm/yyyy)
        with open("output_file.csv", 'r') as file:
            text = file.read()
        pattern = r'(\d{2})/(\d{2})/(\d{4})'
        
        # Search for the date pattern in the text
        match = re.search(pattern, text)
        
        if match:
            # Extract the year and month parts from the matched date
            year = int(match.group(3))
            month = int(match.group(2))
            
            # Format the date as "YYYY-MM-01"
            formatted_date = f"{year:04d}-{month:02d}-01"
            return formatted_date
        else:
            return None




    def get_final_values():

        # Initialize text_lines variable to store the contents of the CSV file
        text_lines = []

        # Read the contents of the CSV file and store them in text_lines
        with open('output_file.csv', 'r') as csv_file:
            for line in csv_file:
                text_lines.append(line.strip())

        # Initialize variables to store extracted values
        opening_balance = None
        debits = None
        credits = None
        closing_balance = None

        # Iterate through each line of the text
        for i in range(len(text_lines) - 1):
            line = text_lines[i]
            next_line = text_lines[i + 1]

            # Check if the current line contains the required labels
            if "Opening Balance" in line and "Debits" in line and "Credits" in line and "Closing Bal" in line:
                # Extract numeric values from the next line
                values = re.findall(r'[\d.]+', next_line)
                
                # Assign values to variables
                if len(values) >= 4:
                    opening_balance = values[0]
                    debits = values[1]
                    credits = values[2]
                    closing_balance = values[3]
                
                # Break the loop once the values are extracted
                break


        return {
            "Opening Balance": opening_balance,
            "Debits": debits,
            "Credits": credits,
            "Closing Balance": closing_balance
        }



    def process_shitless():
        misc_sum = 0
        with open('output_file.csv', 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for line in csv_reader:
                if line[1] not in processed:
                    if line[1]:
                    
                    
                        try:
                            value = float(line[4].replace(',', ''))

                            misc_comb = f"{line[1]}::{line[4]}"
                            misc.add(misc_comb)

                        except Exception as e:
                            value = 0
                    
                        # Add the value to the total sum
                        misc_sum += value
        return misc_sum

    def process_shit(yaml_file):
        # Read YAML file
        json_data = {}
        with open(yaml_file, 'r') as file:
            yaml_data = yaml.safe_load(file)

        # Initialize sum
        total_sum = 0

        # Open the CSV file containing the data
        with open('output_file.csv', 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            
            
            # Iterate through each line in the CSV file
            for line in csv_reader:
                # Check if any of the regex patterns match in the line
                for regex_pattern in yaml_data['regex']:
                    if re.search(regex_pattern, line[1]):
                        # Extract the fourth comma-separated element and convert it to float
                        processed.add(line[1])
                        try:
                            value = float(line[4].replace(',', ''))
                        except Exception as e:
                            value = 0
                    
                        # Add the value to the total sum
                        total_sum += value
                        break  # Break the loop if a match is found to avoid counting the same line multiple times

        for category, regex in yaml_data.items():
            if category != 'regex':
                total_sum = round(total_sum, 2)
                category = yaml_data['category']
                json_data[category] = total_sum

        return json_data

    def process_all_yaml_files(directory):
        files = os.listdir(directory)
        combined_json = {}
        yaml_files = [file for file in files if file.endswith('.yaml')]
        total_income = 0
        # Iterate over each .yaml file
        for yaml_file in yaml_files:
            # Generate the full path to the .yaml file
            yaml_path = os.path.join(directory, yaml_file)
            
            # Call the process_shit function for the current .yaml file
            new_income = process_shit(yaml_path)
            combined_json.update(new_income)

            

        return combined_json



    directory = yaml_dir

    # Call the function to process all .yaml files in the directory


    category_json = process_all_yaml_files(directory)
    misc_t = process_shitless()
    category_json["Miscellaneous"] = float(misc_t)


    given_list = list(misc)

    # Create JSON object with the list
    json_data = json.dumps({'Miscellaneous': given_list}, indent=4)




    # {"Month": "April",  Get current month
    # "Expenses": {print(f"{yaml_data['category']}: {total_sum}")
    #   "Food": "510", 
    #   "Maintenance": "32",
    #   "Rent": "34",
    #   "Entertainment": "3213",
    #   "Loans": "23", 
    #   "Savings": "231", 
    #   "Healthcare": "132", 
    #   "Travel": "21", 
    #   "Fuel": "23", 
    #   "Subscriptions": "132", 
    #   "Miscellaneous": "123" misc_t
    #   },
    #   "Credit": "3232",    get_final_values
    #   "Debit": "232",  get_final_values
    #   "Zerodha": "423", will set later
    #   "Dividends": "324", will set later
    #   "Opening balance": "3232", get_final_values
    #   "Closing Balance": "4224" get_final_values
    #  }
    current_month = extract_month()
    output_data = {
        "Month": current_month,
        "Expenses":category_json,
        "Miscellaneous": misc_t,
        "Credit": get_final_values()["Credits"],
        "Debit": get_final_values()["Debits"],
        "Opening Balance": get_final_values()["Opening Balance"],
        "Closing Balance": get_final_values()["Closing Balance"]
    }
    output_data["Misc_set"] = json.loads(json_data)
    return output_data