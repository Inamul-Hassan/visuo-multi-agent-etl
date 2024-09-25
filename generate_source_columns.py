import os
import pandas as pd
import json

def get_csv_columns(file_path):
    # Check if the file exists and is a CSV
    if not os.path.isfile(file_path) or not file_path.endswith('.csv'):
        raise ValueError("Invalid file path or the file is not a CSV.")
    
    # Get the file name without the extension
    file_name = os.path.basename(file_path).replace('.csv', '')
    
    # Read the CSV file to get the columns
    df = pd.read_csv(file_path)
    columns_list = df.columns.tolist()
    
    # Return the dictionary with file name as key and columns as list
    return {file_name: columns_list}
  
def get_all_csv_files(directory_path):
    # Check if the directory exists
    if not os.path.isdir(directory_path):
        raise ValueError("Invalid directory path.")
    
    # List all files in the directory and filter for CSV files
    csv_files = [os.path.join(directory_path, file) for file in os.listdir(directory_path) if file.endswith('.csv')]
    
    return csv_files
  
def save_dict_to_json(data, output_path):
    with open(output_path, 'w') as json_file:
        json.dump(data, json_file, indent=2)

csv_directory = 'visuo-ETL/data/source_data/'
output_path = 'all_tables.json'
csv_files = get_all_csv_files(csv_directory)
all_tables = {}
for file_name in csv_files:
  print(file_name)
  all_tables.update(get_csv_columns(file_name))
  
save_dict_to_json(all_tables, output_path)
  
print(all_tables)
  

