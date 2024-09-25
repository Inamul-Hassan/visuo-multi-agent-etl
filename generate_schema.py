import pandas as pd
import json
import os
from environs import Env
env = Env()
env.read_env()

# Function to generate field information for schema
def generate_field_info(df):
    """Generate descriptions and constraints based on the data available in the dataframe."""
    field_info = []
    for column in df.columns:
        col_data = df[column]
        unique_count = col_data.nunique()
        null_count = col_data.isnull().sum()
        
        # Basic description based on column name and type
        description = f"This field represents the {column.replace('_', ' ')}."
        
        # Data type constraint
        data_type = str(col_data.dtype)
        constraints = {
            "type": data_type,
            "unique_values": int(unique_count),
            "missing_values": int(null_count)
        }
        
        # Additional constraints for certain data types
        if data_type == "object":
            max_length = col_data.str.len().max()
            constraints["max_length"] = int(max_length) if pd.notnull(max_length) else None
        elif data_type in ["int64", "float64"]:
            min_value = col_data.min()
            max_value = col_data.max()
            constraints["min_value"] = float(min_value) if pd.notnull(min_value) else None
            constraints["max_value"] = float(max_value) if pd.notnull(max_value) else None
        
        # Add field info
        field_info.append({
            "Column Name": column,
            "Data Type": data_type,
            "Description": description,
            "Constraints": constraints
        })
    
    return field_info

# Directory containing the CSV files
csv_directory = 'visuo-ETL\source_data'
target_directory = 'visuo-ETL\generated_schema'

# Initialize dictionary to hold schemas for all CSV files
detailed_schemas = {}

# Iterate over all files in the directory
for file_name in os.listdir(csv_directory):
    if file_name.endswith('.csv'):
        # Create a name for the dataframe by removing the .csv extension
        df_name = os.path.splitext(file_name)[0]
        
        # Load the CSV into a dataframe
        file_path = os.path.join(csv_directory, file_name)
        df = pd.read_csv(file_path)
        
        # Generate the schema for the dataframe and store it in the dictionary
        detailed_schemas[df_name] = generate_field_info(df)

# Convert the detailed schema to JSON format
detailed_schemas_json = json.dumps(detailed_schemas, indent=4)

# Save the detailed schema to a single JSON file
schema_file_path = os.path.join(target_directory, 'hvac_detailed_schema.json')
with open(schema_file_path, 'w') as file:
    file.write(detailed_schemas_json)

# Function to save each schema separately
def save_schema_to_file(schema, file_name):
    file_path = os.path.join(target_directory, f'{file_name}.json')
    with open(file_path, 'w') as file:
        json.dump(schema, file, indent=4)
    return file_path

# Save each schema to a separate file
for df_name, schema in detailed_schemas.items():
    save_schema_to_file(schema, f'{df_name}_schema')
