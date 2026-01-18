import streamlit as st
import numpy as np
import json
import faiss
from sentence_transformers import SentenceTransformer
from groq import Groq
import os


@st.cache_resource
def load_embeddings():
    emb = np.load("final_legal_embeddings.npy")
    with open("final_legal_laws_metadata.json", "r") as f:
        meta = json.load(f)

    dim = emb.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(emb)

    return emb, meta, index


@st.cache_resource
def load_sbert():
    return SentenceTransformer("all-mpnet-base-v2")


@st.cache_resource
def load_llm():
    return Groq(api_key=os.environ["GROQ_API_KEY"])


def search_law(query, sbert, index, metadata, k=3):
    q_emb = sbert.encode([query], convert_to_numpy=True)
    distances, indices = index.search(q_emb, k)

    chunks = []
    for i in indices[0]:
        item = metadata[i]
        chunks.append(f"[{item.get('chunk_id')}] {item['text']}")

    return "\n\n".join(chunks)


def ask_llm(client, context, question):
    prompt = f"""
You are an AI LEGAL ASSISTANT whose sole authority is the
National Penal Code of Nepal, 2017.

This system operates under a Retrieval-Augmented Generation (RAG) framework.
The provided Law Text is the ONLY source of truth.

======================
ABSOLUTE LEGAL RULES
======================

1. You MUST answer strictly and exclusively from the provided Law Text.
2. You MUST NOT rely on prior knowledge, general law principles, or assumptions.
3. You MUST NOT add, infer, simplify, reinterpret, or generalize the law.
4. If the Law Text does NOT explicitly contain the answer, you MUST respond with a refusal.
5. Partial answers are NOT allowed.
6. Every legal statement MUST be directly supported by the Law Text.
7. You MUST preserve all legal conditions, exceptions, and provisos.
8. You MUST maintain a formal, neutral, legal tone.
9. You MUST cite the exact Chapter, Section, and Subsection if available.
10. Hallucination of law is STRICTLY PROHIBITED.

======================
REFUSAL POLICY (MANDATORY)
======================

You MUST refuse to answer if:
- The relevant legal provision is absent
- The Law Text is incomplete
- The question exceeds the scope of the provided sections
- The question asks for punishment, procedure, or interpretation not stated

Refusal MUST use EXACT wording:

"The provided sections of the National Penal Code, 2017 do not mention this."

No alternative phrasing is permitted.

======================
AUTHORITATIVE LAW TEXT
======================

{context}

======================
USER QUESTION
======================

{question}

======================
RESPONSE FORMAT (STRICT)
======================

Answer:
<Precise, faithful legal explanation strictly grounded in the Law Text>

Source:
<Exact Chapter / Section / Subsection OR "Not specified in provided text">
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,
        max_tokens=350,
    )
    return response.choices[0].message.content



# =========================
# STREAMLIT UI
# =========================
st.title("🇳🇵 Nepal Criminal Code — RAG Legal Assistant")

q = st.text_input("Ask a legal question:")

if st.button("Search"):
    if not q.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Loading models..."):
            emb, metadata, index = load_embeddings()
            sbert = load_sbert()
            client = load_llm()

        with st.spinner("Retrieving law sections..."):
            context = search_law(q, sbert, index, metadata)

        with st.expander("Retrieved Law Context"):
            st.write(context)

        with st.spinner("Generating answer..."):
            answer = ask_llm(client, context, q)

        st.subheader("Answer")
        st.write(answer)
