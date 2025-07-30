"""
Main service for orchestrating entity classification and Wikipedia matching process.
"""

from typing import Dict, Optional
import dspy

from .wikipedia_service import WikipediaService
from .chroma_service import ChromaService
from ..models.entity_classifier import ClassifyEntityModule
from ..models.llm_model import initialize_litellm_dspy

class EntityProcessor:
    def __init__(self):
        """Initialize services and configure DSPy."""
        self.wikipedia_service = WikipediaService()
        self.chroma_service = ChromaService()
        self.classifier = ClassifyEntityModule()
        
        # Configure DSPy with LiteLLM
        self.llm = initialize_litellm_dspy()

    def perform_entity_linking(self, term: str) -> Dict:
        """
        Placeholder for entity linking service.
        In a real implementation, this would call an external entity linking service.
        """
        # This is a mock implementation
        return {
            'wikipedia_page_title': term,
            'wikidata_id': 'Q12345',
            'is_unrelated': False
        }

    def process_entity(self, term: str) -> Dict:
        """
        Main function to orchestrate the entity classification and Wikipedia matching process.
        """
        print(f"\n--- Processing Term: '{term}' ---")

        # Step 1: Entity Linking
        entity_link_info = self.perform_entity_linking(term)
        linked_wikipedia_title = entity_link_info['wikipedia_page_title']
        wikidata_id = entity_link_info['wikidata_id']
        is_unrelated = entity_link_info['is_unrelated']

        if is_unrelated or not linked_wikipedia_title:
            print(f"Term '{term}' could not be confidently linked to a Wikipedia page.")
            return {
                "term": term,
                "entity_type": "unrelated",
                "explanation": f"The term '{term}' did not confidently link to a specific known entity in Wikipedia/Wikidata.",
                "matched_chunks": []
            }

        # Step 2: Retrieve Wikipedia Article
        article_content = self.wikipedia_service.retrieve_article(linked_wikipedia_title)
        if not article_content:
            print(f"Could not retrieve content for '{linked_wikipedia_title}'.")
            return {
                "term": term,
                "entity_type": "unrelated",
                "explanation": f"Wikipedia article for '{linked_wikipedia_title}' could not be retrieved.",
                "matched_chunks": []
            }

        # Step 3: Chunk Text
        processed_chunks = self.wikipedia_service.chunk_text(
            article_content,
            {"article_title": linked_wikipedia_title}
        )

        # Step 4: Index Chunks in Chroma
        self.chroma_service.index_chunks(processed_chunks)

        # Step 5: Query Chroma for Relevant Chunks
        relevant_chunks = self.chroma_service.query_chunks(term, linked_wikipedia_title)

        # Step 6: Classify Entity Type
        entity_type, explanation = self.classifier.forward(
            term=term,
            linked_wikipedia_title=linked_wikipedia_title,
            retrieved_chunks=[c["text"] for c in relevant_chunks]
        )

        print(f"\n--- Results for '{term}' ---")
        print(f"Linked Wikipedia Title: {linked_wikipedia_title}")
        print(f"Wikidata ID: {wikidata_id}")
        print(f"Classified Entity Type: {entity_type}")
        print(f"Classification Explanation: {explanation}")
        print(f"Number of Matched Chunks: {len(relevant_chunks)}")

        return {
            "term": term,
            "linked_wikipedia_title": linked_wikipedia_title,
            "wikidata_id": wikidata_id,
            "entity_type": entity_type,
            "explanation": explanation,
            "matched_chunks": relevant_chunks
        } 