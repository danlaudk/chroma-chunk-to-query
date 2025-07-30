"""
Test script to verify sentence-transformers functionality.
"""
from sentence_transformers import SentenceTransformer
from ..config.settings import EMBEDDING_MODEL_NAME

def test_embeddings():
    print("Testing Sentence Transformers...")
    
    try:
        # Initialize the model
        model = SentenceTransformer(EMBEDDING_MODEL_NAME)
        print(f"✓ Model '{EMBEDDING_MODEL_NAME}' loaded successfully")
        
        # Test sentences
        sentences = [
            "This is a test sentence.",
            "Another different sentence for testing.",
            "A third sentence about something else."
        ]
        
        # Generate embeddings
        print("\nGenerating embeddings for test sentences...")
        embeddings = model.encode(sentences)
        
        # Verify embeddings shape
        print(f"\nEmbeddings generated successfully:")
        print(f"Number of sentences: {len(sentences)}")
        print(f"Embedding dimension: {embeddings.shape[1]}")
        
        print("\nSentence Transformers is working correctly!")
        
    except Exception as e:
        print(f"Error in embeddings setup: {e}")
        raise

if __name__ == "__main__":
    test_embeddings() 