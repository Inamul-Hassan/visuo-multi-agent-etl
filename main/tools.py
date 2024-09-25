from abc import ABC, abstractmethod

from langchain_google_genai import ChatGoogleGenerativeAI

class AbstractChat(ABC):
    @abstractmethod
    def __init__(self, api_key: str, model: str):
        pass

    @abstractmethod
    def invoke(self, chat_input: str)->str:
        pass

class ChatGemini(AbstractChat):
    def __init__(self, api_key: str, model: str = "gemini-1.5-flash"):
        self.model = model
        self.api_key = api_key
        self.llm = ChatGoogleGenerativeAI(model=model, api_key=api_key)

    def invoke(self, chat_input: str)->str:
        response = self.llm.invoke(chat_input)
        return response.content