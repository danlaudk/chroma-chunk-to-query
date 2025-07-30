"""
Service for retrieving and processing Wikipedia articles.
"""

import requests
from typing import List, Dict
from ..config.settings import WIKIPEDIA_API_URL

class WikipediaService:
    def retrieve_article(self, page_title: str) -> str:
        """
        Retrieves the full text content of a Wikipedia article.
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
            
            response = requests.get(WIKIPEDIA_API_URL, params=params)
            data = response.json()
            page = next(iter(data['query']['pages'].values()))
            
            if 'extract' in page:
                return page['extract']
            else:
                print(f"No extract found for page: {page_title}")
                return ""
                
        except Exception as e:
            print(f"Error retrieving Wikipedia article '{page_title}': {e}")
            return ""

    def chunk_text(self, text: str, source_metadata: Dict) -> List[Dict]:
        """
        Performs robust, layered text chunking on the Wikipedia article.
        First, content-aware (by paragraph/section), then optionally semantic.
        """
        print("Chunking text and adding metadata...")
        chunks = []
        
        # Split by double newline for paragraphs
        paragraphs = text.split('\n\n')
        
        for i, para in enumerate(paragraphs):
            if para.strip():  # Ensure chunk is not empty
                chunk_metadata = {
                    "source_article": source_metadata.get("article_title"),
                    "chunk_id": f"{source_metadata.get('article_title', 'unknown')}_chunk_{i}",
                    "section_heading": "General"  # Placeholder, real impl would parse headings
                }
                chunks.append({
                    "text": para.strip(),
                    "metadata": chunk_metadata
                })
                
        print(f"Created {len(chunks)} chunks.")
        return chunks 