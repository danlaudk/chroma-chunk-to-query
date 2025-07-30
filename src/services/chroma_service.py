"""
ChromaDB service for managing document embeddings and retrieval.
"""

import chromadb
from sentence_transformers import SentenceTransformer
from typing import List, Dict

from ..config.settings import (
    CHROMA_PERSISTENCE_DIR,
    EMBEDDING_MODEL_NAME
)

class ChromaService:
    def __init__(self):
        """Initialize ChromaDB client and embedding model."""
        self.client = chromadb.PersistentClient(path=CHROMA_PERSISTENCE_DIR)
        self.sentence_transformer = SentenceTransformer(EMBEDDING_MODEL_NAME)
        self.collection = self._get_or_create_collection()

    def _get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for the given texts."""
        return self.sentence_transformer.encode(texts).tolist()

    def _get_or_create_collection(self):
        """Get or create the Wikipedia chunks collection."""
        # Create a proper embedding function object
        embedding_function = chromadb.utils.embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=EMBEDDING_MODEL_NAME
        )
        
        return self.client.get_or_create_collection(
            name="wikipedia_chunks",
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

    def query_chunks(self, query_text: str, linked_wikipedia_title: str, top_k: int = 5) -> List[Dict]:
        """Query ChromaDB for semantically similar chunks."""
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