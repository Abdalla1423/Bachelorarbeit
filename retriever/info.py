from langchain_core.pydantic_v1 import Field
from langchain_core.vectorstores import VectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter, TextSplitter
from typing import List
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings

# Correct initialization of the vectorstore
embedding = OpenAIEmbeddings()  # or your chosen embeddings
texts = ['']  # Replace with actual documents
vectorstore = FAISS.from_texts(texts, embedding)


retrieved_information = []

text_splitter: TextSplitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=50)

url_database: List[str] = Field(
    default_factory=list, description="List of processed URLs"
)

url_database: List[str] = []
