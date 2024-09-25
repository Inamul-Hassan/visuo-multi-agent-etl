import os
from environs import Env
env = Env()
env.read_env()

OPENAI_KEY = os.getenv("OPENAI_KEY")

prompts: dict = {
  "system_prompt": "You are a data analyst.",
}

from pydantic import BaseModel

'''
# TypedDict
class Source(TypedDict):
    """Identified Source data to map"""

    source_fields: Annotated[list[str], ..., "Identified field/s from the source data schema to map to the target field"]
    logic: Annotated[str|None, ..., "Mapping logic/formula for the source field/s if any"]
    
class Mapping(TypedDict):
    """Mapping of source data fields to target data field"""

    target_field: Annotated[str, ..., "Target field to map to"]
    source: Annotated[list[Source], ..., "Source data schema to map from"]
'''

# TypedDict
class Source(BaseModel):
    """Identified Source data to map"""

    source_fields:list[str]
    logic: str | None
    
class Mapping(BaseModel):
    """Mapping of source data fields to target data field"""

    target_field: str
    source: list[Source]
    

    
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import json

def call_model(system_prompt: str, user_prompt: str):
  
    llm = ChatOpenAI(model="gpt-4o-mini",api_key=OPENAI_KEY)
    structured_llm = llm.with_structured_output(Mapping)
    prompt = ChatPromptTemplate.from_messages([("system", system_prompt), ("human", "{input}")])
    few_shot_structured_llm = prompt | structured_llm
    response = few_shot_structured_llm.invoke(user_prompt)

    return response
  
def call_o_model(system_prompt: str, user_prompt: str):
  from openai import OpenAI
  client = OpenAI(api_key=OPENAI_KEY)

  response = client.chat.completions.create(
    model="gpt-4o-mini-2024-07-18",
    messages=[
      {"role": "system", "content": f"{system_prompt}"},
      {"role": "user", "content": f"{user_prompt}"},
    ]

  )
  print(response)
  return response
  
target_schema_path =  "visuo-ETL\\target_schema\\sample_target_schema.json"
with open(target_schema_path, 'r') as f:
            target_schema = json.load(f)

source_schema_path = "visuo-ETL\source_schema\invoices_schema.json"
with open(source_schema_path, 'r') as f:
            source_schema = json.load(f)
            
            
# With strcutured response
chat_input = f"""
An HVAC (Heating, Ventilation, and Air Conditioning) service company provides data integration services for various clients. Each client has unique data requirements and target schemas for their analytics platforms. But we have a consistent source data tables. Below are the tables,
<Tables>
1. customers 
2. contracts
3. equipment.
4. invoices
5. maintenance 
6. plants 
7. service_requests 
8. technicians 

Give the source data schema and target schema, Identify the most relevant field(s) in the source data schema that map to the target field. 

"""
 
# Without strcutured response            
chat_input = f"""
An HVAC (Heating, Ventilation, and Air Conditioning) service company provides data integration services for various clients. Each client has unique data requirements and target schemas for their analytics platforms. But we have a consistent source data tables. Below are the tables,
<Tables>
1. customers 
2. contracts
3. equipment.
4. invoices
5. maintenance 
6. plants 
7. service_requests 
8. technicians 

Now given the client's unique target schema, you have to map the source data fields to the target data fields. But I will provide only one source schema at a time, Identify the most relevant field(s) in the source data schema that map to the target field. For each mapping, provide:
- Source Field Name(s)
- Necessary Transformations (if any)
- Any Data Type Conversions
- Notes on Data Quality or Potential Issues

Provide the output as a JSON object. And No Extra text.

<Target Schema in JSON>
{target_schema}

<Source Data Schema in JSON>
{source_schema}
"""


response = call_o_model(prompts["first_prompt"],chat_input)

event = response.choices[0].message.content

print(event)


import json

def fetch_source_data(tables: list[str])->dict:
    """
    Provided a list of tables, fetches all the columns in the tables and returns a dictionary with the table name as the key and the columns as the value.
    
    Args:
    tables: list[str]: A list of tables
    return: dict: table_name: columns
    """
    for table in tables:
      try:
        source_schema_path = f"visuo-ETL\source_schema\{table}_schema.json"
        with open(source_schema_path, 'r') as f:
            source_schema = json.load(f)
        source_schema = dict(source_schema)
        print(source_schema)
        # convert json to dict
        source_schema
      except Exception as e:
        print(e)
        
        pass
      
    pass
  
fetch_source_data(["invoices", "customers", "contracts"])
