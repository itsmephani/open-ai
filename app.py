import json
import os
import uuid

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from openai_client import OpenAIClient
from dotenv import load_dotenv
from tool import tools, get_current_weather, get_latest_ai_news_report, search_web

# Initialize OpenAI client and vector store
load_dotenv()
client = OpenAIClient().get_client()
auth_token = os.getenv("RENDER_OPEN_AI_AUTH_TOKEN") or "changeme"

class Query(BaseModel):
  question: str
  auth_token: str
  session_id: str = None

input_store = {}

def chatbot(query: Query):
  if auth_token == "changeme" or query.auth_token != auth_token:
    return {"error": "Unauthorized"}, 401
  
  sources = list([])
  tools_used = list([])
  session_id = query.session_id or uuid.uuid4().hex
  input_store.setdefault(session_id, [])
  input_list = input_store.get(session_id, [])
  input_list.append({"role": "user", "content": query.question})

  print(f"Received question: {query.question}")

  
  response = get_responses(input_list)
  print(f"Response: {response}")
  input_list += response.output

  for item in response.output:
    if item.type == "function_call":
      print(f"Function call: {item.name} with arguments {item.arguments}")
      if item.name == "get_current_weather":
        weather_report = get_current_weather(**json.loads(item.arguments))
        tools_used.append(item.name)
        input_list.append({
          "type": "function_call_output",
          "call_id": item.call_id,
          "output": json.dumps(weather_report)
        })
        response = get_responses(input_list)
      if item.name == "latest_ai_news_report":
        news = get_latest_ai_news_report(**json.loads(item.arguments))
        tools_used.append(item.name)
        sources += [ f"{res["metadata"].get("source")}#{res["metadata"].get("page_label")}" for res in news.get("results", []) if res["metadata"].get("source")]
        input_list.append({
          "type": "function_call_output",
          "call_id": item.call_id,
          "output": json.dumps(news)
        })
        response = get_responses(input_list)
      if item.name == "search_web":
        news = search_web(**json.loads(item.arguments))
        tools_used.append(item.name)
        
        input_list.append({
          "type": "function_call_output",
          "call_id": item.call_id,
          "output": json.dumps(news)
        })
        response = get_responses(input_list)

  return {
    "answer": response.output_text,
    "sources": sources,
    "tools_used": tools_used,
    "session_id": session_id,
  }

def get_responses(input_list, instructions="You are a helpful AI assistant. Use the provided tools when needed to answer the question."):
  return client.responses.create(
    instructions= instructions,
    input=input_list,
    model="gpt-5-nano",
    tools=tools,
    tool_choice="auto",
    # store=False
    # max_output_tokens=1000,
  )

if __name__ == "__main__":
  while True:
    question = input("Enter your question: ")
    if question.lower() in ["exit", "quit"]:
      break
    
    session_id = uuid.uuid4().hex
    response = chatbot(Query(question=question, auth_token=auth_token, session_id=session_id))
    print(f"Response{':'*32}")
    print(response)
    print("="*40)
