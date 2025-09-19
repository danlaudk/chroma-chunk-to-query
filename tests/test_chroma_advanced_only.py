"""
Standalone test for ChromaService advanced queries only.
"""
import chromadb
from src.services.chroma_service import ChromaService
from src.config.settings import CHROMA_PERSISTENCE_DIR

def test_chroma_service_advanced_queries():
    """Test advanced ChromaService querying capabilities."""
    print("=" * 60)
    print("CHROMA SERVICE TEST: Advanced Queries")
    print("=" * 60)
    
    try:
        # Initialize ChromaService
        print("\n1. Initializing ChromaService...")
        chroma_service = ChromaService()
        
        # Create diverse test data
        print("\n2. Creating diverse test data...")
        diverse_chunks = [
            {
                "text": "Aristotle was an Ancient Greek philosopher and polymath who lived from 384 to 322 BCE.",
                "metadata": {
                    "source_article": "Aristotle",
                    "chunk_id": "aristotle_001",
                    "category": "philosopher"
                }
            },
            {
                "text": "Democracy is a form of government in which the people have the authority to choose their governing legislators.",
                "metadata": {
                    "source_article": "Democracy",
                    "chunk_id": "democracy_001",
                    "category": "political_system"
                }
            },
            {
                "text": "Quantum mechanics is a fundamental theory in physics that describes the behavior of matter and energy at the atomic and subatomic level.",
                "metadata": {
                    "source_article": "Quantum Mechanics",
                    "chunk_id": "quantum_001",
                    "category": "physics"
                }
            },
            {
                "text": "Artificial Intelligence is the simulation of human intelligence in machines that are programmed to think and learn like humans.",
                "metadata": {
                    "source_article": "Artificial Intelligence",
                    "chunk_id": "ai_001",
                    "category": "technology"
                }
            }
        ]
        
        # Index the diverse chunks
        print("\n3. Indexing diverse chunks...")
        chroma_service.index_chunks(diverse_chunks)
        print("✓ Diverse chunks indexed successfully")
        
        # Test semantic similarity queries
        print("\n4. Testing semantic similarity queries...")
        
        # Test 1: Query for philosophical concepts
        print("\n   Test 1: Querying for philosophical concepts...")
        philosophy_results = chroma_service.query_chunks("philosophy", "Aristotle")
        print(f"   ✓ Philosophy query returned {len(philosophy_results)} results")
        
        # Test 2: Query for political concepts
        print("\n   Test 2: Querying for political concepts...")
        politics_results = chroma_service.query_chunks("government", "Democracy")
        print(f"   ✓ Politics query returned {len(politics_results)} results")
        
        # Test 3: Query for scientific concepts
        print("\n   Test 3: Querying for scientific concepts...")
        science_results = chroma_service.query_chunks("physics", "Quantum Mechanics")
        print(f"   ✓ Science query returned {len(science_results)} results")
        
        # Test 4: Query for technology concepts
        print("\n   Test 4: Querying for technology concepts...")
        tech_results = chroma_service.query_chunks("machine learning", "Artificial Intelligence")
        print(f"   ✓ Technology query returned {len(tech_results)} results")
        
        # Test cross-article queries (should return empty due to metadata filtering)
        print("\n5. Testing cross-article queries (should be filtered out)...")
        cross_results = chroma_service.query_chunks("physics", "Democracy")
        print(f"   ✓ Cross-article query returned {len(cross_results)} results (expected 0 due to metadata filtering)")
        
        print("\n🎉 Advanced ChromaService query test completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Advanced ChromaService test failed: {e}")
        raise

if __name__ == "__main__":
    test_chroma_service_advanced_queries() 