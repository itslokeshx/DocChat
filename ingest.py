import os
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
data = PyMuPDFLoader("data/Attached.pdf")
data_content=data.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=100,)
chunks=text_splitter.split_documents(data_content)
load_dotenv()
os.environ['HF_TOKEN']=os.getenv("HF_TOKEN")
GROQ_API =os.environ['GROQ_API']=os.getenv("GROQ_API")
hg_embedding=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
Vector_DB= Chroma.from_documents(
    documents=chunks,
    embedding=hg_embedding,
    collection_name="pdf_embedding_vectorDB",
    persist_directory="Chrome_DB")