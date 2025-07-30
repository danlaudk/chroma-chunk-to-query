"""
ChromaDB service for managing document embeddings and retrieval.
"""

import chromadb
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any, Optional, Union
import logging

from ..config.settings import (
    CHROMA_PERSISTENCE_DIR,
    EMBEDDING_MODEL_NAME
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChromaService:
    def __init__(self):
        """Initialize ChromaDB client and embedding model."""
        try:
            self.client = chromadb.PersistentClient(path=CHROMA_PERSISTENCE_DIR)
            self.sentence_transformer = SentenceTransformer(EMBEDDING_MODEL_NAME)
            self.collection = self._get_or_create_collection()
            logger.info("ChromaService initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize ChromaService: {e}")
            raise

    def _get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for the given texts."""
        try:
            return self.sentence_transformer.encode(texts).tolist()
        except Exception as e:
            logger.error(f"Failed to generate embeddings: {e}")
            raise

    def _get_or_create_collection(self):
        """Get or create the Wikipedia chunks collection."""
        try:
            # Create a proper embedding function object
            embedding_function = chromadb.utils.embedding_functions.SentenceTransformerEmbeddingFunction(
                model_name=EMBEDDING_MODEL_NAME
            )
            
            collection = self.client.get_or_create_collection(
                name="wikipedia_chunks",
                embedding_function=embedding_function
            )
            logger.info("Collection retrieved/created successfully")
            return collection
        except Exception as e:
            logger.error(f"Failed to get or create collection: {e}")
            raise

    def index_chunks(self, chunks: List[Dict[str, Any]]) -> None:
        """Index the processed chunks in ChromaDB."""
        if not chunks:
            logger.warning("No chunks provided for indexing")
            return
            
        try:
            logger.info(f"Indexing {len(chunks)} chunks in ChromaDB...")
            
            # Validate chunk structure
            documents = []
            metadatas = []
            ids = []
            
            for i, chunk in enumerate(chunks):
                if not isinstance(chunk, dict) or 'text' not in chunk or 'metadata' not in chunk:
                    logger.warning(f"Invalid chunk structure at index {i}: {chunk}")
                    continue
                    
                text = chunk['text']
                metadata = chunk['metadata']
                
                # Validate text
                if not text or not isinstance(text, str):
                    logger.warning(f"Invalid text in chunk {i}: {text}")
                    continue
                    
                # Validate metadata
                if not isinstance(metadata, dict) or 'chunk_id' not in metadata:
                    logger.warning(f"Invalid metadata in chunk {i}: {metadata}")
                    continue
                
                documents.append(text)
                metadatas.append(metadata)
                ids.append(metadata['chunk_id'])

            if documents:
                self.collection.add(
                    documents=documents,
                    metadatas=metadatas,
                    ids=ids
                )
                logger.info(f"Successfully indexed {len(documents)} chunks")
            else:
                logger.warning("No valid chunks to index")
                
        except Exception as e:
            logger.error(f"Failed to index chunks: {e}")
            raise

    def query_chunks(self, query_text: str, linked_wikipedia_title: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Query ChromaDB for semantically similar chunks with metadata filtering."""
        try:
            logger.info(f"Querying Chroma for relevant chunks for '{query_text}' from '{linked_wikipedia_title}'...")
            
            if not query_text or not linked_wikipedia_title:
                logger.warning("Empty query text or article title provided")
                return []
            
            metadata_filter = {"source_article": linked_wikipedia_title}
            results = self.collection.query(
                query_texts=[query_text],
                n_results=top_k,
                where=metadata_filter
            )

            retrieved_chunks = []
            if results and results['documents'] and results['documents'][0]:
                for i in range(len(results['documents'][0])):
                    retrieved_chunks.append({
                        "text": results['documents'][0][i],
                        "metadata": results['metadatas'][0][i],
                        "distance": results['distances'][0][i] if 'distances' in results else None
                    })

            logger.info(f"Retrieved {len(retrieved_chunks)} chunks")
            return retrieved_chunks
            
        except Exception as e:
            logger.error(f"Failed to query chunks: {e}")
            return []

    def query_with_complex_filter(self, query_text: str, metadata_filter: Dict[str, Any], top_k: int = 5) -> List[Dict[str, Any]]:
        """Query ChromaDB with complex metadata filtering criteria."""
        try:
            logger.info(f"Querying with complex filter: {metadata_filter}")
            
            if not query_text:
                logger.warning("Empty query text provided")
                return []
            
            results = self.collection.query(
                query_texts=[query_text],
                n_results=top_k,
                where=metadata_filter
            )

            retrieved_chunks = []
            if results and results['documents'] and results['documents'][0]:
                for i in range(len(results['documents'][0])):
                    retrieved_chunks.append({
                        "text": results['documents'][0][i],
                        "metadata": results['metadatas'][0][i],
                        "distance": results['distances'][0][i] if 'distances' in results else None
                    })

            logger.info(f"Retrieved {len(retrieved_chunks)} chunks with complex filter")
            return retrieved_chunks
            
        except Exception as e:
            logger.error(f"Failed to query with complex filter: {e}")
            return []

    def query_by_category(self, query_text: str, category: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Query chunks filtered by category."""
        return self.query_with_complex_filter(query_text, {"category": category}, top_k)

    def query_by_domain(self, query_text: str, domain: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Query chunks filtered by domain."""
        return self.query_with_complex_filter(query_text, {"domain": domain}, top_k)

    def query_by_difficulty(self, query_text: str, difficulty: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Query chunks filtered by difficulty level."""
        return self.query_with_complex_filter(query_text, {"difficulty": difficulty}, top_k)

    def query_with_multiple_filters(self, query_text: str, filters: Dict[str, Any], top_k: int = 5) -> List[Dict[str, Any]]:
        """Query chunks with multiple metadata filters."""
        return self.query_with_complex_filter(query_text, filters, top_k)

    def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about the collection."""
        try:
            count = self.collection.count()
            return {
                "total_chunks": count,
                "collection_name": self.collection.name
            }
        except Exception as e:
            logger.error(f"Failed to get collection stats: {e}")
            return {"error": str(e)}

    def delete_chunks_by_article(self, article_title: str) -> bool:
        """Delete all chunks from a specific article."""
        try:
            logger.info(f"Deleting chunks for article: {article_title}")
            self.collection.delete(where={"source_article": article_title})
            logger.info(f"Successfully deleted chunks for article: {article_title}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete chunks for article {article_title}: {e}")
            return False

    def update_chunk_metadata(self, chunk_id: str, new_metadata: Dict[str, Any]) -> bool:
        """Update metadata for a specific chunk."""
        try:
            logger.info(f"Updating metadata for chunk: {chunk_id}")
            # Note: ChromaDB doesn't have a direct update method, so we need to delete and re-add
            # This is a limitation of the current ChromaDB version
            logger.warning("ChromaDB doesn't support direct metadata updates. Consider re-indexing the chunk.")
            return False
        except Exception as e:
            logger.error(f"Failed to update metadata for chunk {chunk_id}: {e}")
            return False

    def search_similar_chunks(self, text: str, top_k: int = 5, exclude_article: Optional[str] = None) -> List[Dict[str, Any]]:
        """Search for similar chunks without article filtering, optionally excluding a specific article."""
        try:
            logger.info(f"Searching for similar chunks to: {text[:50]}...")
            
            if exclude_article:
                # Use NOT operator to exclude specific article
                where_filter = {"source_article": {"$ne": exclude_article}}
                results = self.collection.query(
                    query_texts=[text],
                    n_results=top_k,
                    where=where_filter
                )
            else:
                results = self.collection.query(
                    query_texts=[text],
                    n_results=top_k
                )

            retrieved_chunks = []
            if results and results['documents'] and results['documents'][0]:
                for i in range(len(results['documents'][0])):
                    retrieved_chunks.append({
                        "text": results['documents'][0][i],
                        "metadata": results['metadatas'][0][i],
                        "distance": results['distances'][0][i] if 'distances' in results else None
                    })

            logger.info(f"Found {len(retrieved_chunks)} similar chunks")
            return retrieved_chunks
            
        except Exception as e:
            logger.error(f"Failed to search similar chunks: {e}")
            return []

    def validate_metadata_structure(self, metadata: Dict[str, Any]) -> bool:
        """Validate that metadata has the required structure."""
        required_fields = ['chunk_id', 'source_article']
        return all(field in metadata for field in required_fields)

    def get_articles_in_collection(self) -> List[str]:
        """Get list of all unique article titles in the collection."""
        try:
            # Get all documents to extract unique article titles
            results = self.collection.get()
            if not results or not results['metadatas']:
                return []
            
            articles = set()
            for metadata in results['metadatas']:
                if metadata and 'source_article' in metadata:
                    articles.add(metadata['source_article'])
            
            return list(articles)
        except Exception as e:
            logger.error(f"Failed to get articles in collection: {e}")
            return [] 