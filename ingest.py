"""
ingest.py
Milestone 3: Document Ingestion and Chunking

Loads .txt files from the documents/ folder, cleans them,
and splits them into chunks of 300 characters with 50 character overlap.

Based on planning.md spec:
- Chunk size: 300 characters
- Overlap: 50 characters
- Source: one .txt file per professor
"""

import os


# ── 1. LOAD ──────────────────────────────────────────────────────────────────

def load_documents(folder_path="/Users/fidantahirli/Documents/GitHub/ai201-project1-unofficial-guide-starter/documents"):
    """
    Reads every .txt file in the folder.
    Returns a list of dicts: { "text": ..., "source": filename }
    """
    documents = []

    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            filepath = os.path.join(folder_path, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read()
            documents.append({
                "text": text,
                "source": filename  # e.g. "prof_john_smith.txt"
            })
            print(f"Loaded: {filename} ({len(text)} characters)")

    print(f"\nTotal documents loaded: {len(documents)}")
    return documents


# ── 2. CLEAN ─────────────────────────────────────────────────────────────────

def clean_text(text):
    """
    Removes junk from raw copy-pasted RateMyProfessors text.
    Keeps: review content, professor name, course info
    Removes: extra blank lines, leading/trailing whitespace
    """
    lines = text.splitlines()
    cleaned_lines = []

    for line in lines:
        line = line.strip()

        # Skip empty lines and common RMP boilerplate
        if not line:
            continue
        if line.lower() in ["read more", "helpful", "not helpful", "report"]:
            continue
        if line.startswith("http"):
            continue

        cleaned_lines.append(line)

    return "\n".join(cleaned_lines)


# ── 3. CHUNK ─────────────────────────────────────────────────────────────────

def chunk_text(text, source, chunk_size=300, overlap=50):
    """
    Splits text into chunks of `chunk_size` characters,
    with `overlap` characters shared between neighboring chunks.

    Returns a list of dicts: { "text": ..., "source": ... }
    """
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if len(chunk) > 20:  # skip tiny leftover fragments
            chunks.append({
                "text": chunk,
                "source": source
            })

        start += chunk_size - overlap  # move forward, leaving overlap behind

    return chunks


# ── 4. PIPELINE ───────────────────────────────────────────────────────────────

def run_pipeline(folder_path="documents"):
    """
    Full ingestion pipeline:
    Load → Clean → Chunk → Return all chunks
    """
    documents = load_documents(folder_path)
    all_chunks = []

    for doc in documents:
        cleaned = clean_text(doc["text"])
        chunks = chunk_text(cleaned, source=doc["source"])
        all_chunks.extend(chunks)

    print(f"\nTotal chunks produced: {len(all_chunks)}")
    return all_chunks


# ── 5. INSPECT (run this to verify your chunks look good) ────────────────────

if __name__ == "__main__":
    chunks = run_pipeline("documents")

    print("\n── Sample Chunks ──────────────────────────────")
    for i, chunk in enumerate(chunks[:5]):
        print(f"\nChunk {i+1} | Source: {chunk['source']}")
        print(f"Length: {len(chunk['text'])} chars")
        print(f"Text: {chunk['text']}")
        print("─" * 50)

    print(f"\nTotal chunks: {len(chunks)}")
    print("If this number is between 50 and 2000, you're in good shape!")