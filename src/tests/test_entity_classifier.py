"""
Test script to verify the Entity Classifier functionality with Pydantic validation.
"""
import dspy
from ..models.entity_classifier import (
    ClassifyEntityModule, 
    EntityType, 
    EntityClassificationResponse,
    EntityClassificationSignature
)
from ..models.llm_model import initialize_litellm_dspy
from pydantic import ValidationError


def test_entity_type_enum():
    """Test the EntityType enum values."""
    print("Testing EntityType enum...")
    
    # Test all valid entity types
    valid_types = [
        "PERSON", "ORGANIZATION", "LOCATION", "CONCEPT", "EVENT",
        "WORK", "TECHNOLOGY", "SCIENTIFIC_CONCEPT", "PHILOSOPHICAL_CONCEPT",
        "POLITICAL_CONCEPT", "UNKNOWN"
    ]
    
    for entity_type in valid_types:
        assert entity_type in EntityType.__members__, f"Entity type {entity_type} should be valid"
    
    print("✓ EntityType enum validation passed")


def test_entity_classification_response_validation():
    """Test Pydantic validation for EntityClassificationResponse."""
    print("\nTesting EntityClassificationResponse validation...")
    
    # Test valid response
    try:
        valid_response = EntityClassificationResponse(
            entity_type="PERSON",
            explanation="This is a valid explanation that meets the minimum length requirement."
        )
        assert valid_response.entity_type == EntityType.PERSON
        assert len(valid_response.explanation) >= 10
        print("✓ Valid response validation passed")
    except ValidationError as e:
        print(f"✗ Valid response validation failed: {e}")
        raise
    
    # Test invalid entity type
    try:
        EntityClassificationResponse(
            entity_type="INVALID_TYPE",
            explanation="This is a valid explanation."
        )
        print("✗ Invalid entity type should have failed validation")
        assert False
    except ValidationError:
        print("✓ Invalid entity type correctly rejected")
    
    # Test too short explanation
    try:
        EntityClassificationResponse(
            entity_type="PERSON",
            explanation="Short"
        )
        print("✗ Too short explanation should have failed validation")
        assert False
    except ValidationError:
        print("✓ Too short explanation correctly rejected")


def test_entity_classifier():
    """Test the Entity Classifier with DSPy integration and validation."""
    print("\nTesting Entity Classifier with validation...")
    
    try:
        # Initialize DSPy with our LiteLLM model
        llm = initialize_litellm_dspy()
        print("✓ DSPy and LiteLLM initialized")
        
        # Create the entity classifier
        classifier = ClassifyEntityModule()
        print("✓ Entity Classifier created")
        
        # Test data
        term = "Aristotle"
        linked_wikipedia_title = "Aristotle"
        retrieved_chunks = [
            "Aristotle was an Ancient Greek philosopher and polymath.",
            "His writings cover many subjects including physics, biology, zoology, metaphysics, logic, ethics, aesthetics, poetry, theatre, music, rhetoric, psychology, linguistics, economics, politics, meteorology, geology, and government.",
            "Aristotle provided a complex synthesis of the various philosophies existing prior to him."
        ]
        
        print(f"\nTesting classification for term: '{term}'")
        print(f"Wikipedia title: '{linked_wikipedia_title}'")
        print(f"Number of chunks: {len(retrieved_chunks)}")
        
        # Perform classification
        entity_type, explanation = classifier.forward(
            term=term,
            linked_wikipedia_title=linked_wikipedia_title,
            retrieved_chunks=retrieved_chunks
        )
        
        print(f"\nClassification Results:")
        print(f"Entity Type: {entity_type}")
        print(f"Explanation: {explanation}")
        
        # Enhanced validation
        assert entity_type is not None, "Entity type should not be None"
        assert explanation is not None, "Explanation should not be None"
        assert len(entity_type) > 0, "Entity type should not be empty"
        assert len(explanation) > 0, "Explanation should not be empty"
        
        # Validate entity type is from allowed set
        assert entity_type in [e.value for e in EntityType], f"Entity type '{entity_type}' should be from allowed set"
        
        # Validate explanation length
        assert len(explanation) >= 10, "Explanation should meet minimum length requirement"
        assert len(explanation) <= 1000, "Explanation should not exceed maximum length"
        
        print("✓ Entity classification test completed successfully!")
        
    except Exception as e:
        print(f"Error in Entity Classifier test: {e}")
        raise


def test_entity_classifier_with_different_terms():
    """Test the Entity Classifier with different types of entities."""
    print("\nTesting Entity Classifier with different entity types...")
    
    try:
        # Initialize DSPy with our LiteLLM model
        llm = initialize_litellm_dspy()
        
        # Create the entity classifier
        classifier = ClassifyEntityModule()
        
        # Test cases with expected entity types
        test_cases = [
            {
                "term": "Democracy",
                "title": "Democracy",
                "chunks": ["Democracy is a form of government in which the people have the authority to choose their governing legislators."],
                "expected_types": ["POLITICAL_CONCEPT", "CONCEPT"]
            },
            {
                "term": "Quantum Mechanics",
                "title": "Quantum Mechanics", 
                "chunks": ["Quantum mechanics is a fundamental theory in physics that describes the behavior of matter and energy at the atomic and subatomic level."],
                "expected_types": ["SCIENTIFIC_CONCEPT", "CONCEPT", "TECHNOLOGY"]
            },
            {
                "term": "Microsoft",
                "title": "Microsoft",
                "chunks": ["Microsoft Corporation is an American multinational technology company."],
                "expected_types": ["ORGANIZATION"]
            }
        ]
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\nTest Case {i}: '{test_case['term']}'")
            
            entity_type, explanation = classifier.forward(
                term=test_case["term"],
                linked_wikipedia_title=test_case["title"],
                retrieved_chunks=test_case["chunks"]
            )
            
            print(f"  Entity Type: {entity_type}")
            print(f"  Explanation: {explanation[:100]}...")  # Truncate for readability
            
            # Enhanced validation
            assert entity_type is not None and len(entity_type) > 0
            assert explanation is not None and len(explanation) > 0
            assert entity_type in [e.value for e in EntityType], f"Entity type '{entity_type}' should be from allowed set"
            assert len(explanation) >= 10, "Explanation should meet minimum length requirement"
            
            # Check if entity type is reasonable (optional, since LLM might choose different valid types)
            if entity_type not in test_case["expected_types"]:
                print(f"  Note: Expected one of {test_case['expected_types']}, got {entity_type}")
        
        print("✓ Multiple entity classification tests completed successfully!")
        
    except Exception as e:
        print(f"Error in multiple entity classification test: {e}")
        raise


def test_validation_fallback():
    """Test the validation fallback mechanisms."""
    print("\nTesting validation fallback mechanisms...")
    
    try:
        classifier = ClassifyEntityModule()
        
        # Test entity type fixing
        assert classifier._fix_entity_type("person") == "PERSON"
        assert classifier._fix_entity_type("org") == "ORGANIZATION"
        assert classifier._fix_entity_type("location") == "LOCATION"
        assert classifier._fix_entity_type("invalid_type") == "UNKNOWN"
        assert classifier._fix_entity_type("") == "UNKNOWN"
        
        # Test explanation fixing
        assert len(classifier._fix_explanation("Short")) >= 10
        assert len(classifier._fix_explanation("")) >= 10
        long_explanation = "x" * 1500
        fixed_long = classifier._fix_explanation(long_explanation)
        assert len(fixed_long) <= 1000
        assert fixed_long.endswith("...")
        
        print("✓ Validation fallback mechanisms working correctly")
        
    except Exception as e:
        print(f"Error in validation fallback test: {e}")
        raise


def test_signature_restrictions():
    """Test that the DSPy signature has the correct restrictions."""
    print("\nTesting DSPy signature restrictions...")
    
    try:
        # Check that the signature has the correct output field types
        # We can't instantiate the signature directly, but we can inspect its class attributes
        signature_class = EntityClassificationSignature
        
        # Verify entity_type field has Literal type restriction
        entity_type_field = signature_class.__annotations__.get("entity_type")
        assert entity_type_field is not None, "Entity type field should have annotation"
        
        # Check that it's a Literal type (this is a simplified check)
        assert "Literal" in str(entity_type_field), "Entity type should be a Literal type"
        
        # Verify explanation field has string type
        explanation_field = signature_class.__annotations__.get("explanation")
        assert explanation_field == str, "Explanation field should be string type"
        
        print("✓ DSPy signature restrictions correctly configured")
        
    except Exception as e:
        print(f"Error in signature restrictions test: {e}")
        raise


if __name__ == "__main__":
    test_entity_type_enum()
    test_entity_classification_response_validation()
    test_entity_classifier()
    test_entity_classifier_with_different_terms()
    test_validation_fallback()
    test_signature_restrictions() 