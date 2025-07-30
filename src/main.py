"""
Main script demonstrating the entity classification and Wikipedia matching system.
"""

from services.entity_processor import EntityProcessor

def main():
    # Initialize the entity processor
    processor = EntityProcessor()
    
    # Example usage
    terms = [
        "Aristotle",
        "democracy",
        "quantum mechanics",
        "artificial intelligence"
    ]
    
    for term in terms:
        try:
            result = processor.process_entity(term)
            print("\nProcessing Results:")
            print(f"Term: {result['term']}")
            print(f"Entity Type: {result['entity_type']}")
            print(f"Explanation: {result['explanation']}")
            print(f"Number of matched chunks: {len(result['matched_chunks'])}")
            print("-" * 50)
        except Exception as e:
            print(f"Error processing term '{term}': {e}")

if __name__ == "__main__":
    main() 