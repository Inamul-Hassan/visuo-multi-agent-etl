import os
from environs import Env
import json
env = Env()
env.read_env()

GEMINI = os.getenv("GEMINI")

from langchain_google_genai import ChatGoogleGenerativeAI

           
table_path = "visuo-ETL\main\data\\all_tables.json"
with open(table_path, 'r') as f:
            tables = json.load(f)
            
            
 
# Without strcutured response            
chat_input = f"""
An HVAC (Heating, Ventilation, and Air Conditioning) service company provides data integration services for various clients. Each client has unique data requirements and target schemas for their analytics platforms. But we have a consistent source data tables. Below are the tables and all the fields in them,
<Tables and Fields>
{tables}

Now given a field from the client's unique target schema, you have to identify the most relevant field(s) from the above 'Tables and Fields' that map to the target field. For each mapping, provide a json object with:
- Source Field Name(s)
- Necessary Transformations (if any)

Provide the output as a JSON object. And No Extra text.

<Target Field>
Target Field: customer_health.score' - 
'type': 'number', 
'minimum': 0, 
'maximum': 100, '
description': 'Overall health score of the customer based on various factors'
"""




llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", api_key=GEMINI)
response = llm.invoke(chat_input)
content = response.content

res = json.loads(content.split("```")[1].split("json")[1])
print(res)
print(type(res))
print(str(res))