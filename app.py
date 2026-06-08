"""
app.py
Milestone 5: Grounded Generation + Gradio Interface

Takes a user question, retrieves the top 5 relevant chunks
from ChromaDB, then uses Groq's LLM to generate an answer
based ONLY on those chunks. Includes source attribution.

Run with: python app.py
Then open: http://localhost:7860
"""

import os
from groq import Groq
from dotenv import load_dotenv
from retriever import retrieve
import gradio as gr

# Load API key from .env file
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# ── 1. GROUNDED GENERATION ────────────────────────────────────────────────────

def ask(question):
    """
    Full RAG pipeline:
    1. Retrieve top 5 relevant chunks from ChromaDB
    2. Build a prompt with those chunks as context
    3. Ask Groq LLM to answer using ONLY those chunks
    4. Return answer + source attribution
    """

    # Step 1: Retrieve relevant chunks
    chunks = retrieve(question, k=5)

    # Step 2: Build context string from chunks
    context = ""
    for i, chunk in enumerate(chunks):
        context += f"[Source {i+1}: {chunk['source']}]\n{chunk['text']}\n\n"

    # Step 3: Build the prompt
    # CRITICAL: we explicitly tell the LLM to ONLY use the provided context
    prompt = f"""You are a helpful assistant that answers questions about CS professors at Gannon University based on student reviews.

IMPORTANT RULES:
- Answer using ONLY the information provided in the sources below
- Do NOT use any outside knowledge or make assumptions
- If the sources do not contain enough information to answer, say "I don't have enough information on that based on the available reviews."
- Always mention which professor(s) your answer is about
- Keep your answer clear and helpful

SOURCES:
{context}

QUESTION: {question}

ANSWER:"""

    # Step 4: Call Groq API
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000
    )

    answer = response.choices[0].message.content

    # Step 5: Collect unique sources
    sources = list(set(chunk["source"] for chunk in chunks))

    return {
        "answer": answer,
        "sources": sources
    }


# ── 2. GRADIO INTERFACE ───────────────────────────────────────────────────────

def handle_query(question):
    """
    Wrapper for Gradio — calls ask() and formats output
    """
    if not question.strip():
        return "Please enter a question.", ""

    result = ask(question)
    sources_text = "\n".join(f"• {s}" for s in result["sources"])
    return result["answer"], sources_text


# ── 3. TEST WITHOUT UI (optional) ─────────────────────────────────────────────

def test_generation():
    """
    Test grounded generation on your 5 evaluation questions
    Run this before launching the UI to verify everything works
    """
    test_questions = [
        "Which professor curves their exams?",
        "Which professor is best for office hours?",
        "Which professor gives the most homework?",
        "Which professor is easiest to pass?",
        "Which professor explains things most clearly?",
        "What is the best restaurant in Erie Pennsylvania?"  # out of scope test
    ]

    for question in test_questions:
        print(f"\nQuestion: {question}")
        print("─" * 50)
        result = ask(question)
        print(f"Answer: {result['answer']}")
        print(f"Sources: {', '.join(result['sources'])}")
        print()


# ── 4. LAUNCH ─────────────────────────────────────────────────────────────────

with gr.Blocks(title="Gannon CS Professor Guide") as demo:
    gr.Markdown("# 🎓 Gannon CS Professor Unofficial Guide")
    gr.Markdown("Ask questions about CS professors at Gannon University based on real student reviews.")

    with gr.Row():
        inp = gr.Textbox(
            label="Your Question",
            placeholder="e.g. Which professor is easiest to pass?",
            lines=2
        )

    btn = gr.Button("Ask", variant="primary")

    with gr.Row():
        answer = gr.Textbox(label="Answer", lines=8)
        sources = gr.Textbox(label="Sources Used", lines=8)

    # Example questions users can click
    gr.Examples(
        examples=[
            ["Which professor curves their exams?"],
            ["Which professor is best for office hours?"],
            ["Which professor gives the most homework?"],
            ["Which professor is easiest to pass?"],
            ["Which professor explains things most clearly?"],
        ],
        inputs=inp
    )

    btn.click(handle_query, inputs=inp, outputs=[answer, sources])
    inp.submit(handle_query, inputs=inp, outputs=[answer, sources])

if __name__ == "__main__":
    # Uncomment the line below to test without the UI first
    # test_generation()

    print("Launching Gradio interface...")
    print("Open http://localhost:7860 in your browser")
    demo.launch()