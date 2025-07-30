"""
Main service for orchestrating entity classification and Wikipedia matching process.
"""

from typing import Dict, Optional
import dspy

from .wikipedia_service import WikipediaService
from .chroma_service import ChromaService
from .entity_linking_service import EntityLinkingService
from ..models.entity_classifier import ClassifyEntityModule
from ..models.llm_model import initialize_litellm_dspy

class EntityProcessor:
    def __init__(self, 
                 wikipedia_service: Optional[WikipediaService] = None,
                 chroma_service: Optional[ChromaService] = None,
                 entity_linking_service: Optional[EntityLinkingService] = None,
                 classifier: Optional[ClassifyEntityModule] = None,
                 llm: Optional[dspy.LM] = None):
        """
        Initialize services with dependency injection for better testability and efficiency.
        
        Args:
            wikipedia_service: Wikipedia service instance (created if None)
            chroma_service: ChromaDB service instance (created if None)
            entity_linking_service: Entity linking service instance (created if None)
            classifier: Entity classifier instance (created if None)
            llm: DSPy LM instance (created if None)
        """
        # Use dependency injection or create instances if not provided
        self.wikipedia_service = wikipedia_service or WikipediaService()
        self.chroma_service = chroma_service or ChromaService()
        self.entity_linking_service = entity_linking_service or EntityLinkingService()
        self.classifier = classifier or ClassifyEntityModule()
        
        # Configure DSPy with LiteLLM if not provided
        if llm is None:
            self.llm = initialize_litellm_dspy()
        else:
            self.llm = llm
            dspy.configure(lm=self.llm)

    def process_entity(self, term: str) -> Dict:
        """
        Main function to orchestrate the entity classification and Wikipedia matching process.
        """
        print(f"\n--- Processing Term: '{term}' ---")

        # Step 1: Entity Linking
        entity_link_info = self.entity_linking_service.perform_entity_linking(term)
        linked_wikipedia_title = entity_link_info['wikipedia_page_title']
        wikidata_id = entity_link_info['wikidata_id']
        is_unrelated = entity_link_info['is_unrelated']

        if is_unrelated or not linked_wikipedia_title:
            print(f"Term '{term}' could not be confidently linked to a Wikipedia page.")
            return self._create_unrelated_result(term, f"The term '{term}' did not confidently link to a specific known entity in Wikipedia/Wikidata.")

        # Step 2: Retrieve Wikipedia Article
        article_content = self.wikipedia_service.retrieve_article(linked_wikipedia_title)
        if not article_content:
            print(f"Could not retrieve content for '{linked_wikipedia_title}'.")
            return self._create_unrelated_result(term, f"Wikipedia article for '{linked_wikipedia_title}' could not be retrieved.")

        # Step 3: Process and Index Content
        processed_chunks = self.wikipedia_service.chunk_text(
            article_content,
            {"article_title": linked_wikipedia_title}
        )
        self.chroma_service.index_chunks(processed_chunks)

        # Step 4: Query and Classify
        relevant_chunks = self.chroma_service.query_chunks(term, linked_wikipedia_title)
        entity_type, explanation = self.classifier.forward(
            term=term,
            linked_wikipedia_title=linked_wikipedia_title,
            retrieved_chunks=[c["text"] for c in relevant_chunks]
        )

        return self._create_success_result(
            term, linked_wikipedia_title, wikidata_id, 
            entity_type, explanation, relevant_chunks
        )

    def _create_unrelated_result(self, term: str, explanation: str) -> Dict:
        """Create a result for unrelated terms."""
        return {
            "term": term,
            "entity_type": "unrelated",
            "explanation": explanation,
            "matched_chunks": []
        }

    def _create_success_result(self, term: str, linked_wikipedia_title: str, 
                              wikidata_id: str, entity_type: str, 
                              explanation: str, matched_chunks: list) -> Dict:
        """Create a successful result."""
        print(f"\n--- Results for '{term}' ---")
        print(f"Linked Wikipedia Title: {linked_wikipedia_title}")
        print(f"Wikidata ID: {wikidata_id}")
        print(f"Classified Entity Type: {entity_type}")
        print(f"Classification Explanation: {explanation}")
        print(f"Number of Matched Chunks: {len(matched_chunks)}")

        return {
            "term": term,
            "linked_wikipedia_title": linked_wikipedia_title,
            "wikidata_id": wikidata_id,
            "entity_type": entity_type,
            "explanation": explanation,
            "matched_chunks": matched_chunks
        } 