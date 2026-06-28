# 📄 DocChat — Chat with Any PDF

<div align="center">

**A lightweight RAG pipeline that turns any PDF into an intelligent conversational assistant.**  
Ask questions in plain English. Get grounded, context-accurate answers

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-Framework-1C3C3C?style=flat-square&logo=chainlink&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-LLM-F55036?style=flat-square)
![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector%20Store-orange?style=flat-square)
![HuggingFace](https://img.shields.io/badge/HuggingFace-Embeddings-FFD21E?style=flat-square&logo=huggingface&logoColor=black)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

</div>

---

## What is DocChat?

DocChat is a **Retrieval-Augmented Generation (RAG)** app that lets you have a natural conversation with any PDF. It embeds your document into a local vector database, retrieves only the most relevant passages per question, and passes them to a Groq-hosted LLM for a precise, context-grounded answer.

No full document is ever sent to the LLM — only the relevant chunks. This keeps latency low, cost minimal, and answers accurate.

---

## ✨ Features

| Feature | Details |
|---|---|
| 📥 **PDF Ingestion** | Parses and chunks any PDF using PyMuPDF |
| 🔍 **Semantic Search** | Embeds chunks via `all-MiniLM-L6-v2` and stores them in ChromaDB |
| 🤖 **LLM Answering** | Routes only relevant context to Groq's LLM for grounded answers |
| 🛡️ **Smart Filtering** | Distance-threshold filtering discards low-quality context before it reaches the LLM |
| 👋 **Greeting Detection** | Recognises chitchat and responds naturally, skipping the retrieval step |
| ⚠️ **Fail-fast Validation** | Clear errors on startup if API keys, the PDF, or the vector DB are missing |

---

## 🏗️ Architecture

```
╔══════════════════════════════════════════════════════╗
║                     INGESTION                        ║
║                                                      ║
║  PDF  ──► PyMuPDFLoader ──► RecursiveTextSplitter    ║
║                                    │                 ║
║                         HuggingFace Embeddings       ║
║                                    │                 ║
║                               ChromaDB  (on disk)    ║
╚══════════════════════════════════════════════════════╝

╔══════════════════════════════════════════════════════╗
║                   QUERY  (RAG)                       ║
║                                                      ║
║  User question                                       ║
║       │                                              ║
║       ├─► Greeting? ──────────► Direct reply         ║
║       │                                              ║
║       └─► HuggingFace Embeddings                     ║
║                   │                                  ║
║          ChromaDB similarity_search (k=6)            ║
║                   │                                  ║
║          Distance filter  (score ≤ 1.2)              ║
║                   │                                  ║
║          No match? ──────────► "Not found" reply     ║
║                   │                                  ║
║          Build prompt (context + question)           ║
║                   │                                  ║
║          Groq LLM  (llama-3.1-8b-instant)            ║
║                   │                                  ║
║               Answer ──► User                        ║
╚══════════════════════════════════════════════════════╝
```

---

## 📁 Project Structure

```
DocChat/
├── app.py          # CLI entry point — chat loop & I/O handling
├── chat.py         # Core RAG logic: embedding, retrieval, LLM call
├── ingest.py       # One-time ingestion script → populates ChromaDB
├── prompts.py      # System prompt template for the LLM
├── config.py       # Central config (paths, model names, chunk settings)
├── data/
│   └── <your-file>.pdf     # Drop your PDF here
├── chroma_db/              # Auto-generated vector store (git-ignored)
└── .env                    # API keys (git-ignored)
```

---

## ⚙️ Configuration (`config.py`)

All tuneable knobs live in one place — no need to touch any other file.

| Variable | Default | Description |
|---|---|---|
| `DATA_PATH` | `data/<your-file>.pdf` | Path to the PDF to ingest |
| `CHROMA_PATH` | `chroma_db` | Directory where ChromaDB persists vectors |
| `COLLECTION_NAME` | `pdf_embedding_vectorDB` | ChromaDB collection name |
| `EMBEDDING_MODEL` | `sentence-transformers/all-MiniLM-L6-v2` | HuggingFace embedding model |
| `GROQ_MODEL` | `llama-3.1-8b-instant` | Groq LLM model identifier |
| `CHUNK_SIZE` | `500` | Characters per text chunk |
| `CHUNK_OVERLAP` | `100` | Character overlap between adjacent chunks |

---

## 🚀 Quickstart

### 1. Clone the repo

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

### 4. Add your API keys

Create a `.env` file in the project root:

```env
GROQ_API=your_groq_api_key_here
HF_TOKEN=your_huggingface_token_here
```

> - **GROQ_API** — Free key at [console.groq.com](https://console.groq.com)  
> - **HF_TOKEN** — Free token at [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)

### 5. Add your PDF

Drop your PDF into the `data/` folder, then update `DATA_PATH` in `config.py` to match the filename.

### 6. Ingest the PDF *(once per document)*

```bash
python ingest.py
```

```
📥 Loading PDF...
✅ Loaded 268 pages.
✂️ Created 991 chunks.
🔄 Creating Vector Database...
✅ Vector Database Created Successfully at 'chroma_db'!
```

> Re-run `ingest.py` whenever you switch to a different PDF.

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

👤 You: what is the main argument of the book?

🤖 DocChat: The central argument is that being "nice" — constantly
seeking approval and avoiding conflict — keeps people from living
authentically and getting what they truly want from life.

👤 You: exit

👋 Goodbye!
```

**Exit:** type `exit`, `quit`, `bye`, or press `Ctrl+C`.

---

## 🔬 How RAG Works — Step by Step

1. **Ingest** — The PDF is parsed page-by-page and split into overlapping 500-character chunks. Each chunk is encoded into a 384-dimensional vector by `all-MiniLM-L6-v2` and stored in ChromaDB on disk.

2. **Embed the question** — At query time, the user's question is encoded by the same model, producing a comparable 384-d vector.

3. **Retrieve** — ChromaDB returns the 6 nearest chunks ranked by L2 distance.

4. **Filter** — Chunks with a distance score > 1.2 are dropped. This prevents semantically unrelated context from reaching the LLM.

5. **Generate** — The surviving chunks are concatenated into a context block and injected into a structured prompt. The Groq LLM synthesises an answer using *only* that context.

6. **Guard** — If no chunks pass the threshold, the app returns a "not found" message without ever calling the LLM, saving tokens and latency.

---

## 🛠️ Troubleshooting

| Error / Symptom | Fix |
|---|---|
| `❌ HF_TOKEN environment variable not set` | Add `HF_TOKEN=...` to `.env` |
| `❌ GROQ_API environment variable not set` | Add `GROQ_API=...` to `.env` |
| `❌ Vector DB not found at 'chroma_db'` | Run `python ingest.py` first |
| `❌ PDF file not found` | Verify `DATA_PATH` in `config.py` and that the file exists |
| Vague or off-topic answers | Switch to a larger model: `GROQ_MODEL = "llama-3.3-70b-versatile"` |
| Too many "not found" responses | Raise the threshold in `chat.py`: `DISTANCE_THRESHOLD = 1.4` |

---

## 📦 Tech Stack

| Package | Role |
|---|---|
| `langchain-community` | PDF loader (`PyMuPDFLoader`) |
| `langchain-text-splitters` | `RecursiveCharacterTextSplitter` |
| `langchain-huggingface` | HuggingFace embeddings wrapper |
| `langchain-chroma` | ChromaDB vector store integration |
| `langchain-groq` | Groq LLM integration |
| `chromadb` | Local vector database |
| `python-dotenv` | `.env` file loading |
| `pymupdf` | PDF parsing engine |

---

## 📝 License

MIT — free to use, modify, and distribute.