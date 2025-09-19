"""
Demonstration of Pydantic validation features for LLM responses.
"""
import dspy
from src.models.entity_classifier import (
    ClassifyEntityModule, 
    EntityType, 
    EntityClassificationResponse
)
from src.models.llm_model import initialize_dspy
from pydantic import ValidationError


def demo_validation_features():
    """Demonstrate the validation features with examples."""
    print("=" * 60)
    print("Pydantic Validation Features Demonstration")
    print("=" * 60)
    
    # Initialize the classifier
    llm = initialize_dspy()
    classifier = ClassifyEntityModule()
    
    print("\n1. Testing Valid LLM Response Validation")
    print("-" * 40)
    
    # Simulate a valid LLM response
    valid_entity_type = "PERSON"
    valid_explanation = "This is a valid explanation that meets the minimum length requirement and provides meaningful context about the entity classification."
    
    try:
        validated_type, validated_explanation = classifier._validate_llm_response(
            valid_entity_type, valid_explanation
        )
        print(f"✓ Valid response accepted:")
        print(f"  Entity Type: {validated_type}")
        print(f"  Explanation: {validated_explanation[:80]}...")
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
    
    print("\n2. Testing Invalid Entity Type Handling")
    print("-" * 40)
    
    # Test various invalid entity types
    invalid_cases = [
        ("INVALID_TYPE", "This should be rejected."),
        ("person", "Should be normalized to PERSON."),
        ("org", "Should be normalized to ORGANIZATION."),
        ("", "Empty string should become UNKNOWN."),
        ("random_text", "Unknown type should become UNKNOWN."),
    ]
    
    for invalid_type, explanation in invalid_cases:
        try:
            validated_type, validated_explanation = classifier._validate_llm_response(
                invalid_type, explanation
            )
            print(f"✓ Fixed '{invalid_type}' → '{validated_type}'")
        except Exception as e:
            print(f"✗ Failed to fix '{invalid_type}': {e}")
    
    print("\n3. Testing Invalid Explanation Handling")
    print("-" * 40)
    
    # Test various invalid explanations
    invalid_explanations = [
        ("PERSON", "Short"),  # Too short
        ("PERSON", ""),  # Empty
        ("PERSON", "x" * 1500),  # Too long
    ]
    
    for entity_type, explanation in invalid_explanations:
        try:
            validated_type, validated_explanation = classifier._validate_llm_response(
                entity_type, explanation
            )
            print(f"✓ Fixed explanation for '{entity_type}':")
            print(f"  Length: {len(validated_explanation)} chars")
            print(f"  Preview: {validated_explanation[:50]}...")
        except Exception as e:
            print(f"✗ Failed to fix explanation: {e}")
    
    print("\n4. Testing Entity Type Mapping")
    print("-" * 40)
    
    # Test the entity type mapping function
    mapping_tests = [
        ("person", "PERSON"),
        ("people", "PERSON"),
        ("organization", "ORGANIZATION"),
        ("company", "ORGANIZATION"),
        ("location", "LOCATION"),
        ("place", "LOCATION"),
        ("concept", "CONCEPT"),
        ("theory", "CONCEPT"),
        ("technology", "TECHNOLOGY"),
        ("tech", "TECHNOLOGY"),
        ("science", "SCIENTIFIC_CONCEPT"),
        ("philosophy", "PHILOSOPHICAL_CONCEPT"),
        ("politics", "POLITICAL_CONCEPT"),
        ("unknown", "UNKNOWN"),
        ("invalid", "UNKNOWN"),
    ]
    
    for input_type, expected in mapping_tests:
        result = classifier._fix_entity_type(input_type)
        status = "✓" if result == expected else "✗"
        print(f"{status} '{input_type}' → '{result}' (expected: '{expected}')")
    
    print("\n5. Testing Pydantic Model Validation")
    print("-" * 40)
    
    # Test the Pydantic model directly
    try:
        response = EntityClassificationResponse(
            entity_type="PERSON",
            explanation="This is a valid explanation that meets all requirements."
        )
        print(f"✓ Pydantic model validation passed")
        print(f"  Entity Type: {response.entity_type}")
        print(f"  Explanation Length: {len(response.explanation)}")
    except ValidationError as e:
        print(f"✗ Pydantic validation failed: {e}")
    
    # Test invalid Pydantic model
    try:
        EntityClassificationResponse(
            entity_type="INVALID_TYPE",
            explanation="Valid explanation."
        )
        print("✗ Should have failed validation")
    except ValidationError:
        print("✓ Correctly rejected invalid entity type")
    
    print("\n6. Testing Real LLM Response with Validation")
    print("-" * 40)
    
    # Test with a real classification
    test_term = "Albert Einstein"
    test_chunks = [
        "Albert Einstein was a German-born theoretical physicist who developed the theory of relativity.",
        "He is considered one of the most influential scientists of the 20th century."
    ]
    
    try:
        entity_type, explanation = classifier.forward(
            term=test_term,
            linked_wikipedia_title="Albert Einstein",
            retrieved_chunks=test_chunks
        )
        
        print(f"✓ Real classification with validation:")
        print(f"  Term: {test_term}")
        print(f"  Entity Type: {entity_type}")
        print(f"  Explanation: {explanation[:100]}...")
        
        # Verify the result is valid
        assert entity_type in [e.value for e in EntityType]
        assert len(explanation) >= 10
        assert len(explanation) <= 1000
        
    except Exception as e:
        print(f"✗ Real classification failed: {e}")
    
    print("\n" + "=" * 60)
    print("Validation Features Demonstration Complete!")
    print("=" * 60)


if __name__ == "__main__":
    demo_validation_features() 