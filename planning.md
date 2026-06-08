# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

i chose rate my professor as source and specifically university i attented to and computer science department of that university. This knowledge is valuable because it gives students insigts about what professors are like and who to avoid to take the class of. I think it even could be perspective to new students to even attend the university based on how its computer science department is doing.

---

## Documents

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 |Rate My Professors |Reviews for CS Professor|Mark Blair |https://www.ratemyprofessors.com/professor/2099395
| 2 | Rate My Professors| Reviews for CS Professor |Jeremy Cannell |https://www.ratemyprofessors.com/professor/98098
| 3 | Rate My Professors|Reviews for CS Professor  |Tajmilur Rahman |https://www.ratemyprofessors.com/professor/2664280
| 4 | Rate My Professors|Reviews for CS Professor  |Mei-Hue Tang |https://www.ratemyprofessors.com/professor/282230
| 5 | Rate My Professors|Reviews for CS Professor  |David Marino |https://www.ratemyprofessors.com/professor/567007
| 6 |Rate My Professors |Reviews for CS Professor  |John Coffman |https://www.ratemyprofessors.com/professor/2692664
| 7 |Rate My Professors | Reviews for CS Professor |Dadmehr Rahbari |https://www.ratemyprofessors.com/professor/2932444
| 8 |Rate My Professors|Reviews for CS Professor  | Scott Steinbrink |https://www.ratemyprofessors.com/professor/2836844
| 9 |Rate My Professors |Reviews for CS Professor | Yunkai Liu |https://www.ratemyprofessors.com/professor/2459997
| 10 | Rate My Professors|Reviews for CS Professor  |Hector Gonzalez |https://www.ratemyprofessors.com/professor/2991157
---

## Chunking Strategy


**Chunk size:** 300 characters

**Overlap:** 50 characters 

**Reasoning:** Reviews are already short students reviews, so i they are alreay self contained and short, i think 300 is enough to include couple reviews and also it without being splited up.

---

## Retrieval Approach


**Embedding model:** all-MiniLM-L6-v2 via sentence-transformers

**Top-k:** 5

**Production tradeoff reflection:** For this  project, all-MiniLM-L6-v2 is ideal. It is free and runs locally, but if i were to run this on real production i would use more powerful models that can take up to 1000 students reviews.

---

## Evaluation Plan


| # | Question | Expected answer |
|---|----------|-----------------|
| 1 |which professor is the easiest to pass | David Marino| 
| 2 | which professor isnt clear about grades and lectures|  Tajmilur Rahman| 
| 3 | which professor is student favorite and everyone likes him? | Mark Blair|
| 4 | |which professor is most disliked by students for being rude? |Tajmilur Rahman|
| 5 | which professor is very disorganized? | Jeremy Cannell 
|

---

## Anticipated Challenges


1.Students rarely mentioned professors name when leaving reviews, so i think it is something that could confuse the model

2. Short reviews with little context and with very little specifics.

---

## Architecture

┌─────────────────────────────────────────────────────────────┐
│                      RAG PIPELINE                           │
└─────────────────────────────────────────────────────────────┘

  [.txt files per professor]
           │
           ▼
  ┌─────────────────┐
  │   INGESTION     │  Tool: Python (open / read files)
  │  Load raw text  │  One .txt file per professor
  └────────┬────────┘
           │
           ▼
  ┌─────────────────┐
  │    CHUNKING     │  Tool: Python string slicing
  │  300 char size  │  50 char overlap
  │  50 char overlap│
  └────────┬────────┘
           │
           ▼
  ┌─────────────────┐
  │   EMBEDDING     │  Tool: sentence-transformers
  │ all-MiniLM-L6   │  Converts each chunk → vector
  │    -v2          │
  └────────┬────────┘
           │
           ▼
  ┌─────────────────┐
  │  VECTOR STORE   │  Tool: ChromaDB (local)
  │  Store vectors  │  + metadata: source filename
  │  + metadata     │
  └────────┬────────┘
           │
      user query
           │
           ▼
  ┌─────────────────┐
  │   RETRIEVAL     │  ChromaDB similarity search
  │   top-k = 5     │  Returns 5 closest chunks
  └────────┬────────┘
           │
           ▼
  ┌─────────────────┐
  │   GENERATION    │  Tool: Groq API
  │ llama-3.3-70b   │  Answer from chunks only
  │  + citations    │  Source attribution required
  └─────────────────┘
---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**

I will give Claude my Documents section (file format: .txt, one per professor) and my Chunking Strategy section (300 char chunks, 50 char overlap). I will ask Claude to implement two functions: load_documents(folder_path) that reads all .txt files and returns a list of {text, source} dicts, and chunk_text(text, chunk_size=300, overlap=50) that splits text into overlapping chunks. I will verify the output by printing 5 sample chunks and checking they are readable, self-contained, and correctly labeled with their source filename.
**Milestone 4 — Embedding and retrieval:**
I will give Claude my Retrieval Approach section (model: all-MiniLM-L6-v2, top-k: 5) and my Architecture diagram. I will ask Claude to implement embed_and_store(chunks) that embeds all chunks using sentence-transformers and stores them in ChromaDB with source metadata, and retrieve(query, k=5) that embeds the query and returns the top-5 most similar chunks with their source filenames. I will verify by running 3 of my evaluation questions and checking that returned chunks visibly relate to each question.

**Milestone 5 — Generation and interface:**
i gave Claude my grounding requirement (answers only 
from retrieved chunks) and my source attribution 
requirement (every response must show which txt file 
it came from) and the Gradio skeleton from the project 
instructions. i asked it to write app.py with the full 
pipeline and a Gradio interface. i verified it worked 
by asking an out of scope question about restaurants 
in Erie and it correctly said it didnt have enough 
information.
