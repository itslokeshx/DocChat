from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
data = PyMuPDFLoader("data/Attached.pdf")
data_content=data.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=100,)
chunks=text_splitter.split_documents(data_content)
