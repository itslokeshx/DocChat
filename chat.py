import os
import re

from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq

from config import *
from prompts import build_prompt

_GREETINGS = re.compile(
    r"^(hi+|h[ae]+llo+|hey+|good\s*(morning|afternoon|evening)|howdy|sup|yo+|greetings|what'?s\s*up)[!?.\s]*$",
    re.IGNORECASE
)

load_dotenv()

hf_token = os.getenv("HF_TOKEN")
if not hf_token:
    raise ValueError(
        "❌ HF_TOKEN environment variable not set.\n"
        "Add it to your .env file for HuggingFace model access."
    )
os.environ["HF_TOKEN"] = hf_token

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

    if _GREETINGS.match(question.strip()):
        return "Hello! Ask me anything about the document and I'll do my best to help."

    results_with_scores = db.similarity_search_with_score(
        query=question,
        k=6
    )


   relevant = [
        doc for doc, score in results_with_scores
        if score <= DISTANCE_THRESHOLD
    ]

    if not relevant:
        return "I couldn't find relevant information about that in the document."

    context = "".join(doc.page_content + "\n\n" for doc in relevant)

    prompt = build_prompt(context, question)
    response = llm.invoke(prompt)
    return response.content