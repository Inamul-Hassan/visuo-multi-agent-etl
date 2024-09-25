import os
from environs import Env


from .SchemaAnalyzerAgent import SchemaAnalyzerAgent
from .tools import ChatGemini

env = Env()
env.read_env()

gemini_model = ChatGemini(api_key=os.getenv("GEMINI")) 
si_agent = SchemaAnalyzerAgent(llm=gemini_model,
                               target_schema_path=os.getenv("TARGET_SCHEMA_PATH"),
                               all_tables_path=os.getenv("ALL_TABLES"))
si_agent.map_fields()




