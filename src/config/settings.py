"""
Configuration settings for the application.
"""
import os

from dotenv import load_dotenv

# Load environment variables
load_dotenv()



# ChromaDB Settings
CHROMA_PERSISTENCE_DIR = "./chroma_db"

# Embedding Model Settings
EMBEDDING_MODEL_NAME = "mixedbread-ai/deepset-mxbai-embed-de-large-v1"

# Wikipedia API Settings
WIKIPEDIA_API_URL = "https://en.wikipedia.org/w/api.php"

# Retrieval Settings
DEFAULT_CHUNK_RETRIEVAL_COUNT = 5
