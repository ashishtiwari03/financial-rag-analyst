import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API keys from environment (NOT hardcoded)
os.environ["LLAMA_CLOUD_API_KEY"] = os.getenv("LLAMA_CLOUD_API_KEY")
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

from llama_parse import LlamaParse
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, Settings
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.llms.groq import Groq
from llama_index.embeddings.ollama import OllamaEmbedding
import chromadb

Settings.llm = Groq(model="llama-3.1-8b-instant")
Settings.embed_model = OllamaEmbedding(model_name="nomic-embed-text")
     
# --- MODEL SETUP ---
# After trying OpenAI (quota errors) and local Llama (RAM issues),
# settled on this hybrid approach - cloud for reasoning, local for embeddings
Settings.llm = Groq(model="llama-3.1-8b-instant")  # Free and fast!
Settings.embed_model = OllamaEmbedding(model_name="nomic-embed-text")

def load_and_index_data(file_path):
    """
    Parse PDF and store in vector DB
    Using LlamaParse because it preserves table structure - game changer!
    """
    # Setup parser
    parser = LlamaParse(result_type="markdown", verbose=True)
    file_extractor = {".pdf": parser}
    
    # Load the document
    documents = SimpleDirectoryReader(
        input_files=[file_path],
        file_extractor=file_extractor
    ).load_data()
    
    # DEBUG: Uncomment to see doc count
    # print(f"Loaded {len(documents)} document chunks")

    # Setup ChromaDB - persistent so we don't re-index every time
    db = chromadb.PersistentClient(path="./chroma_db")
    
    # NOTE: Using v3 after debugging that "table not found" issue
    # v1 and v2 had stale data problems
    chroma_collection = db.get_or_create_collection("finance_v3")
    
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # Index the documents
    index = VectorStoreIndex.from_documents(
        documents, 
        storage_context=storage_context
    )
    
    return index

def get_query_engine():
    """
    Create query engine from existing index
    """
    db = chromadb.PersistentClient(path="./chroma_db")
    chroma_collection = db.get_or_create_collection("finance_v3")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    
    index = VectorStoreIndex.from_vector_store(vector_store)
    
    # Retrieve top 10 chunks - found this works better for financial docs
    # than the default 3. Tables are often spread across pages.
    # TODO: Make this configurable? Might need different values for different doc types

    return index.as_query_engine(similarity_top_k=10)
