import os

from dotenv import load_dotenv
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

from config import *

load_dotenv()

os.environ["HF_TOKEN"] = os.getenv("HF_TOKEN")


def ingest():

    print("Loading PDF...")

    loader = PyMuPDFLoader(DATA_PATH)
    documents = loader.load()

    print(f"Loaded {len(documents)} pages.")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )

    chunks = splitter.split_documents(documents)

    print(f"Created {len(chunks)} chunks.")

    embedding = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
    )

    print("Creating Vector Database...")

    Chroma.from_documents(
        documents=chunks,
        embedding=embedding,
        collection_name=COLLECTION_NAME,
        persist_directory=CHROMA_PATH
    )

    print("✅ Vector Database Created Successfully!")


if __name__ == "__main__":
    ingest()