"""
retriever.py
Milestone 4: Embedding and Retrieval

Takes chunks from ingest.py, converts them to vectors using
all-MiniLM-L6-v2, stores them in ChromaDB, and retrieves
the top-5 most relevant chunks for any query.

Based on planning.md:
- Embedding model: all-MiniLM-L6-v2 via sentence-transformers
- Vector store: ChromaDB (local)
- Top-k: 5
"""

import chromadb
from sentence_transformers import SentenceTransformer
from ingest import run_pipeline


# ── 1. SETUP ─────────────────────────────────────────────────────────────────

# Load the embedding model (runs locally, no API key needed)
print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

# Set up ChromaDB — stores everything locally in a folder called "chroma_db"
client = chromadb.PersistentClient(path="chroma_db")

# Create a collection (like a table in a regular database)
# get_or_create means it won't crash if you run this twice
collection = client.get_or_create_collection(name="professor_reviews")


# ── 2. EMBED AND STORE ────────────────────────────────────────────────────────

def embed_and_store(chunks):
    """
    Takes all chunks from ingest.py, converts each one to a vector,
    and stores it in ChromaDB with its source filename as metadata.
    """

    # Check if already stored — don't re-embed if collection already has data
    if collection.count() > 0:
        print(f"Collection already has {collection.count()} chunks. Skipping embedding.")
        return

    print(f"Embedding {len(chunks)} chunks...")

    texts = [chunk["text"] for chunk in chunks]
    sources = [chunk["source"] for chunk in chunks]

    # Convert all texts to vectors at once
    embeddings = model.encode(texts, show_progress_bar=True)

    # Store in ChromaDB — needs ids, embeddings, documents, and metadata
    collection.add(
        ids=[f"chunk_{i}" for i in range(len(chunks))],
        embeddings=embeddings.tolist(),
        documents=texts,
        metadatas=[{"source": source} for source in sources]
    )

    print(f"Stored {len(chunks)} chunks in ChromaDB!")


# ── 3. RETRIEVE ───────────────────────────────────────────────────────────────

def retrieve(query, k=5):
    """
    Takes a user question, converts it to a vector,
    and finds the top-k most similar chunks in ChromaDB.

    Returns a list of dicts: { "text": ..., "source": ... , "distance": ... }
    """

    # Convert the query to a vector using the same model
    query_embedding = model.encode([query])[0]

    # Search ChromaDB for the closest chunks
    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=k
    )

    # Format results nicely
    chunks = []
    for i in range(len(results["documents"][0])):
        chunks.append({
            "text": results["documents"][0][i],
            "source": results["metadatas"][0][i]["source"],
            "distance": round(results["distances"][0][i], 3)
        })

    return chunks


# ── 4. TEST RETRIEVAL (run this to verify search works) ──────────────────────

if __name__ == "__main__":

    # Step 1: Load and embed all chunks
    chunks = run_pipeline("documents")
    embed_and_store(chunks)

    print("\n── Testing Retrieval ──────────────────────────────")

    # Test with 3 of your evaluation questions from planning.md
    test_queries = [
        "Which professor curves their exams?",
        "Which professor is best for office hours?",
        "Which professor gives the most homework?"
    ]

    for query in test_queries:
        print(f"\nQuery: {query}")
        print("─" * 50)
        results = retrieve(query)
        for i, result in enumerate(results):
            print(f"Result {i+1} | Source: {result['source']} | Distance: {result['distance']}")
            print(f"Text: {result['text'][:150]}...")
            print()