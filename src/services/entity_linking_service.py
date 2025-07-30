"""
Service for performing entity linking to Wikipedia and Wikidata.
"""

from typing import Dict
import requests
from ..config.settings import config

class EntityLinkingService:
    """Service responsible for linking terms to Wikipedia pages and Wikidata entities."""
    
    def __init__(self, wikipedia_config=None):
        """
        Initialize the entity linking service.
        
        Args:
            wikipedia_config: Optional WikipediaConfig instance for testing
        """
        self.config = wikipedia_config or config.wikipedia

    def perform_entity_linking(self, term: str) -> Dict:
        """
        Perform entity linking for a given term.
        
        In a real implementation, this would call an external entity linking service
        like DBpedia Spotlight, TagMe, or a custom ML model. For now, this is a
        simplified implementation that attempts to find a Wikipedia page.
        
        Args:
            term: The term to link to an entity
            
        Returns:
            Dictionary containing linking information:
            - wikipedia_page_title: The linked Wikipedia page title
            - wikidata_id: The Wikidata entity ID
            - is_unrelated: Whether the term is unrelated to any known entity
        """
        try:
            # Try to find a Wikipedia page for the term
            wikipedia_title = self._find_wikipedia_page(term)
            
            if wikipedia_title:
                # In a real implementation, you would also get the Wikidata ID
                # from the Wikipedia page or a separate API call
                wikidata_id = self._get_wikidata_id(wikipedia_title)
                return {
                    'wikipedia_page_title': wikipedia_title,
                    'wikidata_id': wikidata_id,
                    'is_unrelated': False
                }
            else:
                return {
                    'wikipedia_page_title': None,
                    'wikidata_id': None,
                    'is_unrelated': True
                }
                
        except Exception as e:
            print(f"Error during entity linking for '{term}': {e}")
            return {
                'wikipedia_page_title': None,
                'wikidata_id': None,
                'is_unrelated': True
            }

    def _find_wikipedia_page(self, term: str) -> str:
        """
        Find a Wikipedia page for the given term.
        
        Args:
            term: The term to search for
            
        Returns:
            Wikipedia page title if found, None otherwise
        """
        try:
            params = {
                "action": "query",
                "format": "json",
                "list": "search",
                "srsearch": term,
                "srlimit": 1,
                "srnamespace": 0  # Main namespace only
            }
            
            response = requests.get(
                self.config.api_url, 
                params=params, 
                timeout=self.config.timeout
            )
            response.raise_for_status()
            
            data = response.json()
            if data['query']['search']:
                return data['query']['search'][0]['title']
            else:
                return None
                
        except Exception as e:
            print(f"Error searching Wikipedia for '{term}': {e}")
            return None

    def _get_wikidata_id(self, wikipedia_title: str) -> str:
        """
        Get the Wikidata ID for a Wikipedia page.
        
        Args:
            wikipedia_title: The Wikipedia page title
            
        Returns:
            Wikidata entity ID if found, placeholder otherwise
        """
        try:
            params = {
                "action": "query",
                "format": "json",
                "titles": wikipedia_title,
                "prop": "pageprops",
                "ppprop": "wikibase_item"
            }
            
            response = requests.get(
                self.config.api_url, 
                params=params, 
                timeout=self.config.timeout
            )
            response.raise_for_status()
            
            data = response.json()
            page = next(iter(data['query']['pages'].values()))
            
            if 'pageprops' in page and 'wikibase_item' in page['pageprops']:
                return page['pageprops']['wikibase_item']
            else:
                return 'Q12345'  # Placeholder ID
                
        except Exception as e:
            print(f"Error getting Wikidata ID for '{wikipedia_title}': {e}")
            return 'Q12345'  # Placeholder ID