# litellm access to one service (without dspy??) ??
# entity linking service using claude and chatgpt (URL/name) (wikipedia api investigate)
# update dspy to 3.0.2
# wide variation LLM to generate retrieval query
# chromadb test teardown usint unittest
# chromadb error edge case 
#    2. Testing empty chunks list...
#     Indexing 0 chunks in ChromaDB...
#        ⚠ Empty chunks list caused error: Non-empty lists are required for ['ids', 'metadatas', 'documents'] in add.

# Pseudocode for a Robust Entity Classification and Wikipedia Matching System

# This pseudocode outlines the architecture for classifying named entities
# and matching them to relevant Wikipedia chunks, following the principles
# of robust methods and tools.

# --- Configuration and Initialization ---
# Define constants and initialize services
# Assume necessary libraries (e.g., dspy, chromadb, sentence_transformers, requests, beautifulsoup4) are installed

# Initialize DSPy (Language Model and Retriever)
# Replace with your actual LLM (e.g., OpenAI, local model)
# LM_MODEL = dspy.OpenAI(model="gpt-3.5-turbo")
# dspy.configure(lm=LM_MODEL)

# Initialize ChromaDB client
# This can be in-memory, persistent, or client-server mode
# CHROMA_CLIENT = chromadb.Client() # In-memory client for simplicity
# Or for persistent storage:
# CHROMA_CLIENT = chromadb.PersistentClient(path="./chroma_db")

# Get or create the Chroma collection for Wikipedia chunks
# Ensure to specify the embedding function for consistency
# EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
# from sentence_transformers import SentenceTransformer
# sentence_transformer_model = SentenceTransformer(EMBEDDING_MODEL_NAME)

# def get_embeddings(texts):
#     return sentence_transformer_model.encode(texts).tolist()

# WIKIPEDIA_COLLECTION = CHROMA_CLIENT.get_or_create_collection(
#     name="wikipedia_chunks",
#     embedding_function=get_embeddings # Pass the custom embedding function
# )

# --- DSPy Modules Definition ---
# Define DSPy modules for the LLM-driven parts of the pipeline

# Module for classifying the entity type
class ClassifyEntityModule(dspy.Module):
    def __init__(self):
        super().__init__()
        # Define the signature for the classification task
        # Inputs: term, linked_wikipedia_title, retrieved_chunks
        # Outputs: entity_type (e.g., 'philosopher', 'concept', 'unrelated'), explanation
        self.prog = dspy.ChainOfThought(
            "term, linked_wikipedia_title, retrieved_chunks -> entity_type, explanation"
        )

    def forward(self, term, linked_wikipedia_title, retrieved_chunks):
        # The LLM will synthesize information from the inputs to classify
        # the entity and provide an explanation.
        prediction = self.prog(
            term=term,
            linked_wikipedia_title=linked_wikipedia_title,
            retrieved_chunks=retrieved_chunks
        )
        return prediction.entity_type, prediction.explanation

# --- Core Functions ---

def retrieve_wikipedia_article(page_title: str) -> str:
    """
    Retrieves the full text content of a Wikipedia article using a WikipediaReader-like approach.
    """
    print(f"Retrieving Wikipedia article: {page_title}")
    # In a real implementation, this would use LlamaIndex's WikipediaReader or a direct API call.
    # For pseudocode, we'll simulate fetching.
    try:
        # Using requests to fetch from Wikipedia API for demonstration
        # This is a simplified fetch, WikipediaReader handles more complexities.
        API_URL = "https://en.wikipedia.org/w/api.php"
        params = {
            "action": "query",
            "format": "json",
            "titles": page_title,
            "prop": "extracts",
            "explaintext": True,
            "exintro": False, # Get full extract, not just intro
            "redirects": 1 # Follow redirects
        }
        response = requests.get(API_URL, params=params)
        data = response.json()
        page = next(iter(data['query']['pages'].values()))
        if 'extract' in page:
            return page['extract']
        else:
            print(f"No extract found for page: {page_title}")
            return ""
    except Exception as e:
        print(f"Error retrieving Wikipedia article '{page_title}': {e}")
        return ""

def chunk_text(text: str, source_metadata: dict) -> list[dict]:
    """
    Performs robust, layered text chunking on the Wikipedia article.
    First, content-aware (by paragraph/section), then optionally semantic.
    Attaches relevant metadata to each chunk.
    """
    print("Chunking text and adding metadata...")
    chunks = []
    # Example: Simple paragraph-based chunking for pseudocode
    paragraphs = text.split('\n\n') # Split by double newline for paragraphs
    for i, para in enumerate(paragraphs):
        if para.strip(): # Ensure chunk is not empty
            chunk_metadata = {
                "source_article": source_metadata.get("article_title"),
                "chunk_id": f"{source_metadata.get('article_title', 'unknown')}_chunk_{i}",
                "section_heading": "General" # Placeholder, real impl would parse headings
            }
            # In a real system, you'd apply semantic chunking here if paragraphs are too long
            chunks.append({"text": para.strip(), "metadata": chunk_metadata})
    print(f"Created {len(chunks)} chunks.")
    return chunks

def index_chunks_in_chroma(chunks: list[dict]):
    """
    Indexes the processed chunks in ChromaDB.
    """
    print(f"Indexing {len(chunks)} chunks in ChromaDB...")
    documents = [chunk["text"] for chunk in chunks]
    metadatas = [chunk["metadata"] for chunk in chunks]
    ids = [m["chunk_id"] for m in metadatas] # Use chunk_id as document ID

    # Add documents to the collection. Chroma will handle embedding internally
    # if an embedding function was provided during collection creation.
    # WIKIPEDIA_COLLECTION.add(
    #     documents=documents,
    #     metadatas=metadatas,
    #     ids=ids
    # )
    print("Chunks indexed successfully.")

def query_chroma_for_relevant_chunks(
    query_text: str,
    linked_wikipedia_title: str,
    top_k: int = 5
) -> list[dict]:
    """
    Queries ChromaDB for semantically similar chunks, applying metadata filtering.
    """
    print(f"Querying Chroma for relevant chunks for '{query_text}' from '{linked_wikipedia_title}'...")
    # Define metadata filter to restrict search to the specific Wikipedia article
    metadata_filter = {"source_article": linked_wikipedia_title}

    # Perform the query
    # results = WIKIPEDIA_COLLECTION.query(
    #     query_texts=[query_text],
    #     n_results=top_k,
    #     where=metadata_filter
    # )

    # Placeholder for results structure
    mock_results = {
        "documents": [
            [f"Chunk 1 from {linked_wikipedia_title} about {query_text}"],
            [f"Chunk 2 from {linked_wikipedia_title} discussing aspects of {query_text}"],
            [f"Chunk 3 from {linked_wikipedia_title} providing context on {query_text}"]
        ],
        "metadatas": [
            [{"source_article": linked_wikipedia_title, "section_heading": "Introduction"}],
            [{"source_article": linked_wikipedia_title, "section_heading": "Key Concepts"}],
            [{"source_article": linked_wikipedia_title, "section_heading": "Impact"}]
        ]
    }

    retrieved_chunks_with_metadata = []
    # if results and results['documents']:
    #     for i in range(len(results['documents'][0])):
    #         retrieved_chunks_with_metadata.append({
    #             "text": results['documents'][0][i],
    #             "metadata": results['metadatas'][0][i]
    #         })
    # Mocking the actual retrieval for pseudocode
    for i in range(len(mock_results['documents'][0])):
        retrieved_chunks_with_metadata.append({
            "text": mock_results['documents'][0][i],
            "metadata": mock_results['metadatas'][0][i]
        })

    print(f"Retrieved {len(retrieved_chunks_with_metadata)} chunks.")
    return retrieved_chunks_with_metadata

# --- Main Orchestration Logic ---

def classify_and_match_entity(term: str):
    """
    Main function to orchestrate the entity classification and Wikipedia matching process.
    """
    print(f"\n--- Processing Term: '{term}' ---")

    # Step 1: Entity Linking
    # This is the crucial pre-processing step for disambiguation.
    entity_link_info = perform_entity_linking(term) # this is in a separate API service
    linked_wikipedia_title = entity_link_info['wikipedia_page_title']
    wikidata_id = entity_link_info['wikidata_id']
    is_unrelated = entity_link_info['is_unrelated']

    if is_unrelated or not linked_wikipedia_title:
        print(f"Term '{term}' could not be confidently linked to a Wikipedia page. Classifying as 'unrelated'.")
        return {
            "term": term,
            "entity_type": "unrelated",
            "explanation": f"The term '{term}' did not confidently link to a specific known entity in Wikipedia/Wikidata.",
            "matched_chunks": []
        }

    # Step 2: Retrieve Wikipedia Article
    article_content = retrieve_wikipedia_article(linked_wikipedia_title)
    if not article_content:
        print(f"Could not retrieve content for '{linked_wikipedia_title}'. Classifying as 'unrelated'.")
        return {
            "term": term,
            "entity_type": "unrelated",
            "explanation": f"Wikipedia article for '{linked_wikipedia_title}' could not be retrieved.",
            "matched_chunks": []
        }

    # Step 3: Chunk Text and Prepare for Indexing
    # Metadata includes source article title, section, etc.
    processed_chunks = chunk_text(article_content, {"article_title": linked_wikipedia_title})

    # Step 4: Index Chunks in Chroma (if not already indexed)
    # In a production system, this would be a separate ingestion pipeline,
    # only run when new articles are added or updated.
    # For this pseudocode, we assume indexing happens as part of the flow.
    # index_chunks_in_chroma(processed_chunks)

    # Step 5: Query Chroma for Relevant Chunks (with metadata filtering)
    # The query text can be the original term or a refined query.
    relevant_chunks = query_chroma_for_relevant_chunks(term, linked_wikipedia_title)

    # Step 6: Classify Entity Type using DSPy Module
    classify_module = ClassifyEntityModule()
    entity_type, explanation = classify_module.forward(
        term=term,
        linked_wikipedia_title=linked_wikipedia_title,
        retrieved_chunks=[c["text"] for c in relevant_chunks] # Pass only text to LLM
    )

    print(f"\n--- Results for '{term}' ---")
    print(f"Linked Wikipedia Title: {linked_wikipedia_title}")
    print(f"Wikidata ID: {wikidata_id}")
    print(f"Classified Entity Type: {entity_type}")
    print(f"Classification Explanation: {explanation}")
    print(f"Number of Matched Chunks: {len(relevant_chunks)}")

    return {
        "term": term,
        "linked_wikipedia_title": linked_wikipedia_title,
        "wikidata_id": wikidata_id,
        "entity_type": entity_type,
        "explanation": explanation,
        "matched_chunks": relevant_chunks
    }

# --- Example Usage ---
# To run this pseudocode, you would need to uncomment and properly configure
# the DSPy and ChromaDB initializations.