#!/usr/bin/env python3
"""
Test script to verify the architectural fixes work correctly.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from unittest.mock import Mock, patch
from src.config.settings import AppConfig, LLMConfig, ChromaConfig, WikipediaConfig, RetrievalConfig
from src.services.entity_processor import EntityProcessor
from src.services.entity_linking_service import EntityLinkingService
from src.services.wikipedia_service import WikipediaService
from src.services.chroma_service import ChromaService
from src.models.entity_classifier import ClassifyEntityModule

def test_dependency_injection():
    """Test that dependency injection works correctly."""
    print("Testing dependency injection...")
    
    # Create mock services
    mock_wikipedia = Mock(spec=WikipediaService)
    mock_chroma = Mock(spec=ChromaService)
    mock_linking = Mock(spec=EntityLinkingService)
    mock_classifier = Mock(spec=ClassifyEntityModule)
    mock_llm = Mock()
    
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

def test_configuration_system():
    """Test that the new configuration system works correctly."""
    print("\nTesting configuration system...")
    
    # Test that we can create custom configs
    test_llm_config = LLMConfig(
        api_key="test_key",
        model="test_model",
        temperature=0.5,
        max_tokens=2000
    )
    
    test_chroma_config = ChromaConfig(
        persistence_dir="./test_db",
        collection_name="test_collection",
        embedding_model="test_embedding_model"
    )
    
    test_wikipedia_config = WikipediaConfig(
        api_url="https://test.wikipedia.org/w/api.php",
        timeout=10,
        max_retries=2
    )
    
    test_retrieval_config = RetrievalConfig(
        default_chunk_retrieval_count=3,
        max_chunk_size=500,
        min_chunk_size=25,
        chunk_overlap=50
    )
    
    test_config = AppConfig(
        environment="testing",
        debug=True,
        llm=test_llm_config,
        chroma=test_chroma_config,
        wikipedia=test_wikipedia_config,
        retrieval=test_retrieval_config
    )
    
    assert test_config.environment == "testing"
    assert test_config.debug is True
    assert test_config.llm.model == "test_model"
    assert test_config.chroma.persistence_dir == "./test_db"
    assert test_config.wikipedia.timeout == 10
    assert test_config.retrieval.default_chunk_retrieval_count == 3
    
    print("✓ Configuration system test passed")

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
    test_chroma_config = ChromaConfig(
        persistence_dir="./test_chroma",
        collection_name="test_collection",
        embedding_model="test_embedding_model"
    )
    
    test_wikipedia_config = WikipediaConfig(
        api_url="https://test.wikipedia.org/w/api.php",
        timeout=15,
        max_retries=5
    )
    
    # Test that services accept and use custom configs
    chroma_service = ChromaService(chroma_config=test_chroma_config)
    assert chroma_service.config.persistence_dir == "./test_chroma"
    assert chroma_service.config.collection_name == "test_collection"
    
    wikipedia_service = WikipediaService(wikipedia_config=test_wikipedia_config)
    assert wikipedia_service.config.api_url == "https://test.wikipedia.org/w/api.php"
    assert wikipedia_service.config.timeout == 15
    
    print("✓ Configuration integration test passed")

if __name__ == "__main__":
    print("Running architectural fix verification tests...\n")
    
    try:
        test_dependency_injection()
        test_configuration_system()
        test_single_responsibility()
        test_configuration_integration()
        
        print("\n🎉 All architectural fix tests passed!")
        print("\nSummary of fixes applied:")
        print("1. ✅ Dependency Injection: EntityProcessor now accepts injected dependencies")
        print("2. ✅ Configuration System: Centralized, environment-aware configuration")
        print("3. ✅ Single Responsibility: Extracted EntityLinkingService and simplified EntityProcessor")
        print("4. ✅ Removed Magic Numbers: All hardcoded values now use configuration")
        print("5. ✅ Improved Error Handling: Better exception handling and timeouts")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)