"""
Test script to verify the Entity Classifier functionality.
"""
import dspy
from ..models.entity_classifier import ClassifyEntityModule
from ..models.llm_model import initialize_litellm_dspy

def test_entity_classifier():
    """Test the Entity Classifier with DSPy integration."""
    print("Testing Entity Classifier...")
    
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
        
        # Basic validation
        assert entity_type is not None, "Entity type should not be None"
        assert explanation is not None, "Explanation should not be None"
        assert len(entity_type) > 0, "Entity type should not be empty"
        assert len(explanation) > 0, "Explanation should not be empty"
        
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
        
        # Test cases
        test_cases = [
            {
                "term": "Democracy",
                "title": "Democracy",
                "chunks": ["Democracy is a form of government in which the people have the authority to choose their governing legislators."]
            },
            {
                "term": "Quantum Mechanics",
                "title": "Quantum Mechanics", 
                "chunks": ["Quantum mechanics is a fundamental theory in physics that describes the behavior of matter and energy at the atomic and subatomic level."]
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
            
            # Basic validation
            assert entity_type is not None and len(entity_type) > 0
            assert explanation is not None and len(explanation) > 0
        
        print("✓ Multiple entity classification tests completed successfully!")
        
    except Exception as e:
        print(f"Error in multiple entity classification test: {e}")
        raise

if __name__ == "__main__":
    test_entity_classifier()
    test_entity_classifier_with_different_terms() 