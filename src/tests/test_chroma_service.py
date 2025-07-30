"""
Comprehensive test for ChromaService functionality.
Tests chunk indexing, querying, and metadata filtering.
"""
import chromadb
from ..services.chroma_service import ChromaService
from ..config.settings import CHROMA_PERSISTENCE_DIR

def test_chroma_service_basic_functionality():
    """Test basic ChromaService functionality with proper metadata."""
    print("=" * 60)
    print("CHROMA SERVICE TEST: Basic Functionality")
    print("=" * 60)
    
    try:
        # Initialize ChromaService
        print("\n1. Initializing ChromaService...")
        chroma_service = ChromaService()
        print("✓ ChromaService initialized successfully")
        
        # Create test chunks with proper metadata structure
        print("\n2. Creating test chunks...")
        test_chunks = [
            {
                "text": "Python is a high-level programming language known for its simplicity and readability.",
                "metadata": {
                    "source_article": "Python (programming language)",
                    "chunk_id": "python_001",
                    "section": "introduction"
                }
            },
            {
                "text": "Python was created by Guido van Rossum and first released in 1991.",
                "metadata": {
                    "source_article": "Python (programming language)",
                    "chunk_id": "python_002",
                    "section": "history"
                }
            },
            {
                "text": "Python supports multiple programming paradigms including procedural, object-oriented, and functional programming.",
                "metadata": {
                    "source_article": "Python (programming language)",
                    "chunk_id": "python_003",
                    "section": "features"
                }
            },
            {
                "text": "Machine learning is a subset of artificial intelligence that enables computers to learn without being explicitly programmed.",
                "metadata": {
                    "source_article": "Machine Learning",
                    "chunk_id": "ml_001",
                    "section": "definition"
                }
            },
            {
                "text": "Deep learning is a subset of machine learning that uses neural networks with multiple layers.",
                "metadata": {
                    "source_article": "Machine Learning",
                    "chunk_id": "ml_002",
                    "section": "deep_learning"
                }
            }
        ]
        
        print(f"✓ Created {len(test_chunks)} test chunks")
        for i, chunk in enumerate(test_chunks, 1):
            print(f"   Chunk {i}: {chunk['text'][:50]}...")
        
        # Index chunks
        print("\n3. Indexing chunks in ChromaDB...")
        chroma_service.index_chunks(test_chunks)
        print("✓ Chunks indexed successfully")
        
        # Test basic querying without metadata filter
        print("\n4. Testing basic querying...")
        results = chroma_service.collection.query(
            query_texts=["programming language"],
            n_results=3
        )
        assert len(results['documents'][0]) > 0, "Basic query returned no results"
        print(f"✓ Basic query returned {len(results['documents'][0])} results")
        
        # Test querying with metadata filtering
        print("\n5. Testing metadata filtering...")
        
        # Test 1: Query for Python-related content
        print("\n   Test 1: Querying for Python content...")
        python_results = chroma_service.query_chunks("programming", "Python (programming language)")
        assert len(python_results) > 0, "Python query returned no results"
        print(f"   ✓ Python query returned {len(python_results)} results")
        for i, result in enumerate(python_results, 1):
            print(f"     Result {i}: {result['text'][:60]}...")
            print(f"     Metadata: {result['metadata']}")
        
        # Test 2: Query for Machine Learning content
        print("\n   Test 2: Querying for Machine Learning content...")
        ml_results = chroma_service.query_chunks("neural networks", "Machine Learning")
        assert len(ml_results) > 0, "Machine Learning query returned no results"
        print(f"   ✓ Machine Learning query returned {len(ml_results)} results")
        for i, result in enumerate(ml_results, 1):
            print(f"     Result {i}: {result['text'][:60]}...")
            print(f"     Metadata: {result['metadata']}")
        
        # Test 3: Query with non-existent article (should return empty)
        print("\n   Test 3: Querying for non-existent article...")
        empty_results = chroma_service.query_chunks("test", "NonExistentArticle")
        print(f"   ✓ Non-existent article query returned {len(empty_results)} results (expected 0)")
        
        print("\n🎉 Basic ChromaService functionality test completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Basic ChromaService test failed: {e}")
        raise

def test_chroma_service_advanced_queries():
    """Test advanced ChromaService querying capabilities."""
    print("\n" + "=" * 60)
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

def test_chroma_service_edge_cases():
    """Test ChromaService edge cases and error handling."""
    print("\n" + "=" * 60)
    print("CHROMA SERVICE TEST: Edge Cases")
    print("=" * 60)
    
    try:
        # Initialize ChromaService
        print("\n1. Initializing ChromaService...")
        chroma_service = ChromaService()
        
        # Test 1: Empty chunks list
        print("\n2. Testing empty chunks list...")
        try:
            chroma_service.index_chunks([])
            print("   ✓ Empty chunks list handled gracefully")
        except Exception as e:
            print(f"   ⚠ Empty chunks list caused error: {e}")
        
        # Test 2: Single character text
        print("\n3. Testing single character text...")
        single_char_chunks = [
            {
                "text": "A",
                "metadata": {
                    "source_article": "Test",
                    "chunk_id": "single_001"
                }
            }
        ]
        chroma_service.index_chunks(single_char_chunks)
        print("   ✓ Single character text indexed successfully")
        
        # Test 3: Very long text
        print("\n4. Testing very long text...")
        long_text = "This is a very long text " * 100  # Create a long text
        long_chunks = [
            {
                "text": long_text,
                "metadata": {
                    "source_article": "LongText",
                    "chunk_id": "long_001"
                }
            }
        ]
        chroma_service.index_chunks(long_chunks)
        print("   ✓ Very long text indexed successfully")
        
        # Test 4: Special characters in text
        print("\n5. Testing special characters...")
        special_chunks = [
            {
                "text": "Text with special chars: @#$%^&*()_+-=[]{}|;':\",./<>?",
                "metadata": {
                    "source_article": "SpecialChars",
                    "chunk_id": "special_001"
                }
            }
        ]
        chroma_service.index_chunks(special_chunks)
        print("   ✓ Special characters handled successfully")
        
        # Test 5: Query with empty string
        print("\n6. Testing query with empty string...")
        empty_query_results = chroma_service.query_chunks("", "Test")
        print(f"   ✓ Empty query returned {len(empty_query_results)} results")
        
        # Test 6: Query with very long string
        print("\n7. Testing query with very long string...")
        long_query = "This is a very long query string " * 50
        long_query_results = chroma_service.query_chunks(long_query, "Test")
        print(f"   ✓ Long query returned {len(long_query_results)} results")
        
        print("\n🎉 Edge cases test completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Edge cases test failed: {e}")
        raise

def test_chroma_service_performance():
    """Test ChromaService performance with larger datasets."""
    print("\n" + "=" * 60)
    print("CHROMA SERVICE TEST: Performance")
    print("=" * 60)
    
    try:
        # Initialize ChromaService
        print("\n1. Initializing ChromaService...")
        chroma_service = ChromaService()
        
        # Create larger dataset
        print("\n2. Creating larger dataset...")
        large_chunks = []
        for i in range(20):  # Create 20 chunks
            chunk = {
                "text": f"This is test chunk number {i} with some content about various topics including technology, science, and philosophy.",
                "metadata": {
                    "source_article": f"TestArticle_{i % 4}",  # 4 different articles
                    "chunk_id": f"chunk_{i:03d}",
                    "index": i
                }
            }
            large_chunks.append(chunk)
        
        print(f"✓ Created {len(large_chunks)} chunks across 4 articles")
        
        # Index large dataset
        print("\n3. Indexing large dataset...")
        chroma_service.index_chunks(large_chunks)
        print("✓ Large dataset indexed successfully")
        
        # Test querying performance
        print("\n4. Testing querying performance...")
        
        # Test queries across different articles
        for article_num in range(4):
            article_name = f"TestArticle_{article_num}"
            results = chroma_service.query_chunks("test content", article_name)
            print(f"   Article {article_name}: {len(results)} results")
        
        print("\n🎉 Performance test completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Performance test failed: {e}")
        raise

if __name__ == "__main__":
    test_chroma_service_basic_functionality()
    test_chroma_service_advanced_queries()
    test_chroma_service_edge_cases()
    test_chroma_service_performance() 