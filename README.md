rag/
├── 📄 app.py
├── 📦 requirements.txt
├── 🔐 .env.example
├── 🧠 final_legal_embeddings.npy
├── 📋 final_legal_laws_metadata.json
├── 📖 README.md
│
├── 📁 scripts/
│   ├── pdf_extraction.py
│   ├── add_chunk_ids.py
│   └── generate_embeddings.py
│
├── 📁 data/
│   ├── penal_code.pdf
│   ├── structured_laws.json
│   └── chunked_laws.json
│
├── 📁 tests/
│   ├── test_retrieval.py
│   └── test_embeddings.py
│
└── 📁 archive/
    ├── pdf→text_nochunk/
    ├── embedding/
    └── chunk_id-add/
