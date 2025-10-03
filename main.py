from openai_client import OpenAIClient
from utils import upload_pdfs_and_create_vector_store

client = OpenAIClient().get_client()

print("Client initialized:", client)
  
def main():

  while True:
    query = input("Enter your question (or 'exit' to quit): ")
    # vector_store_details = create_vector_store("learn_open_ai_rag_responses_store")
    
    if query.lower() == 'create_vector_store':
      vector_store_details = upload_pdfs_and_create_vector_store()
      print(f"Vector store ready for queries. {vector_store_details}")   
      continue

    if query.lower() == 'exit':
      break
    
    print(f"Vector store id: {vector_store_details['id']}")
    response = client.responses.create(
      input= query,
      model="gpt-5-nano",
      tools=[{
        "type": "file_search",
        "vector_store_ids": [vector_store_details['id']],
        "max_num_results": 2
      }],
      # max_output_tokens=500,
    )
    # Extract annotations / filenames from the response in a defensive way.
    # Different SDK objects (like ResponseFileSearchToolCall) may expose
    # annotations/text directly or inside a .content list. Handle both.
    annotations = []
    file_search_text = None

    for out in getattr(response, "output", []) or []:
      # Case: item has a .content list (each element may have annotations/text)
      if hasattr(out, "content") and out.content:
        for c in out.content:
          if hasattr(c, "annotations") and c.annotations:
            annotations.extend(list(c.annotations))
          if hasattr(c, "text") and c.text:
            file_search_text = c.text
      else:
        # Case: the tool call object exposes annotations/text directly
        if hasattr(out, "annotations") and out.annotations:
          annotations.extend(list(out.annotations))
        if hasattr(out, "text") and out.text:
          file_search_text = out.text

    # Get top-k retrieved filenames (annotations may be objects or dict-like)
    retrieved_files = set()
    for a in annotations:
      # object-like
      if hasattr(a, "filename"):
        retrieved_files.add(getattr(a, "filename"))
      # dict-like
      elif isinstance(a, dict) and "filename" in a:
        retrieved_files.add(a["filename"])

    print(f'Files used: {retrieved_files}')
    print('Response:')
    if file_search_text:
      print(file_search_text)
    else:
      # Fallback to the aggregate output_text provided by the response
      print(getattr(response, "output_text", ""))
    
    print("\n-------------------------------------\n")

if __name__ == "__main__":
  main()
