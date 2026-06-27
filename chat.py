import os

from dotenv import load_dotenv

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq

from config import *
from prompts import build_prompt

load_dotenv()

os.environ["HF_TOKEN"] = os.getenv("HF_TOKEN")

embedding = HuggingFaceEmbeddings(
    model_name=EMBEDDING_MODEL
)

db = Chroma(
    persist_directory=CHROMA_PATH,
    embedding_function=embedding,
    collection_name=COLLECTION_NAME,
)

llm = ChatGroq(
    model=GROQ_MODEL,
    api_key=os.getenv("GROQ_API"),
    temperature=0.1,
)
def ask(question):

    results = db.similarity_search(
        question,
        k=4
    )

    context = ""

    for doc in results:
        context += doc.page_content + "\n\n"

    prompt = build_prompt(context, question)

    response = llm.invoke(prompt)

    return response.content