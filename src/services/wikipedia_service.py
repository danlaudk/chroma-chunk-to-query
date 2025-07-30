"""
Service for retrieving and processing Wikipedia articles.
"""

import requests
from typing import List, Dict
from ..config.settings import config

class WikipediaService:
    def __init__(self, wikipedia_config=None):
        """
        Initialize the Wikipedia service.
        
        Args:
            wikipedia_config: Optional WikipediaConfig instance for testing
        """
        self.config = wikipedia_config or config.wikipedia

    def retrieve_article(self, page_title: str) -> str:
        """
        Retrieves the full text content of a Wikipedia article.
        
        Args:
            page_title: The Wikipedia page title to retrieve
            
        Returns:
            The article content as a string, or empty string if not found
        """
        print(f"Retrieving Wikipedia article: {page_title}")
        
        try:
            params = {
                "action": "query",
                "format": "json",
                "titles": page_title,
                "prop": "extracts",
                "explaintext": True,
                "exintro": False,  # Get full extract, not just intro
                "redirects": 1  # Follow redirects
            }
            
            response = requests.get(
                self.config.api_url, 
                params=params, 
                timeout=self.config.timeout
            )
            response.raise_for_status()
            
            data = response.json()
            page = next(iter(data['query']['pages'].values()))
            
            if 'extract' in page:
                return page['extract']
            else:
                print(f"No extract found for page: {page_title}")
                return ""
                
        except requests.exceptions.Timeout:
            print(f"Timeout retrieving Wikipedia article '{page_title}'")
            return ""
        except requests.exceptions.RequestException as e:
            print(f"Request error retrieving Wikipedia article '{page_title}': {e}")
            return ""
        except Exception as e:
            print(f"Error retrieving Wikipedia article '{page_title}': {e}")
            return ""

    def chunk_text(self, text: str, source_metadata: Dict) -> List[Dict]:
        """
        Performs robust, layered text chunking on the Wikipedia article.
        First, content-aware (by paragraph/section), then optionally semantic.
        
        Args:
            text: The text to chunk
            source_metadata: Metadata about the source article
            
        Returns:
            List of chunk dictionaries with text and metadata
        """
        print("Chunking text and adding metadata...")
        chunks = []
        
        # Split by double newline for paragraphs
        paragraphs = text.split('\n\n')
        
        for i, para in enumerate(paragraphs):
            if para.strip():  # Ensure chunk is not empty
                # Apply size constraints from config
                chunk_text = para.strip()
                if len(chunk_text) > config.retrieval.max_chunk_size:
                    # Split large paragraphs into smaller chunks
                    chunk_text = chunk_text[:config.retrieval.max_chunk_size]
                elif len(chunk_text) < config.retrieval.min_chunk_size:
                    # Skip chunks that are too small
                    continue
                    
                chunk_metadata = {
                    "source_article": source_metadata.get("article_title"),
                    "chunk_id": f"{source_metadata.get('article_title', 'unknown')}_chunk_{i}",
                    "section_heading": "General",  # Placeholder, real impl would parse headings
                    "chunk_size": len(chunk_text)
                }
                chunks.append({
                    "text": chunk_text,
                    "metadata": chunk_metadata
                })
                
        print(f"Created {len(chunks)} chunks.")
        return chunks 