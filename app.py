from langchain_community.document_loaders import PyMuPDFLoader
data = PyMuPDFLoader("data/Attached.pdf")
data_content=data.load()
print(data)