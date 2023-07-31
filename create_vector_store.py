from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import UnstructuredPDFLoader
import os
import openai
from my_embs import myEmbs

openai.api_key = os.getenv("OPENAI_API_KEY")

# Load source PDFs: 'pdfs/Manual.pdf', 
paths = ["pdfs/Orwe1984-text20.pdf"]
store_path = "faiss_store"

print("Loading documents")
pages = []
for path in paths:
    loader = UnstructuredPDFLoader(path) # Quite good, but slow
    #loader = PyPDFium2Loader(path)
    #loader = PDFMinerLoader(path)
    #loader = PyMuPDFLoader(path) # Fast
    #loader = PDFPlumberLoader(path)

    local_pages = loader.load_and_split()
    pages.extend(local_pages)

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(pages)

# Create vector database
print("Generating database")
# embeddings = OpenAIEmbeddings()
embeddings = myEmbs()
db = FAISS.from_documents(texts, embeddings)
db.save_local(store_path)

print(f"Database stored in {store_path} folder")