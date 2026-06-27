import os

from dotenv import load_dotenv

from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

from config import *

load_dotenv()

os.environ["HF_TOKEN"] = os.getenv("HF_TOKEN")

loader = PyMuPDFLoader(DATA_PATH)
documents = loader.load()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
)

chunks = splitter.split_documents(documents)

embedding = HuggingFaceEmbeddings(
    model_name=EMBEDDING_MODEL
)

Chroma.from_documents(
    documents=chunks,
    embedding=embedding,
    collection_name=COLLECTION_NAME,
    persist_directory=CHROMA_PATH,
)

print("Database created successfully.")