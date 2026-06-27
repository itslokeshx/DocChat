import os

from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq

from config import *
from prompts import build_prompt

load_dotenv()

# ✅ FIX #3: Validate HF_TOKEN
hf_token = os.getenv("HF_TOKEN")
if not hf_token:
    raise ValueError(
        "❌ HF_TOKEN environment variable not set.\n"
        "Add it to your .env file for HuggingFace model access."
    )
os.environ["HF_TOKEN"] = hf_token

# ✅ FIX #1: Check if vector DB exists
if not os.path.exists(CHROMA_PATH):
    raise FileNotFoundError(
        f"❌ Vector DB not found at '{CHROMA_PATH}'.\n"
        f"Please run 'python ingest.py' first to create the database."
    )

embedding = HuggingFaceEmbeddings(
    model_name=EMBEDDING_MODEL
)

db = Chroma(
    collection_name=COLLECTION_NAME,
    persist_directory=CHROMA_PATH,
    embedding_function=embedding
)

# ✅ FIX #2: Validate GROQ_API
groq_api = os.getenv("GROQ_API")
if not groq_api:
    raise ValueError(
        "❌ GROQ_API environment variable not set.\n"
        "Add it to your .env file."
    )

llm = ChatGroq(
    model=GROQ_MODEL,
    temperature=0.1,
    max_tokens=1024,
    api_key=groq_api
)


def ask(question: str):

    results = db.similarity_search(
        query=question,
        k=4
    )

    # ✅ FIX #5: Handle empty search results
    if not results:
        return "❌ No relevant information found in the document to answer your question."

    context = ""
    for doc in results:
        context += doc.page_content + "\n\n"

    prompt = build_prompt(context, question)

    response = llm.invoke(prompt)

    return response.content