from retriever.google_retriever import google_search
from retriever.ddg_retriever import ddg_search
from retriever.qa_retriever.google_qa_retriever import langchain_qa
from retriever.serper_retriever import serper_search

def retrieve(query):
    return serper_search(query)