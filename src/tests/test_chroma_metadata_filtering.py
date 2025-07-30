"""
Comprehensive test suite for ChromaDB metadata filtering functionality.
Tests cross-article filtering, complex metadata structures, and edge cases.
"""
import chromadb
import time
from typing import List, Dict, Any
from ..services.chroma_service import ChromaService
from ..config.settings import CHROMA_PERSISTENCE_DIR

def create_test_chunks_with_complex_metadata() -> List[Dict[str, Any]]:
    """Create test chunks with complex metadata structures for comprehensive testing."""
    return [
        # Article 1: Technology
        {
            "text": "Python is a high-level programming language known for its simplicity and readability.",
            "metadata": {
                "source_article": "Python (programming language)",
                "chunk_id": "python_001",
                "section": "introduction",
                "category": "technology",
                "subcategory": "programming_language",
                "year_created": 1991,
                "creator": "Guido van Rossum",
                "tags": "programming,language,python",
                "difficulty": "beginner",
                "domain": "computer_science"
            }
        },
        {
            "text": "Python supports multiple programming paradigms including procedural, object-oriented, and functional programming.",
            "metadata": {
                "source_article": "Python (programming language)",
                "chunk_id": "python_002",
                "section": "features",
                "category": "technology",
                "subcategory": "programming_language",
                "year_created": 1991,
                "creator": "Guido van Rossum",
                "tags": "programming,paradigms,oop",
                "difficulty": "intermediate",
                "domain": "computer_science"
            }
        },
        {
            "text": "Python's extensive standard library and third-party packages make it ideal for data science and machine learning.",
            "metadata": {
                "source_article": "Python (programming language)",
                "chunk_id": "python_003",
                "section": "applications",
                "category": "technology",
                "subcategory": "programming_language",
                "year_created": 1991,
                "creator": "Guido van Rossum",
                "tags": "data_science,machine_learning,libraries",
                "difficulty": "advanced",
                "domain": "computer_science"
            }
        },
        
        # Article 2: Science
        {
            "text": "Quantum mechanics is a fundamental theory in physics that describes the behavior of matter and energy at the atomic and subatomic level.",
            "metadata": {
                "source_article": "Quantum Mechanics",
                "chunk_id": "quantum_001",
                "section": "introduction",
                "category": "science",
                "subcategory": "physics",
                "year_developed": 1920,
                "pioneers": "Max Planck,Niels Bohr,Werner Heisenberg",
                "tags": "physics,quantum,atomic",
                "difficulty": "advanced",
                "domain": "physics"
            }
        },
        {
            "text": "The uncertainty principle states that the more precisely the position of a particle is determined, the less precisely its momentum can be known.",
            "metadata": {
                "source_article": "Quantum Mechanics",
                "chunk_id": "quantum_002",
                "section": "uncertainty_principle",
                "category": "science",
                "subcategory": "physics",
                "year_developed": 1920,
                "pioneers": "Max Planck,Niels Bohr,Werner Heisenberg",
                "tags": "uncertainty,momentum,position",
                "difficulty": "advanced",
                "domain": "physics"
            }
        },
        {
            "text": "Quantum entanglement is a phenomenon where two or more particles become correlated in such a way that the quantum state of each particle cannot be described independently.",
            "metadata": {
                "source_article": "Quantum Mechanics",
                "chunk_id": "quantum_003",
                "section": "entanglement",
                "category": "science",
                "subcategory": "physics",
                "year_developed": 1920,
                "pioneers": "Max Planck,Niels Bohr,Werner Heisenberg",
                "tags": "entanglement,correlation,particles",
                "difficulty": "advanced",
                "domain": "physics"
            }
        },
        
        # Article 3: Philosophy
        {
            "text": "Aristotle was an Ancient Greek philosopher and polymath who lived from 384 to 322 BCE.",
            "metadata": {
                "source_article": "Aristotle",
                "chunk_id": "aristotle_001",
                "section": "biography",
                "category": "philosophy",
                "subcategory": "ancient_philosophy",
                "era": "ancient_greece",
                "influences": "Plato,Socrates",
                "tags": "philosopher,ancient_greece,polymath",
                "difficulty": "intermediate",
                "domain": "philosophy"
            }
        },
        {
            "text": "Aristotle's Nicomachean Ethics explores the nature of virtue and the good life, introducing the concept of eudaimonia or human flourishing.",
            "metadata": {
                "source_article": "Aristotle",
                "chunk_id": "aristotle_002",
                "section": "ethics",
                "category": "philosophy",
                "subcategory": "ancient_philosophy",
                "era": "ancient_greece",
                "influences": "Plato,Socrates",
                "tags": "ethics,virtue,eudaimonia",
                "difficulty": "intermediate",
                "domain": "philosophy"
            }
        },
        {
            "text": "Aristotle's logical works, particularly the Organon, laid the foundation for formal logic and scientific methodology.",
            "metadata": {
                "source_article": "Aristotle",
                "chunk_id": "aristotle_003",
                "section": "logic",
                "category": "philosophy",
                "subcategory": "ancient_philosophy",
                "era": "ancient_greece",
                "influences": "Plato,Socrates",
                "tags": "logic,organon,methodology",
                "difficulty": "intermediate",
                "domain": "philosophy"
            }
        },
        
        # Article 4: Politics
        {
            "text": "Democracy is a form of government in which the people have the authority to choose their governing legislators.",
            "metadata": {
                "source_article": "Democracy",
                "chunk_id": "democracy_001",
                "section": "definition",
                "category": "politics",
                "subcategory": "political_system",
                "origin": "ancient_greece",
                "modern_forms": "representative,direct,parliamentary",
                "tags": "government,people,authority",
                "difficulty": "beginner",
                "domain": "political_science"
            }
        },
        {
            "text": "Representative democracy allows citizens to elect representatives who make decisions on their behalf in legislative bodies.",
            "metadata": {
                "source_article": "Democracy",
                "chunk_id": "democracy_002",
                "section": "representative",
                "category": "politics",
                "subcategory": "political_system",
                "origin": "ancient_greece",
                "modern_forms": "representative,direct,parliamentary",
                "tags": "representative,elections,legislature",
                "difficulty": "beginner",
                "domain": "political_science"
            }
        },
        {
            "text": "Direct democracy involves citizens directly participating in decision-making through referendums and initiatives.",
            "metadata": {
                "source_article": "Democracy",
                "chunk_id": "democracy_003",
                "section": "direct",
                "category": "politics",
                "subcategory": "political_system",
                "origin": "ancient_greece",
                "modern_forms": "representative,direct,parliamentary",
                "tags": "direct,referendums,initiatives",
                "difficulty": "beginner",
                "domain": "political_science"
            }
        }
    ]

def test_basic_metadata_filtering():
    """Test basic metadata filtering functionality."""
    print("=" * 70)
    print("CHROMA METADATA FILTERING TEST: Basic Functionality")
    print("=" * 70)
    
    try:
        # Initialize ChromaService
        print("\n1. Initializing ChromaService...")
        chroma_service = ChromaService()
        print("✓ ChromaService initialized successfully")
        
        # Create test chunks
        print("\n2. Creating test chunks with complex metadata...")
        test_chunks = create_test_chunks_with_complex_metadata()
        print(f"✓ Created {len(test_chunks)} test chunks across 4 articles")
        
        # Index chunks
        print("\n3. Indexing chunks in ChromaDB...")
        chroma_service.index_chunks(test_chunks)
        print("✓ Chunks indexed successfully")
        
        # Test basic source_article filtering
        print("\n4. Testing basic source_article filtering...")
        
        # Test Python article filtering
        python_results = chroma_service.query_chunks("programming", "Python (programming language)")
        assert len(python_results) > 0, "Python query should return results"
        assert all(result['metadata']['source_article'] == "Python (programming language)" for result in python_results), \
            "All results should be from Python article"
        print(f"✓ Python filtering: {len(python_results)} results, all from correct article")
        
        # Test Quantum Mechanics article filtering
        quantum_results = chroma_service.query_chunks("physics", "Quantum Mechanics")
        assert len(quantum_results) > 0, "Quantum query should return results"
        assert all(result['metadata']['source_article'] == "Quantum Mechanics" for result in quantum_results), \
            "All results should be from Quantum Mechanics article"
        print(f"✓ Quantum filtering: {len(quantum_results)} results, all from correct article")
        
        # Test Aristotle article filtering
        aristotle_results = chroma_service.query_chunks("philosophy", "Aristotle")
        assert len(aristotle_results) > 0, "Aristotle query should return results"
        assert all(result['metadata']['source_article'] == "Aristotle" for result in aristotle_results), \
            "All results should be from Aristotle article"
        print(f"✓ Aristotle filtering: {len(aristotle_results)} results, all from correct article")
        
        # Test Democracy article filtering
        democracy_results = chroma_service.query_chunks("government", "Democracy")
        assert len(democracy_results) > 0, "Democracy query should return results"
        assert all(result['metadata']['source_article'] == "Democracy" for result in democracy_results), \
            "All results should be from Democracy article"
        print(f"✓ Democracy filtering: {len(democracy_results)} results, all from correct article")
        
        print("\n🎉 Basic metadata filtering test completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Basic metadata filtering test failed: {e}")
        raise

def test_cross_article_contamination_prevention():
    """Test that metadata filtering prevents cross-article contamination."""
    print("\n" + "=" * 70)
    print("CHROMA METADATA FILTERING TEST: Cross-Article Contamination Prevention")
    print("=" * 70)
    
    try:
        # Initialize ChromaService
        print("\n1. Initializing ChromaService...")
        chroma_service = ChromaService()
        
        # Create test chunks
        print("\n2. Creating test chunks...")
        test_chunks = create_test_chunks_with_complex_metadata()
        chroma_service.index_chunks(test_chunks)
        print("✓ Chunks indexed successfully")
        
        # Test cross-article queries that should return empty results
        print("\n3. Testing cross-article contamination prevention...")
        
        # Test 1: Query physics terms in Python article (should return empty)
        print("\n   Test 1: Querying physics terms in Python article...")
        physics_in_python = chroma_service.query_chunks("quantum mechanics", "Python (programming language)")
        assert len(physics_in_python) == 0, "Physics query in Python article should return empty"
        print(f"   ✓ Physics query in Python: {len(physics_in_python)} results (expected 0)")
        
        # Test 2: Query programming terms in Quantum Mechanics article (should return empty)
        print("\n   Test 2: Querying programming terms in Quantum Mechanics article...")
        programming_in_quantum = chroma_service.query_chunks("python programming", "Quantum Mechanics")
        assert len(programming_in_quantum) == 0, "Programming query in Quantum article should return empty"
        print(f"   ✓ Programming query in Quantum: {len(programming_in_quantum)} results (expected 0)")
        
        # Test 3: Query philosophy terms in Democracy article (should return empty)
        print("\n   Test 3: Querying philosophy terms in Democracy article...")
        philosophy_in_democracy = chroma_service.query_chunks("aristotle ethics", "Democracy")
        assert len(philosophy_in_democracy) == 0, "Philosophy query in Democracy article should return empty"
        print(f"   ✓ Philosophy query in Democracy: {len(philosophy_in_democracy)} results (expected 0)")
        
        # Test 4: Query political terms in Aristotle article (should return empty)
        print("\n   Test 4: Querying political terms in Aristotle article...")
        politics_in_aristotle = chroma_service.query_chunks("democracy government", "Aristotle")
        assert len(politics_in_aristotle) == 0, "Politics query in Aristotle article should return empty"
        print(f"   ✓ Politics query in Aristotle: {len(politics_in_aristotle)} results (expected 0)")
        
        # Test 5: Query with non-existent article (should return empty)
        print("\n   Test 5: Querying non-existent article...")
        nonexistent_results = chroma_service.query_chunks("any query", "NonExistentArticle")
        assert len(nonexistent_results) == 0, "Non-existent article query should return empty"
        print(f"   ✓ Non-existent article query: {len(nonexistent_results)} results (expected 0)")
        
        print("\n🎉 Cross-article contamination prevention test completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Cross-article contamination prevention test failed: {e}")
        raise

def test_complex_metadata_filtering():
    """Test filtering with complex metadata structures and multiple criteria."""
    print("\n" + "=" * 70)
    print("CHROMA METADATA FILTERING TEST: Complex Metadata Structures")
    print("=" * 70)
    
    try:
        # Initialize ChromaService
        print("\n1. Initializing ChromaService...")
        chroma_service = ChromaService()
        
        # Create test chunks
        print("\n2. Creating test chunks...")
        test_chunks = create_test_chunks_with_complex_metadata()
        chroma_service.index_chunks(test_chunks)
        print("✓ Chunks indexed successfully")
        
        # Test direct collection queries with complex metadata filters
        print("\n3. Testing complex metadata filtering...")
        
        # Test 1: Filter by category
        print("\n   Test 1: Filtering by category...")
        tech_results = chroma_service.collection.query(
            query_texts=["programming"],
            n_results=10,
            where={"category": "technology"}
        )
        assert len(tech_results['documents'][0]) > 0, "Technology category filter should return results"
        assert all(metadata['category'] == 'technology' for metadata in tech_results['metadatas'][0]), \
            "All results should have technology category"
        print(f"   ✓ Technology category filter: {len(tech_results['documents'][0])} results")
        
        # Test 2: Filter by difficulty level
        print("\n   Test 2: Filtering by difficulty level...")
        beginner_results = chroma_service.collection.query(
            query_texts=["concepts"],
            n_results=10,
            where={"difficulty": "beginner"}
        )
        assert len(beginner_results['documents'][0]) > 0, "Beginner difficulty filter should return results"
        assert all(metadata['difficulty'] == 'beginner' for metadata in beginner_results['metadatas'][0]), \
            "All results should have beginner difficulty"
        print(f"   ✓ Beginner difficulty filter: {len(beginner_results['documents'][0])} results")
        
        # Test 3: Filter by domain
        print("\n   Test 3: Filtering by domain...")
        physics_results = chroma_service.collection.query(
            query_texts=["science"],
            n_results=10,
            where={"domain": "physics"}
        )
        assert len(physics_results['documents'][0]) > 0, "Physics domain filter should return results"
        assert all(metadata['domain'] == 'physics' for metadata in physics_results['metadatas'][0]), \
            "All results should have physics domain"
        print(f"   ✓ Physics domain filter: {len(physics_results['documents'][0])} results")
        
        # Test 4: Filter by subcategory
        print("\n   Test 4: Filtering by subcategory...")
        philosophy_results = chroma_service.collection.query(
            query_texts=["thinking"],
            n_results=10,
            where={"subcategory": "ancient_philosophy"}
        )
        assert len(philosophy_results['documents'][0]) > 0, "Ancient philosophy subcategory filter should return results"
        assert all(metadata['subcategory'] == 'ancient_philosophy' for metadata in philosophy_results['metadatas'][0]), \
            "All results should have ancient_philosophy subcategory"
        print(f"   ✓ Ancient philosophy subcategory filter: {len(philosophy_results['documents'][0])} results")
        
        print("\n🎉 Complex metadata filtering test completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Complex metadata filtering test failed: {e}")
        raise

def test_metadata_filtering_performance():
    """Test metadata filtering performance with larger datasets."""
    print("\n" + "=" * 70)
    print("CHROMA METADATA FILTERING TEST: Performance")
    print("=" * 70)
    
    try:
        # Initialize ChromaService
        print("\n1. Initializing ChromaService...")
        chroma_service = ChromaService()
        
        # Create larger dataset
        print("\n2. Creating larger dataset for performance testing...")
        large_chunks = []
        articles = ["Article_A", "Article_B", "Article_C", "Article_D", "Article_E"]
        categories = ["technology", "science", "philosophy", "politics", "history"]
        
        for i in range(100):  # Create 100 chunks
            article = articles[i % len(articles)]
            category = categories[i % len(categories)]
            chunk = {
                "text": f"This is test chunk number {i} with content about {category} and various topics including technology, science, and philosophy.",
                "metadata": {
                    "source_article": article,
                    "chunk_id": f"chunk_{i:03d}",
                    "category": category,
                    "index": i,
                    "difficulty": "intermediate" if i % 2 == 0 else "advanced",
                    "domain": f"domain_{category}"
                }
            }
            large_chunks.append(chunk)
        
        print(f"✓ Created {len(large_chunks)} chunks across {len(articles)} articles")
        
        # Index large dataset
        print("\n3. Indexing large dataset...")
        start_time = time.time()
        chroma_service.index_chunks(large_chunks)
        indexing_time = time.time() - start_time
        print(f"✓ Large dataset indexed in {indexing_time:.2f} seconds")
        
        # Test querying performance with metadata filtering
        print("\n4. Testing querying performance with metadata filtering...")
        
        # Test performance across different articles
        query_times = []
        for article in articles:
            start_time = time.time()
            results = chroma_service.query_chunks("test content", article)
            query_time = time.time() - start_time
            query_times.append(query_time)
            print(f"   Article {article}: {len(results)} results in {query_time:.3f}s")
        
        avg_query_time = sum(query_times) / len(query_times)
        print(f"\n   Average query time: {avg_query_time:.3f} seconds")
        print(f"   Total chunks in database: {len(large_chunks)}")
        
        # Test performance with complex metadata filters
        print("\n5. Testing complex metadata filter performance...")
        complex_filter_times = []
        for category in categories:
            start_time = time.time()
            results = chroma_service.collection.query(
                query_texts=["test"],
                n_results=20,
                where={"category": category}
            )
            query_time = time.time() - start_time
            complex_filter_times.append(query_time)
            print(f"   Category {category}: {len(results['documents'][0])} results in {query_time:.3f}s")
        
        avg_complex_time = sum(complex_filter_times) / len(complex_filter_times)
        print(f"\n   Average complex filter time: {avg_complex_time:.3f} seconds")
        
        # Performance assertions
        assert avg_query_time < 1.0, f"Average query time ({avg_query_time:.3f}s) should be under 1 second"
        assert avg_complex_time < 1.0, f"Average complex filter time ({avg_complex_time:.3f}s) should be under 1 second"
        
        print("\n🎉 Performance test completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Performance test failed: {e}")
        raise

def test_metadata_filtering_edge_cases():
    """Test metadata filtering edge cases and error handling."""
    print("\n" + "=" * 70)
    print("CHROMA METADATA FILTERING TEST: Edge Cases")
    print("=" * 70)
    
    try:
        # Initialize ChromaService
        print("\n1. Initializing ChromaService...")
        chroma_service = ChromaService()
        
        # Create test chunks
        print("\n2. Creating test chunks...")
        test_chunks = create_test_chunks_with_complex_metadata()
        chroma_service.index_chunks(test_chunks)
        print("✓ Chunks indexed successfully")
        
        # Test edge cases
        print("\n3. Testing edge cases...")
        
        # Test 1: Empty query string
        print("\n   Test 1: Empty query string...")
        empty_query_results = chroma_service.query_chunks("", "Python (programming language)")
        print(f"   ✓ Empty query returned {len(empty_query_results)} results")
        
        # Test 2: Very long query string
        print("\n   Test 2: Very long query string...")
        long_query = "This is a very long query string " * 50
        long_query_results = chroma_service.query_chunks(long_query, "Python (programming language)")
        print(f"   ✓ Long query returned {len(long_query_results)} results")
        
        # Test 3: Special characters in query
        print("\n   Test 3: Special characters in query...")
        special_query = "query with special chars: @#$%^&*()_+-=[]{}|;':\",./<>?"
        special_results = chroma_service.query_chunks(special_query, "Python (programming language)")
        print(f"   ✓ Special characters query returned {len(special_results)} results")
        
        # Test 4: Unicode characters in query
        print("\n   Test 4: Unicode characters in query...")
        unicode_query = "query with unicode: αβγδε ζηθικλμν ξοπρστ υφχψω"
        unicode_results = chroma_service.query_chunks(unicode_query, "Python (programming language)")
        print(f"   ✓ Unicode query returned {len(unicode_results)} results")
        
        # Test 5: Query with exact article name that doesn't exist
        print("\n   Test 5: Query with exact non-existent article...")
        exact_nonexistent = chroma_service.query_chunks("test", "ExactNonExistentArticleName")
        assert len(exact_nonexistent) == 0, "Exact non-existent article should return empty"
        print(f"   ✓ Exact non-existent article returned {len(exact_nonexistent)} results (expected 0)")
        
        # Test 6: Query with case-sensitive article name
        print("\n   Test 6: Case-sensitive article name...")
        case_sensitive_results = chroma_service.query_chunks("test", "python (programming language)")  # lowercase
        print(f"   ✓ Case-sensitive query returned {len(case_sensitive_results)} results")
        
        print("\n🎉 Edge cases test completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Edge cases test failed: {e}")
        raise

def test_metadata_filtering_integration():
    """Test integration of metadata filtering with the full workflow."""
    print("\n" + "=" * 70)
    print("CHROMA METADATA FILTERING TEST: Integration")
    print("=" * 70)
    
    try:
        # Initialize ChromaService
        print("\n1. Initializing ChromaService...")
        chroma_service = ChromaService()
        
        # Create test chunks
        print("\n2. Creating test chunks...")
        test_chunks = create_test_chunks_with_complex_metadata()
        chroma_service.index_chunks(test_chunks)
        print("✓ Chunks indexed successfully")
        
        # Test integration scenarios
        print("\n3. Testing integration scenarios...")
        
        # Scenario 1: Multiple queries on same article
        print("\n   Scenario 1: Multiple queries on same article...")
        python_queries = [
            "programming language",
            "code development",
            "software engineering",
            "computer science"
        ]
        
        for i, query in enumerate(python_queries, 1):
            results = chroma_service.query_chunks(query, "Python (programming language)")
            assert all(result['metadata']['source_article'] == "Python (programming language)" for result in results), \
                f"All results from query {i} should be from Python article"
            print(f"     Query {i} ({query}): {len(results)} results, all from Python article")
        
        # Scenario 2: Cross-domain queries to verify isolation
        print("\n   Scenario 2: Cross-domain queries to verify isolation...")
        cross_domain_queries = [
            ("quantum physics", "Python (programming language)"),
            ("democracy government", "Quantum Mechanics"),
            ("python programming", "Aristotle"),
            ("aristotle philosophy", "Democracy")
        ]
        
        for i, (query, article) in enumerate(cross_domain_queries, 1):
            results = chroma_service.query_chunks(query, article)
            assert len(results) == 0, f"Cross-domain query {i} should return empty results"
            print(f"     Cross-domain query {i}: {len(results)} results (expected 0)")
        
        # Scenario 3: Verify metadata consistency across queries
        print("\n   Scenario 3: Verify metadata consistency...")
        all_python_results = []
        for query in ["programming", "language", "code"]:
            results = chroma_service.query_chunks(query, "Python (programming language)")
            all_python_results.extend(results)
        
        # Check that all results have consistent metadata structure
        for result in all_python_results:
            metadata = result['metadata']
            required_fields = ['source_article', 'chunk_id', 'section', 'category', 'subcategory']
            assert all(field in metadata for field in required_fields), \
                f"Result missing required metadata fields: {metadata}"
            assert metadata['source_article'] == "Python (programming language)", \
                f"Result from wrong article: {metadata['source_article']}"
        
        print(f"     ✓ All {len(all_python_results)} Python results have consistent metadata")
        
        print("\n🎉 Integration test completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Integration test failed: {e}")
        raise

if __name__ == "__main__":
    # Run all metadata filtering tests
    test_basic_metadata_filtering()
    test_cross_article_contamination_prevention()
    test_complex_metadata_filtering()
    test_metadata_filtering_performance()
    test_metadata_filtering_edge_cases()
    test_metadata_filtering_integration()
    
    print("\n" + "=" * 70)
    print("🎉 ALL METADATA FILTERING TESTS COMPLETED SUCCESSFULLY!")
    print("=" * 70)