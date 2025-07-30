"""
Configuration settings for the application.
"""
import os
from typing import List, Dict
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@dataclass
class LLMConfig:
    """LLM configuration settings."""
    api_key: str
    provider: str = "google"
    model: str = "gemini/gemini-2.0-flash"
    temperature: float = 0.1
    max_tokens: int = 4000
    cache: bool = True

@dataclass
class ChromaConfig:
    """ChromaDB configuration settings."""
    persistence_dir: str = "./chroma_db"
    collection_name: str = "wikipedia_chunks"
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"

@dataclass
class WikipediaConfig:
    """Wikipedia API configuration settings."""
    api_url: str = "https://en.wikipedia.org/w/api.php"
    timeout: int = 30
    max_retries: int = 3

@dataclass
class RetrievalConfig:
    """Retrieval and processing configuration settings."""
    default_chunk_retrieval_count: int = 5
    max_chunk_size: int = 1000
    min_chunk_size: int = 50
    chunk_overlap: int = 100

@dataclass
class AppConfig:
    """Main application configuration."""
    environment: str
    debug: bool
    llm: LLMConfig
    chroma: ChromaConfig
    wikipedia: WikipediaConfig
    retrieval: RetrievalConfig

def get_config() -> AppConfig:
    """Get configuration based on environment."""
    environment = os.getenv('ENVIRONMENT', 'development')
    debug = os.getenv('DEBUG', 'false').lower() == 'true'
    
    # Environment-specific overrides
    if environment == 'production':
        chunk_retrieval_count = 10
        max_tokens = 8000
    elif environment == 'testing':
        chunk_retrieval_count = 3
        max_tokens = 1000
        debug = True
    else:  # development
        chunk_retrieval_count = 5
        max_tokens = 4000
    
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable is not set")
    
    return AppConfig(
        environment=environment,
        debug=debug,
        llm=LLMConfig(
            api_key=api_key,
            provider=os.getenv('LLM_PROVIDER', 'google'),
            model=os.getenv('LLM_MODEL', 'gemini/gemini-2.0-flash'),
            temperature=float(os.getenv('LLM_TEMPERATURE', '0.1')),
            max_tokens=max_tokens,
            cache=os.getenv('LLM_CACHE', 'true').lower() == 'true'
        ),
        chroma=ChromaConfig(
            persistence_dir=os.getenv('CHROMA_PERSISTENCE_DIR', './chroma_db'),
            collection_name=os.getenv('CHROMA_COLLECTION_NAME', 'wikipedia_chunks'),
            embedding_model=os.getenv('EMBEDDING_MODEL_NAME', 'sentence-transformers/all-MiniLM-L6-v2')
        ),
        wikipedia=WikipediaConfig(
            api_url=os.getenv('WIKIPEDIA_API_URL', 'https://en.wikipedia.org/w/api.php'),
            timeout=int(os.getenv('WIKIPEDIA_TIMEOUT', '30')),
            max_retries=int(os.getenv('WIKIPEDIA_MAX_RETRIES', '3'))
        ),
        retrieval=RetrievalConfig(
            default_chunk_retrieval_count=chunk_retrieval_count,
            max_chunk_size=int(os.getenv('MAX_CHUNK_SIZE', '1000')),
            min_chunk_size=int(os.getenv('MIN_CHUNK_SIZE', '50')),
            chunk_overlap=int(os.getenv('CHUNK_OVERLAP', '100'))
        )
    )

# Global configuration instance
config = get_config()

# Backward compatibility exports
GOOGLE_API_KEY = config.llm.api_key
LLM_PROVIDER = config.llm.provider
LLM_MODEL = config.llm.model
LLM_TEMPERATURE = config.llm.temperature
CHROMA_PERSISTENCE_DIR = config.chroma.persistence_dir
EMBEDDING_MODEL_NAME = config.chroma.embedding_model
WIKIPEDIA_API_URL = config.wikipedia.api_url
DEFAULT_CHUNK_RETRIEVAL_COUNT = config.retrieval.default_chunk_retrieval_count 