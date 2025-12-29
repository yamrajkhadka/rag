rag/
├── 🚀 ACTIVE APPLICATION FILES
│   ├── app.py                              # Main Streamlit RAG interface
│   ├── final_legal_embeddings.npy          # Vector database (768D embeddings)
│   ├── final_legal_laws_metadata.json      # Legal text with metadata & chunk IDs
│   ├── requirements.txt                     # Python package dependencies
│   ├── .env.example                         # Environment configuration template
│   └── README.md                           # Project documentation
│
├── 🔧 PROCESSING SCRIPTS
│   ├── pdf_extraction.py                   # Step 1: PDF → Structured JSON
│   ├── add_chunk_ids.py                    # Step 2: Add npc2017_* identifiers
│   └── generate_embeddings.py              # Step 3: Create embeddings & FAISS index
│
├── 📊 DATA FILES
│   ├── penal_code.pdf                      # Source: National Penal Code Act, 2017
│   ├── structured_laws.json                # Parsed JSON with legal hierarchy
│   └── chunked_laws.json                   # Enhanced JSON with chunk IDs
│
└── 📦 ARCHIVE (PREVIOUS VERSIONS)
    ├── pdf→text_nochunk/                   # Initial text extraction outputs
    ├── embedding/                          # Embedding generation outputs
    └── chunk_id-add/                       # Chunk ID processing outputs
