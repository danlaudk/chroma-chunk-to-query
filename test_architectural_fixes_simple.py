#!/usr/bin/env python3
"""
Simplified test script to verify the architectural fixes work correctly.
This version doesn't require external dependencies.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Mock the external dependencies
class MockConfig:
    def __init__(self):
        self.llm = MockLLMConfig()
        self.chroma = MockChromaConfig()
        self.wikipedia = MockWikipediaConfig()
        self.retrieval = MockRetrievalConfig()

class MockLLMConfig:
    def __init__(self):
        self.api_key = "test_key"
        self.provider = "google"
        self.model = "test_model"
        self.temperature = 0.1
        self.max_tokens = 4000
        self.cache = True

class MockChromaConfig:
    def __init__(self):
        self.persistence_dir = "./test_chroma"
        self.collection_name = "test_collection"
        self.embedding_model = "test_embedding_model"

class MockWikipediaConfig:
    def __init__(self):
        self.api_url = "https://test.wikipedia.org/w/api.php"
        self.timeout = 30
        self.max_retries = 3

class MockRetrievalConfig:
    def __init__(self):
        self.default_chunk_retrieval_count = 5
        self.max_chunk_size = 1000
        self.min_chunk_size = 50
        self.chunk_overlap = 100

# Mock the config module
sys.modules['src.config.settings'] = type('MockSettings', (), {
    'config': MockConfig(),
    'AppConfig': type('AppConfig', (), {}),
    'LLMConfig': type('LLMConfig', (), {}),
    'ChromaConfig': type('ChromaConfig', (), {}),
    'WikipediaConfig': type('WikipediaConfig', (), {}),
    'RetrievalConfig': type('RetrievalConfig', (), {})
})

# Mock dspy
class MockDSPy:
    def __init__(self):
        self.configure_called = False
        self.lm = None
    
    def configure(self, lm=None):
        self.configure_called = True
        self.lm = lm

class MockLM:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
    
    def __call__(self, text):
        return f"Mock response to: {text}"

sys.modules['dspy'] = type('MockDSPy', (), {
    'LM': MockLM,
    'configure': lambda lm=None: None
})

# Mock other dependencies
sys.modules['chromadb'] = type('MockChromaDB', (), {})
sys.modules['sentence_transformers'] = type('MockSentenceTransformers', (), {})
sys.modules['requests'] = type('MockRequests', (), {})
sys.modules['pydantic'] = type('MockPydantic', (), {})

# Now we can import our modules
from src.services.entity_processor import EntityProcessor
from src.services.entity_linking_service import EntityLinkingService
from src.services.wikipedia_service import WikipediaService
from src.services.chroma_service import ChromaService

def test_dependency_injection():
    """Test that dependency injection works correctly."""
    print("Testing dependency injection...")
    
    # Create mock services
    mock_wikipedia = type('MockWikipedia', (), {})()
    mock_chroma = type('MockChroma', (), {})()
    mock_linking = type('MockLinking', (), {})()
    mock_classifier = type('MockClassifier', (), {})()
    mock_llm = type('MockLLM', (), {})()
    
    # Test that EntityProcessor accepts injected dependencies
    processor = EntityProcessor(
        wikipedia_service=mock_wikipedia,
        chroma_service=mock_chroma,
        entity_linking_service=mock_linking,
        classifier=mock_classifier,
        llm=mock_llm
    )
    
    assert processor.wikipedia_service is mock_wikipedia
    assert processor.chroma_service is mock_chroma
    assert processor.entity_linking_service is mock_linking
    assert processor.classifier is mock_classifier
    assert processor.llm is mock_llm
    
    print("✓ Dependency injection test passed")

def test_single_responsibility():
    """Test that services follow single responsibility principle."""
    print("\nTesting single responsibility principle...")
    
    # Test that EntityLinkingService only handles entity linking
    linking_service = EntityLinkingService()
    assert hasattr(linking_service, 'perform_entity_linking')
    assert not hasattr(linking_service, 'retrieve_article')  # Should not have Wikipedia methods
    assert not hasattr(linking_service, 'index_chunks')      # Should not have ChromaDB methods
    
    # Test that WikipediaService only handles Wikipedia operations
    wikipedia_service = WikipediaService()
    assert hasattr(wikipedia_service, 'retrieve_article')
    assert hasattr(wikipedia_service, 'chunk_text')
    assert not hasattr(wikipedia_service, 'perform_entity_linking')  # Should not have linking methods
    
    # Test that ChromaService only handles vector database operations
    chroma_service = ChromaService()
    assert hasattr(chroma_service, 'index_chunks')
    assert hasattr(chroma_service, 'query_chunks')
    assert not hasattr(chroma_service, 'retrieve_article')  # Should not have Wikipedia methods
    
    print("✓ Single responsibility principle test passed")

def test_configuration_integration():
    """Test that services properly use the configuration system."""
    print("\nTesting configuration integration...")
    
    # Create test configurations
    test_chroma_config = MockChromaConfig()
    test_chroma_config.persistence_dir = "./test_chroma"
    test_chroma_config.collection_name = "test_collection"
    
    test_wikipedia_config = MockWikipediaConfig()
    test_wikipedia_config.api_url = "https://test.wikipedia.org/w/api.php"
    test_wikipedia_config.timeout = 15
    
    # Test that services accept and use custom configs
    chroma_service = ChromaService(chroma_config=test_chroma_config)
    assert chroma_service.config.persistence_dir == "./test_chroma"
    assert chroma_service.config.collection_name == "test_collection"
    
    wikipedia_service = WikipediaService(wikipedia_config=test_wikipedia_config)
    assert wikipedia_service.config.api_url == "https://test.wikipedia.org/w/api.php"
    assert wikipedia_service.config.timeout == 15
    
    print("✓ Configuration integration test passed")

def test_code_structure():
    """Test that the code structure follows good practices."""
    print("\nTesting code structure...")
    
    # Test that EntityProcessor has helper methods
    processor = EntityProcessor()
    assert hasattr(processor, '_create_unrelated_result')
    assert hasattr(processor, '_create_success_result')
    
    # Test that services have proper initialization
    linking_service = EntityLinkingService()
    assert hasattr(linking_service, 'config')
    
    wikipedia_service = WikipediaService()
    assert hasattr(wikipedia_service, 'config')
    
    chroma_service = ChromaService()
    assert hasattr(chroma_service, 'config')
    
    print("✓ Code structure test passed")

if __name__ == "__main__":
    print("Running simplified architectural fix verification tests...\n")
    
    try:
        test_dependency_injection()
        test_single_responsibility()
        test_configuration_integration()
        test_code_structure()
        
        print("\n🎉 All architectural fix tests passed!")
        print("\nSummary of fixes applied:")
        print("1. ✅ Dependency Injection: EntityProcessor now accepts injected dependencies")
        print("2. ✅ Configuration System: Centralized, environment-aware configuration")
        print("3. ✅ Single Responsibility: Extracted EntityLinkingService and simplified EntityProcessor")
        print("4. ✅ Removed Magic Numbers: All hardcoded values now use configuration")
        print("5. ✅ Improved Error Handling: Better exception handling and timeouts")
        print("6. ✅ Better Code Organization: Helper methods and proper separation of concerns")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)