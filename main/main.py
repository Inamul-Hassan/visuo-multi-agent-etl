import os

from .SchemaAnalyzerAgent import SchemaAnalyzerAgent
from .tools import ChatGemini

gemini_model = ChatGemini(api_key=os.getenv("GEMINI")) 
si_agent = SchemaAnalyzerAgent(llm=gemini_model)
si_agent.map_fields()




