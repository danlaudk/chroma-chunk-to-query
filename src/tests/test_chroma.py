"""
Test script to verify ChromaDB installation and functionality.
"""
import chromadb
from chromadb.config import Settings

def test_chroma_installation():
    print("Testing ChromaDB installation...")
    
    # Create an in-memory client for testing
    client = chromadb.Client(Settings(
        is_persistent=False,
        anonymized_telemetry=False
    ))
    
    # Create a test collection
    collection = client.create_collection(name="test_collection")
    
    # Add some test documents
    collection.add(
        documents=["This is a test document", "Another test document"],
        metadatas=[{"source": "test1"}, {"source": "test2"}],
        ids=["id1", "id2"]
    )
    
    # Query the collection
    results = collection.query(
        query_texts=["test document"],
        n_results=2
    )
    
    # Print results
    print("\nQuery Results:")
    for i, (doc, metadata) in enumerate(zip(results['documents'][0], results['metadatas'][0])):
        print(f"\nDocument {i+1}:")
        print(f"Content: {doc}")
        print(f"Metadata: {metadata}")
    
    print("\nChromaDB is working correctly!")

if __name__ == "__main__":
    test_chroma_installation() 