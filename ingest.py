import os

from dotenv import load_dotenv
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

from config import *

load_dotenv()

hf_token = os.getenv("HF_TOKEN")
if not hf_token:
    raise ValueError(
        " The HF_TOKEN is not present in the environment variables"
    )

def ingest():

    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(
            f"PDF file not found at '{DATA_PATH}'.\n"
            f"Please ensure the file exists before running ingest."
        )

    print("📥 Loading PDF...")

    loader = PyMuPDFLoader(DATA_PATH)
    documents = loader.load()

    print(f"✅ Loaded {len(documents)} pages.")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )

    chunks = splitter.split_documents(documents)

    print(f"✂️ Created {len(chunks)} chunks.")

    embedding = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
    )

    print("🔄 Creating Vector Database...")

    Chroma.from_documents(
        documents=chunks,
        embedding=embedding,
        collection_name=COLLECTION_NAME,
        persist_directory=CHROMA_PATH
    )

    print(f"✅ Vector Database Created Successfully at '{CHROMA_PATH}'!")


if __name__ == "__main__":
    ingest()