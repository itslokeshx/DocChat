# 📄 DocChat — PDF Question-Answering with RAG

DocChat is a **Retrieval-Augmented Generation (RAG)** application that lets you have a natural conversation with any PDF document. Ask questions in plain English and get accurate, context-grounded answers powered by a local vector database and a Groq-hosted LLM.

---

## ✨ Features

- 📥 **PDF Ingestion** — Loads and chunks any PDF using PyMuPDF
- 🔍 **Semantic Search** — Embeds chunks with a HuggingFace sentence-transformer and stores them in ChromaDB
- 🤖 **LLM Answering** — Sends only the most relevant context to Groq's LLM for a grounded answer
- 🛡️ **Smart Filtering** — Distance-threshold filtering prevents garbage context from reaching the LLM
- 👋 **Greeting Detection** — Recognises chitchat and responds naturally without hitting the database
- ⚠️ **Fail-fast Validation** — Clear error messages if API keys, the PDF, or the vector DB are missing

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        INGESTION                            │
│                                                             │
│  PDF file  ──► PyMuPDFLoader ──► RecursiveTextSplitter      │
│                                        │                    │
│                             HuggingFace Embeddings           │
│                                        │                    │
│                                   ChromaDB ◄── persisted    │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                       QUERY (RAG)                           │
│                                                             │
│  User question                                              │
│       │                                                     │
│       ├─► Greeting? ──► Direct friendly reply               │
│       │                                                     │
│       └─► HuggingFace Embeddings                            │
│                   │                                         │
│            ChromaDB similarity_search_with_score (k=6)      │
│                   │                                         │
│            Distance filter (≤ 1.2)                          │
│                   │                                         │
│            No results? ──► "Not found" reply                │
│                   │                                         │
│            Build prompt (context + question)                │
│                   │                                         │
│            Groq LLM (llama-3.1-8b-instant)                  │
│                   │                                         │
│            Answer ──► User                                  │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
DocChat/
├── app.py          # CLI entry point — chat loop with I/O handling
├── chat.py         # Core RAG logic: embedding, retrieval, LLM call
├── ingest.py       # One-time PDF ingestion script → populates ChromaDB
├── prompts.py      # System prompt template for the LLM
├── config.py       # Central configuration (paths, model names, chunk settings)
├── data/
│   └── Attached.pdf    # The PDF document to chat with
├── chroma_db/          # Auto-generated vector database (git-ignored)
├── .env                # API keys (git-ignored)
└── requirements.txt    # Python dependencies
```

---

## ⚙️ Configuration (`config.py`)

| Variable | Default | Description |
|---|---|---|
| `DATA_PATH` | `data/Attached.pdf` | Path to the PDF to ingest |
| `CHROMA_PATH` | `chroma_db` | Directory where ChromaDB persists |
| `COLLECTION_NAME` | `pdf_embedding_vectorDB` | ChromaDB collection name |
| `EMBEDDING_MODEL` | `sentence-transformers/all-MiniLM-L6-v2` | HuggingFace embedding model |
| `GROQ_MODEL` | `llama-3.1-8b-instant` | Groq LLM model |
| `CHUNK_SIZE` | `500` | Characters per text chunk |
| `CHUNK_OVERLAP` | `100` | Overlap between adjacent chunks |

To use a different PDF or a more powerful model, edit `config.py` — no code changes required.

---

## 🚀 Setup & Usage

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd DocChat
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # Linux / macOS
# venv\Scripts\activate         # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the project root:

```env
GROQ_API=your_groq_api_key_here
HF_TOKEN=your_huggingface_token_here
```

- **GROQ_API** — Get a free key at [console.groq.com](https://console.groq.com)
- **HF_TOKEN** — Get a free token at [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)

### 5. Add your PDF

Place your PDF inside the `data/` folder and update `DATA_PATH` in `config.py` if the filename differs.

### 6. Ingest the PDF *(run once)*

```bash
python ingest.py
```

Expected output:
```
📥 Loading PDF...
✅ Loaded 268 pages.
✂️ Created 991 chunks.
🔄 Creating Vector Database...
✅ Vector Database Created Successfully at 'chroma_db'!
```

> **Note:** Re-run `ingest.py` any time you replace the PDF.

### 7. Start chatting

```bash
python app.py
```

```
==================================================
📄 DocChat - RAG Application
==================================================

✅ System initialized successfully!
Type your questions about the document (or 'exit' to quit)

👤 You: what is anxious attachment?

🤖 DocChat: Anxious attachment is a style characterised by a chronically activated
attachment system. People with this style are highly sensitive to changes in
others' emotional expression and have an intense need for reassurance...

👤 You: exit

👋 Goodbye!
```

**Exit commands:** `exit`, `quit`, or `bye` — or press `Ctrl+C`.

---

## 🔧 How RAG Works (step by step)

1. **Ingestion** — The PDF is parsed page by page and split into overlapping 500-character chunks. Each chunk is embedded into a 384-dimensional vector using `all-MiniLM-L6-v2` and stored in ChromaDB on disk.

2. **Retrieval** — When you ask a question, the question itself is embedded using the same model. ChromaDB returns the 6 most similar chunks ranked by L2 distance.

3. **Filtering** — Chunks with a distance score > 1.2 are discarded. This prevents low-quality, semantically unrelated context from confusing the LLM.

4. **Generation** — The filtered chunks are concatenated into a context block and injected into a structured prompt alongside the question. The Groq LLM synthesises a grounded answer.

5. **Grounding** — The LLM is instructed to answer *only* from the context. If no relevant chunks pass the threshold, it replies with a "not found" message without ever calling the LLM.

---

## 🛠️ Troubleshooting

| Error | Fix |
|---|---|
| `❌ HF_TOKEN environment variable not set` | Add `HF_TOKEN=...` to your `.env` file |
| `❌ GROQ_API environment variable not set` | Add `GROQ_API=...` to your `.env` file |
| `❌ Vector DB not found at 'chroma_db'` | Run `python ingest.py` first |
| `❌ PDF file not found at 'data/...'` | Check `DATA_PATH` in `config.py` and ensure the file exists |
| LLM gives vague answers | Try a larger model: set `GROQ_MODEL = "llama-3.3-70b-versatile"` in `config.py` |
| Too many "not found" responses | Lower `DISTANCE_THRESHOLD` in `chat.py` (try `1.4`) |

---

## 📦 Dependencies

| Package | Purpose |
|---|---|
| `langchain-community` | PDF loader (`PyMuPDFLoader`) |
| `langchain-text-splitters` | `RecursiveCharacterTextSplitter` |
| `langchain-huggingface` | HuggingFace embeddings integration |
| `langchain-chroma` | ChromaDB vector store integration |
| `langchain-groq` | Groq LLM integration |
| `chromadb` | Local vector database |
| `python-dotenv` | `.env` file loading |
| `pymupdf` | PDF parsing engine |

---

## 📝 License

MIT License — free to use and modify.