"""
Configuration settings for the application.
"""
import os

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# LLM Settings
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
LLM_PROVIDER = "google"  # LiteLLM provider name
LLM_MODEL = "gemini/gemini-2.0-flash"  # Model name
LLM_TEMPERATURE = 0.1  # Lower temperature for more focused responses
LOCAL_LLM_MODEL = "gpt-4o-mini"

# Fallback Configuration
FALLBACK_PROVIDERS = [
    {"provider": "google", "model": "gemini/gemini-2.0-flash"},
    # Add more fallback models here if needed
    # {"provider": "anthropic", "model": "claude-2"},
    # {"provider": "openai", "model": "gpt-3.5-turbo"},
]

# ChromaDB Settings
CHROMA_PERSISTENCE_DIR = "./chroma_db"

# Embedding Model Settings
EMBEDDING_MODEL_NAME = "mixedbread-ai/deepset-mxbai-embed-de-large-v1"

# Wikipedia API Settings
WIKIPEDIA_API_URL = "https://en.wikipedia.org/w/api.php"

# Retrieval Settings
DEFAULT_CHUNK_RETRIEVAL_COUNT = 5

# Validate required environment variables
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY environment variable is not set") 