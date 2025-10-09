from openai import OpenAI
from dotenv import load_dotenv

class OpenAIClient:
  _instance = None

  def __new__(cls, *args, **kwargs):
    if cls._instance is None:
      cls._instance = super().__new__(cls)
      load_dotenv()
      cls._instance.client = OpenAI()
    
    return cls._instance

  def get_client(self):
    return self.client
