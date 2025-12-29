import json
import numpy as np
from sentence_transformers import SentenceTransformer

# Load your JSON with chunk_ids
with open("/Users/yamrajkhadka/nepal-legal-rag/source-change/naya_chunk.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Load embedding model
embed_model = SentenceTransformer("all-mpnet-base-v2")


# Generate embeddings for each chunk
texts = [item["text"] for item in data]
embeddings = embed_model.encode(texts, convert_to_numpy=True, show_progress_bar=True)

# Save embeddings for later use
np.save("final_legal_embeddings.npy", embeddings)

# Save metadata mapping (for retrieval)
with open("final_legal_laws_metadata.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Embeddings generated and saved successfully!")
