"""
Test script to verify Wikipedia service functionality.
"""
from ..services.wikipedia_service import WikipediaService

def test_wikipedia_service():
    print("Testing Wikipedia Service...")
    
    try:
        # Initialize the service
        wiki_service = WikipediaService()
        print("✓ Wikipedia service initialized")
        
        # Test article retrieval
        test_article = "Python (programming language)"
        print(f"\nRetrieving test article: '{test_article}'")
        
        content = wiki_service.retrieve_article(test_article)
        if content:
            print(f"✓ Article retrieved successfully")
            print(f"Article length: {len(content)} characters")
            
            # Test chunking
            chunks = wiki_service.chunk_text(content, {"article_title": test_article})
            print(f"\nChunking results:")
            print(f"Number of chunks: {len(chunks)}")
            print(f"First chunk length: {len(chunks[0]['text'])} characters")
            print(f"First chunk metadata: {chunks[0]['metadata']}")
        else:
            print("✗ Failed to retrieve article")
            
        print("\nWikipedia service testing completed!")
        
    except Exception as e:
        print(f"Error in Wikipedia service: {e}")
        raise

if __name__ == "__main__":
    test_wikipedia_service() 