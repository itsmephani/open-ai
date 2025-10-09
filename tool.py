import urllib.request
import urllib.parse
import json
from faiss_store import FaissStore

store = FaissStore()

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
          "score": score
        })
      
      return {
        "success": True,
        "results": formatted_results
      }
    except Exception as e:
        return {"success": False, "error": str(e)}
