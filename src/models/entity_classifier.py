"""
DSPy-based entity classification model.
"""

import dspy
from typing import Tuple, List


class EntityClassificationSignature(dspy.Signature):
    """Signature for entity classification task.
    
    Given a term, its linked Wikipedia title, and retrieved chunks from the article,
    classify the entity type and provide an explanation for the classification.
    """
    
    # Input fields
    term: str = dspy.InputField(
        desc="The term to classify"
    )
    linked_wikipedia_title: str = dspy.InputField(
        desc="The linked Wikipedia article title"
    )
    retrieved_chunks: List[str] = dspy.InputField(
        desc="List of relevant text chunks from the Wikipedia article"
    )
    
    # Output fields
    entity_type: str = dspy.OutputField(
        desc="The classified entity type (e.g., 'PERSON', 'ORGANIZATION', 'LOCATION', 'CONCEPT', etc.)"
    )
    explanation: str = dspy.OutputField(
        desc="Explanation for why the entity was classified as this type, based on the provided context"
    )


class ClassifyEntityModule(dspy.Module):
    """Module for classifying the entity type using DSPy."""
    
    def __init__(self):
        super().__init__()
        # Use the proper Signature class instead of a string
        self.prog = dspy.ChainOfThought(EntityClassificationSignature)

    def forward(self, term: str, linked_wikipedia_title: str, retrieved_chunks: list) -> Tuple[str, str]:
        """
        Classify the entity and provide an explanation.
        
        Args:
            term: The term to classify
            linked_wikipedia_title: The linked Wikipedia article title
            retrieved_chunks: List of relevant text chunks from the article
            
        Returns:
            Tuple of (entity_type, explanation)
        """
        prediction = self.prog(
            term=term,
            linked_wikipedia_title=linked_wikipedia_title,
            retrieved_chunks=retrieved_chunks
        )
        return prediction.entity_type, prediction.explanation 