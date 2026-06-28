import os

from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq

from config import *
from prompts import build_prompt


load_dotenv()

hf_token = os.getenv("HF_TOKEN")
if not hf_token:
    raise ValueError(
        "The HF_TOKEN is not present in the environment variables"
    )

if not os.path.exists(CHROMA_PATH):
    raise FileNotFoundError(
        f" Vector DB not found at '{CHROMA_PATH}'.\n"
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
        "The GROQ_API is not present in the environment variables"
    )

llm = ChatGroq(
    model=GROQ_MODEL,
    temperature=0.1,
    max_tokens=1024,
    api_key=groq_api
)


def ask(question: str):
    results_with_scores = db.similarity_search_with_score(
        query=question,
        k=6
    )
    
    DISTANCE_THRESHOLD = 1.2

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