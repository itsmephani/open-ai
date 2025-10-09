from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

class FaissStore:
  _instance = None

  def __new__(cls, *args, **kwargs):
    if cls._instance is None:
      cls._instance = super().__new__(cls)
      load_dotenv()
      loader = PyPDFLoader("docs/ai_report_2025.pdf")
      documents = loader.load()
      print(f"Loaded {len(documents)} documents from the PDF.")

      text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
      docs = text_splitter.split_documents(documents)
      print(f"Split into {len(docs)} chunks of text.")

      embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
      try:
        cls._instance.library = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
        print("Loaded existing FAISS index.")
      except Exception as e:
        cls._instance.library = FAISS.from_documents(docs, embeddings)
        cls._instance.library.save_local("faiss_index")
        print("Created and saved FAISS index.")
    
    return cls._instance

  def search_index(self, query: str):
    return self.library.similarity_search_with_score(query, k=2)
