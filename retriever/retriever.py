from retriever.google_retriever import google_search
from retriever.serper_retriever import serper_search

def retrieve(query):
    return serper_search(query)