## 📂 Repository Structure

This project utilizes a **Monorepo** structure:

```text
LegalGPT-Nepal/
├── backend/            # FastAPI Application
│   ├── app/
│   │   ├── api/        # REST & WebSocket Routes
│   │   ├── core/       # Config, Security, DB setup
│   │   ├── services/   # RAG & AI Logic
│   │   └── main.py     # Entry Point
│   ├── alembic/        # DB Migrations
│   └── requirements.txt
├── frontend/           # React User Interface
├── ai_engine/          # Notebooks for Fine-tuning & RAG Pipeline
├── data/               # Raw and Processed Legal Datasets
└── docs/               # Project Documentation & Diagrams
```

---
