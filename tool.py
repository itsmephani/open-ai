import urllib.request
import urllib.parse
import json

from dotenv import load_dotenv
from faiss_store import FaissStore
from file_search_tool.openai_client import OpenAIClient

load_dotenv()
store = FaissStore()
client = OpenAIClient().get_client()
tools = [
  {
    "type": "function",
    "name": "get_current_weather",
    "description": "Get weather for the provided city.",
    "parameters": {
        "type": "object",
        "properties": {
            "city": {
              "type": "string",
              "description": "City name e.g. Hyderabad, India",
            },
        },
        "required": ["city"],
        "additionalProperties": False,
    },
    "strict": True,
  },
  {
    "type": "function",
    "name": "latest_ai_news_report",
    "description": """
      Get latest questions, news, trends and reports related to AI, Artificial Intelligence, ML, Machine Learning.
      Use this to answer questions related to latest AI news and reports.
    """,
    "parameters": {
        "type": "object",
        "properties": {
            "query": {
              "type": "string",
              "description": "Question related to latest AI news and reports.",
            },
        },
        "required": ["query"],
        "additionalProperties": False,
    },
    "strict": True, 
  },
  {
    "type": "function",
    "name": "search_web",
    "description": """
      Use this to search web and get latest information.
      INSTRUCTION: DON'T USE FOR AI RELATED NEWS.
    """,
    "parameters": {
        "type": "object",
        "properties": {
            "query": {
              "type": "string",
              "description": "Question related to latest AI news and reports.",
            },
        },
        "required": ["query"],
        "additionalProperties": False,
    },
    "strict": True, 
  }
]

def get_current_weather(city: str) -> dict:
  """Fetch current weather for a city using the free wttr.in JSON API.
  Returns a dict with keys: success (bool), location, temperature_C, temperature_F, condition, humidity, wind_kph, raw (original JSON).
  If an error occurs returns {'success': False, 'error': '...'}
  """
  
  try:
    if not city or not str(city).strip():
        return {"success": False, "error": "Empty city name"}
    encoded = urllib.parse.quote(str(city))
    url = f"https://wttr.in/{encoded}?format=j1"
    with urllib.request.urlopen(url, timeout=10) as resp:
        if getattr(resp, 'status', 200) != 200:
            return {"success": False, "error": f"HTTP {getattr(resp, 'status', 'unknown')}"}
        data = json.load(resp)
    current = data.get('current_condition', [{}])[0]
    nearest = data.get('nearest_area', [{}])[0]
    temp_C = current.get('temp_C')
    temp_F = current.get('temp_F')
    condition = None
    if current.get('weatherDesc'):
        condition = current.get('weatherDesc')[0].get('value')
    humidity = current.get('humidity')
    wind_kph = current.get('windspeedKmph')
    area_name = None
    if nearest.get('areaName'):
        area_name = nearest.get('areaName')[0].get('value')
    return {
        "success": True,
        "location": area_name or city,
        "temperature_C": temp_C,
        "temperature_F": temp_F,
        "condition": condition,
        "humidity": humidity,
        "wind_kph": wind_kph,
        "raw": data,
    }
  except Exception as e:
      return {"success": False, "error": str(e)}
  
def get_latest_ai_news_report(query: str):
    """Fetch latest AI news and reports from the FAISS index."""
    try:
      results = store.search_index(query)
      formatted_results = []
      for doc, score in results:
        formatted_results.append({
          "page_content": doc.page_content,
          "metadata": doc.metadata,
          "score": score.item()
        })
      
      return {
        "success": True,
        "results": formatted_results
      }
    except Exception as e:
        return {"success": False, "error": str(e)}

def search_web(query: str):
    """Fetch latest information from web."""
    try:
      response = client.responses.create(
        model="gpt-5-nano",
        tools=[{"type": "web_search"}],
        input=query
      )
      
      return {
        "success": True,
        "results": response.output_text
      }
    except Exception as e:
        return {"success": False, "error": str(e)}
