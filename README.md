# The Unofficial Guide — Project 1


---

## Domain

I chose student reviews of CS professors at Gannon University from Rate My Professors. this is valuable because it gives students real insights about what professors are actually like, stuff like how hard the exams are, how fair the grading is, and whether they actually help you. the university doesnt publish any of this officially so if you want to know who to take or avoid you have to manually read through dozens of reviews yourself. this system makes that way easier by just letting you ask a question. it could also help new students deciding whether to even attend Gannon based on how the CS department is doing.

---

## Document Sources


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

**Chunk size**:300 characters

**Overlap:**  50 characters

**Why these choices fit your documents**:the reviews are already pretty short, most of them are like 1 to 4 sentences. so 300 characters fits about 1 or 2 reviews in one chunk which i thought was good because each chunk stays focused on one opinion and doesnt mix a bunch of unrelated stuff together. i used 50 character overlap so that if a review gets cut at the end of a chunk the next chunk still has a little bit of it so nothing important gets completely lost. before chunking i manually cleaned each file by removing all the RMP boilerplate like dates, grades, attendance info, thumbs up counts, and tag labels. i only kept the actual review text plus the professor name and course number at the top.

**Final chunk count**: 63 chunks across 10 documents

---

## Embedding Model


**Model used:**all-MiniLM-L6-v2 via sentence-transformers
i used this because its free and runs on my laptop with no api key needed. worked fine for this since the reviews are short and in english.

**Production tradeoff reflection:** if this was a real product i would probably switch to a better model. like if i wanted more accurate results on opinion text i would pay for OpenAIs embedding model. if reviews were in other languages id need a multilingual model. also MiniLM only handles 256 tokens at a time which was fine here but wouldnt work for longer documents. and local models are faster than api ones which matters if real students are using it and dont want to wait.

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:** in app.py i told the LLM it can only use what i give it. the rules i put in the prompt are:
IMPORTANT RULES:
- Answer using ONLY the information provided in the sources below
- Do NOT use any outside knowledge or make assumptions
- If the sources do not contain enough information to answer, say
  "I don't have enough information on that based on the available reviews."
- Always mention which professor(s) your answer is about
basically the chunks get pasted into the prompt before the question so the LLM only sees those and nothing else. it cant just make stuff up from what it already knows.

**How source attribution is surfaced in the response:**each chunk in ChromaDB has the filename saved with it. when chunks get retrieved the filenames go into the prompt too so the LLM knows which file each thing came from. the app also has a Sources Used box on the right side that shows the user exactly which professor files were used to answer their question.

---

## Evaluation Report



| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | which professor is the easiest to pass? | David Marino | said Marino, Blair, and Cannell are all easy to pass | Relevant | Accurate |

| 2 | which professor isnt clear about grades and lectures? | Tajmilur Rahman | said Rahman, doesnt follow syllabus and grades randomly | Relevant | Accurate |

| 3 | which professor is student favorite that everyone likes? | Mark Blair | said David Marino instead of Blair | Partially relevant | Partially accurate |

| 4 | which professor is most disliked by students for being rude? | Tajmilur Rahman | said Rahman, yells at students and humiliates them publicly | Relevant | Accurate |

| 5 | which professor is very disorganized? | Jeremy Cannell | said Mark Blair instead of Cannell | Off-target | Inaccurate |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

**Question that failed:**which professor is very disorganized?

**What the system returned:**Mark Blair instead of Jeremy Cannell

**Root cause (tied to a specific pipeline stage):**the chunking split Cannells reviews by character count so the review that said he was disorganized got cut in half. one chunk ended up starting with "es not know the subject well" which makes no sense on its own. so when ChromaDB searched for disorganized it couldnt find that chunk because the meaning was broken. its a chunking problem basically.

**What you would change to fix it:**instead of splitting by fixed character count i would split by review boundaries. since every review in my files starts with "Review N:" i could use that as a natural split point so every chunk contains one complete review. that way the embeddings would carry the full meaning of what the student wrote and wouldnt get cut off mid thought.

---

## Spec Reflection


**One way the spec helped you during implementation:** writing the chunking strategy in planning.md before i wrote any code made me actually think about my documents first. because i read through the reviews and noticed they were short i decided on 300 characters upfront and that decision carried straight into the chunk_text() function. i didnt have to guess at numbers mid implementation, the spec basically made the decision for me ahead of time.

**One way your implementation diverged from the spec, and why:** my spec assumed i could load documents from URLs but Rate My Professors blocks automated scraping. when i tried fetching a URL in python it just returned an error. so i had to manually copy paste every single review from 10 professor pages into individual txt files which took way longer than expected and wasnt in my original plan at all. if i did this project again i would put that in the spec from the start and budget extra time for it.

---

## AI Usage


**Instance 1**

- *What I gave the AI:*my Documents section (10 txt files, one per professor) and my Chunking Strategy section (300 char chunks, 50 char overlap) from planning.md
- *What it produced:* a working ingest.py script with load_documents() and chunk_text() functions that read all the txt files and split them into overlapping chunks with source metadata attached
- *What I changed or overrode:*i ran python ingest.py and looked at the 5 sample chunks it printed. i noticed some chunks started mid word because of the fixed character split. i kept the chunk size the same but documented this as a known limitation in the failure case section

**Instance 2**

- *What I gave the AI:*my Retrieval Approach section (model: all-MiniLM-L6-v2, top-k: 5) and my architecture diagram from planning.md
- *What it produced:* retriever.py with embed_and_store() that loads chunks and stores them in ChromaDB with source metadata, and retrieve() that embeds a query and returns the top 5 closest chunks with their source filenames and distance scores
- *What I changed or overrode:* i tested it with 3 evaluation queries and saw that distance scores were high around 0.9 to 1.1 meaning weak matches. i didnt change the code but traced the problem back to the chunking stage and used it as my failure case
