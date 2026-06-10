from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DOC_PATH = os.path.join(BASE_DIR, "compliance_docs", "investment_guidelines.txt")

def build_compliance_rag():

    loader = TextLoader(DOC_PATH)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    docs = splitter.split_documents(documents)

    # ✅ Correct embedding model
    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    vectordb = Chroma.from_documents(
        docs,
        embeddings,
        persist_directory="./chroma_compliance_db"
    )

    return vectordb