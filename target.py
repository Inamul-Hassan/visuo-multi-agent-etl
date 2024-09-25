import json
import copy

def parse_schema(schema, parent_key='', fields_dict=None):
    """
    Recursively parse the JSON schema and collect field names and their details.
    """
    if fields_dict is None:
        fields_dict = {}

    if schema.get('type') == 'object' and 'properties' in schema:
        for key, value in schema['properties'].items():
            full_key = f"{parent_key}.{key}" if parent_key else key
            parse_schema(value, full_key, fields_dict)
    elif schema.get('type') == 'array' and 'items' in schema:
        # Handle arrays; traverse the items
        parse_schema(schema['items'], parent_key, fields_dict)
    else:
        # It's a field; store the field path and its details
        field_details = copy.deepcopy(schema)
        # Remove 'properties' and 'items' keys if they exist to avoid clutter
        field_details.pop('properties', None)
        field_details.pop('items', None)
        fields_dict[parent_key] = field_details

    return fields_dict

def main():
    # Load the JSON schema from a file
    with open('visuo-ETL\main\data\\target_schema\sample_target_schema.json', 'r') as file:
        json_schema = json.load(file)

    fields_dict = parse_schema(json_schema)
    print(fields_dict)
    # Now fields_dict contains the field names as keys and their details as values
    # You can use fields_dict as needed; for demonstration, we'll print it
    #print(json.dumps(fields_dict, indent=2))

if __name__ == "__main__":
    main()
