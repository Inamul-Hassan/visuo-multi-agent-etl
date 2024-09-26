import json
import os
import copy

from .tools import AbstractChat


# Will revist this later if going to implement structured response
'''
from typing_extensions import Annotated, TypedDict

class Source(TypedDict):
    """Identified Source data to map"""

    source_fields: Annotated[list[str], ..., "Identified field(s) from the source data schema to map to the target field"]
    logic: Annotated[str|None, ..., "Mapping logic/formula for the source field(s) if any"]
    
class Mapping(TypedDict):
    """Mapping of source data fields to target data field"""

    target_field: Annotated[str, ..., "Target field to map to"]
    source: Annotated[list[Source], ..., "Source data schema to map from"]
'''


class SchemaAnalyzerAgent:
    def __init__(self, llm: AbstractChat, target_schema_path: str, all_tables_path: str):
        self.mapping = {}
        self.model = llm
        self.target_schema_path = target_schema_path
        self.all_tables_path = all_tables_path
        self.target_schema = self.load_json(self.target_schema_path)
        self.all_tables = self.load_json(self.all_tables_path)
        self.fields_dict = self.parse_schema(schema=self.target_schema)
    
    @staticmethod
    def load_json(path: str) -> dict:
        """
        Load a JSON file from the given path.
        """
        try:
            with open(path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"File not found: {path}")
            return {}
        except json.JSONDecodeError:
            print(f"Invalid JSON file: {path}")
            return {}

        
    def parse_schema(self,schema:dict, parent_key:str ='', fields_dict:dict =None)->dict:
        """
        Recursively parse the JSON schema and collect field names and their details.
        """
        if fields_dict is None:
            fields_dict = {}

        if schema.get('type') == 'object' and 'properties' in schema:
            for key, value in schema['properties'].items():
                full_key = f"{parent_key}.{key}" if parent_key else key
                self.parse_schema(value, full_key, fields_dict)
        elif schema.get('type') == 'array' and 'items' in schema:
            # Handle arrays; traverse the items
            self.parse_schema(schema['items'], parent_key, fields_dict)
        else:
            # It's a field; store the field path and its details
            field_details = copy.deepcopy(schema)
            # Remove 'properties' and 'items' keys if they exist to avoid clutter
            field_details.pop('properties', None)
            field_details.pop('items', None)
            fields_dict[parent_key] = field_details

        return fields_dict
    
    def save_to_json(self, data: dict, path: str) -> None:
        """
        Save a dictionary to a JSON file at the given path.
        """
        try:
            with open(path, 'w') as file:
                json.dump(data, file, indent=3)
            print(f"Successfully saved JSON file at {path}")
        except Exception as e:
            print(f"Error saving JSON file: {e}")
    
    def prompt(self,prompt_type:int,target_field:str|None=None,target_details:dict|None=None)->str:
        '''
        Function takes in the prompt type and returns the required prompt template.
        prompt_type: int: Type of prompt to generate
        target_field[optional]: str: Target field name
        target_details[optional]: dict: Details of the target field
        
        prompt_type: 1 - Mapping prompt
        '''
        match prompt_type:
            case 1:
                chat_input = f"""
                An HVAC (Heating, Ventilation, and Air Conditioning) service company provides data integration services for various clients. Each client has unique data requirements and target schemas for their analytics platforms. But we have a consistent source data tables. Below are the tables and all the fields in them,
                <Tables and Fields>
                {self.all_tables}

                Now given a field from the client's unique target schema, you have to identify the most relevant field(s) from the above 'Tables and Fields' that map to the target field. For each mapping, provide a json object with:
                - Source Field Name(s)
                - Necessary Transformations (if any)
                - isDirect: True/False (if direct one-one mapping then True else Flase)

                Provide the output as a JSON object. And No Extra text.

                <Target Field>
                {target_field} - {target_details}
        """
        
        return chat_input
    
    def map_fields(self)->None:
        """
        Map each target field to its source field(s)
        """
        for target_field, target_details in self.fields_dict.items():
            chat_prompt = self.prompt(1,target_field,target_details)
            try:
                response = self.model.invoke(chat_prompt)
            except Exception as e:
                print(f"Error invoking model: {e}")
            try:
                response_dict = json.loads(response.split("```")[1].split("json")[1])
                self.mapping.update(response_dict)
            except Exception as e:
                print(f"Error Response is not in the expected format {response}: {e}")
                continue
        self.save_to_json(self.mapping, "main\data\intitial_mapping_generated_3.json")
        # Debug
        #print(self.mapping)