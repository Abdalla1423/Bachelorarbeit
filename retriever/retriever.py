from retriever.serper_retriever import serper_search

current_retriever = "SERPER_WEBSEARCH"

def set_retriever(retriever):
    global current_retriever
    current_retriever = retriever

def retrieve(query):
    if current_retriever == "SERPER_WEBSEARCH":
        return serper_search(query)
