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
give correct answer"


Law Text:
{context}

Question:
{question}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
        max_tokens=400,
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
