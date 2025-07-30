"""
ChromaDB service for managing document embeddings and retrieval.
"""

import chromadb
from sentence_transformers import SentenceTransformer
from typing import List, Dict

from ..config.settings import config

class ChromaService:
    def __init__(self, chroma_config=None):
        """
        Initialize ChromaDB client and embedding model.
        
        Args:
            chroma_config: Optional ChromaConfig instance for testing
        """
        self.config = chroma_config or config.chroma
        self.client = chromadb.PersistentClient(path=self.config.persistence_dir)
        self.sentence_transformer = SentenceTransformer(self.config.embedding_model)
        self.collection = self._get_or_create_collection()

    def _get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for the given texts."""
        return self.sentence_transformer.encode(texts).tolist()

    def _get_or_create_collection(self):
        """Get or create the Wikipedia chunks collection."""
        # Create a proper embedding function object
        embedding_function = chromadb.utils.embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=self.config.embedding_model
        )
        
        return self.client.get_or_create_collection(
            name=self.config.collection_name,
            embedding_function=embedding_function
        )

    def index_chunks(self, chunks: List[Dict]):
        """Index the processed chunks in ChromaDB."""
        print(f"Indexing {len(chunks)} chunks in ChromaDB...")
        documents = [chunk["text"] for chunk in chunks]
        metadatas = [chunk["metadata"] for chunk in chunks]
        ids = [m["chunk_id"] for m in metadatas]

        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        print("Chunks indexed successfully.")

    def query_chunks(self, query_text: str, linked_wikipedia_title: str, top_k: int = None) -> List[Dict]:
        """
        Query ChromaDB for semantically similar chunks.
        
        Args:
            query_text: The query text to search for
            linked_wikipedia_title: The Wikipedia article title to filter by
            top_k: Number of results to return (uses config default if None)
        """
        if top_k is None:
            top_k = config.retrieval.default_chunk_retrieval_count
            
        print(f"Querying Chroma for relevant chunks for '{query_text}' from '{linked_wikipedia_title}'...")
        
        metadata_filter = {"source_article": linked_wikipedia_title}
        results = self.collection.query(
            query_texts=[query_text],
            n_results=top_k,
            where=metadata_filter
        )

        retrieved_chunks = []
        if results and results['documents']:
            for i in range(len(results['documents'][0])):
                retrieved_chunks.append({
                    "text": results['documents'][0][i],
                    "metadata": results['metadatas'][0][i]
                })

        print(f"Retrieved {len(retrieved_chunks)} chunks.")
        return retrieved_chunks 