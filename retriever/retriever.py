from retriever.google_retriever import google_search
from retriever.ddg_retriever import ddg_search

def retrieve(query):
    return ddg_search(query)