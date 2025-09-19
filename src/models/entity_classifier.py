"""
DSPy-based entity classification model with Pydantic validation.
"""

import dspy
from typing import Tuple, List, Literal
from pydantic import BaseModel, Field, ValidationError
from enum import Enum


class EntityType(str, Enum):
    """Enumeration of allowed entity types."""
    PERSON = "PERSON"
    ORGANIZATION = "ORGANIZATION"
    LOCATION = "LOCATION"
    CONCEPT = "CONCEPT"
    EVENT = "EVENT"
    WORK = "WORK"  # Books, movies, songs, etc.
    TECHNOLOGY = "TECHNOLOGY"
    SCIENTIFIC_CONCEPT = "SCIENTIFIC_CONCEPT"
    PHILOSOPHICAL_CONCEPT = "PHILOSOPHICAL_CONCEPT"
    POLITICAL_CONCEPT = "POLITICAL_CONCEPT"
    UNKNOWN = "UNKNOWN"


class EntityClassificationResponse(BaseModel):
    """Pydantic model for validating LLM response structure."""
    entity_type: EntityType = Field(
        description="The classified entity type from the predefined list"
    )
    explanation: str = Field(
        min_length=10,
        max_length=1000,
        description="Explanation for why the entity was classified as this type"
    )


class EntityClassificationSignature(dspy.Signature):
    """Signature for entity classification task with restricted entity types.
    
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
    
    # Output fields with restricted entity types
    entity_type: Literal[
        "PERSON", "ORGANIZATION", "LOCATION", "CONCEPT", "EVENT", 
        "WORK", "TECHNOLOGY", "SCIENTIFIC_CONCEPT", "PHILOSOPHICAL_CONCEPT", 
        "POLITICAL_CONCEPT", "UNKNOWN"
    ] = dspy.OutputField(
        desc="The classified entity type. Must be one of: PERSON, ORGANIZATION, LOCATION, CONCEPT, EVENT, WORK, TECHNOLOGY, SCIENTIFIC_CONCEPT, PHILOSOPHICAL_CONCEPT, POLITICAL_CONCEPT, UNKNOWN"
    )
    explanation: str = dspy.OutputField(
        desc="Explanation for why the entity was classified as this type, based on the provided context (10-1000 characters)"
    )


class ClassifyEntityModule(dspy.Module):
    """Module for classifying the entity type using DSPy with Pydantic validation."""
    
    def __init__(self):
        super().__init__()
        # Use the proper Signature class with restricted entity types
        self.prog = dspy.ChainOfThought(EntityClassificationSignature)

    def _validate_llm_response(self, entity_type: str, explanation: str) -> Tuple[str, str]:
        """
        Validate LLM response using Pydantic.
        
        Args:
            entity_type: Raw entity type from LLM
            explanation: Raw explanation from LLM
            
        Returns:
            Tuple of (validated_entity_type, validated_explanation)
            
        Raises:
            ValidationError: If the response doesn't meet validation criteria
        """
        try:
            # Create response object for validation
            response = EntityClassificationResponse(
                entity_type=entity_type,
                explanation=explanation
            )
            return response.entity_type.value, response.explanation
            
        except ValidationError as e:
            # Try to fix common issues
            fixed_entity_type = self._fix_entity_type(entity_type)
            fixed_explanation = self._fix_explanation(explanation)
            
            try:
                response = EntityClassificationResponse(
                    entity_type=fixed_entity_type,
                    explanation=fixed_explanation
                )
                return response.entity_type.value, response.explanation
            except ValidationError:
                # If still invalid, return UNKNOWN with error message
                return "UNKNOWN", f"Failed to validate LLM response. Original entity_type: '{entity_type}', explanation: '{explanation[:100]}...'"

    def _fix_entity_type(self, entity_type: str) -> str:
        """Attempt to fix common entity type formatting issues."""
        if not entity_type:
            return "UNKNOWN"
        
        # Normalize the entity type
        normalized = entity_type.strip().upper()
        
        # Map common variations to valid types
        entity_type_mapping = {
            "PERSON": "PERSON",
            "PEOPLE": "PERSON",
            "HUMAN": "PERSON",
            "INDIVIDUAL": "PERSON",
            "ORG": "ORGANIZATION",
            "ORGANIZATION": "ORGANIZATION",
            "COMPANY": "ORGANIZATION",
            "INSTITUTION": "ORGANIZATION",
            "LOC": "LOCATION",
            "LOCATION": "LOCATION",
            "PLACE": "LOCATION",
            "COUNTRY": "LOCATION",
            "CITY": "LOCATION",
            "CONCEPT": "CONCEPT",
            "IDEA": "CONCEPT",
            "THEORY": "CONCEPT",
            "EVENT": "EVENT",
            "HISTORICAL_EVENT": "EVENT",
            "WORK": "WORK",
            "BOOK": "WORK",
            "MOVIE": "WORK",
            "TECH": "TECHNOLOGY",
            "TECHNOLOGY": "TECHNOLOGY",
            "SCIENTIFIC": "SCIENTIFIC_CONCEPT",
            "SCIENCE": "SCIENTIFIC_CONCEPT",
            "PHILOSOPHY": "PHILOSOPHICAL_CONCEPT",
            "PHILOSOPHICAL": "PHILOSOPHICAL_CONCEPT",
            "POLITICAL": "POLITICAL_CONCEPT",
            "POLITICS": "POLITICAL_CONCEPT",
            "UNKNOWN": "UNKNOWN",
            "OTHER": "UNKNOWN"
        }
        
        return entity_type_mapping.get(normalized, "UNKNOWN")

    def _fix_explanation(self, explanation: str) -> str:
        """Attempt to fix common explanation formatting issues."""
        if not explanation:
            return "No explanation provided."
        
        # Ensure minimum length
        if len(explanation.strip()) < 10:
            return f"Brief explanation: {explanation.strip()}"
        
        # Truncate if too long
        if len(explanation) > 1000:
            return explanation[:997] + "..."
        
        return explanation.strip()

    def forward(self, term: str, linked_wikipedia_title: str, retrieved_chunks: list) -> Tuple[str, str]:
        """
        Classify the entity and provide an explanation with Pydantic validation.
        
        Args:
            term: The term to classify
            linked_wikipedia_title: The linked Wikipedia article title
            retrieved_chunks: List of relevant text chunks from the article
            
        Returns:
            Tuple of (entity_type, explanation) with validated values
        """
        try:
            # Get prediction from DSPy
            # assumes DSPy is initialized with llm
            prediction = self.prog(
                term=term,
                linked_wikipedia_title=linked_wikipedia_title,
                retrieved_chunks=retrieved_chunks
            )
            
            # Validate the response
            validated_entity_type, validated_explanation = self._validate_llm_response(
                prediction.entity_type, 
                prediction.explanation
            )
            
            return validated_entity_type, validated_explanation
            
        except Exception as e:
            # Fallback in case of any errors
            return "UNKNOWN", f"Classification Entity-Forward failed: {str(e)}" 