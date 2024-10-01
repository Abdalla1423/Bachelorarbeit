from retriever.google_retriever import google_search
from retriever.ddg_retriever import ddg_search
from retriever.qa_retriever.google_qa_retriever import langchain_qa
from retriever.serper_retriever import serper_search
from retriever.langchain_web_retriever import _get_relevant_documents

def retrieve(query):
    return serper_search(query)