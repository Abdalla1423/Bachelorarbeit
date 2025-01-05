# https://www.youtube.com/watch?v=JtZgVN84cN8
# WebResearchRetriever crawls URLs surfaced through the provided search engine. It is possible that some of those URLs will end up pointing to machines residing on an internal network, leadingto an SSRF (Server-Side Request Forgery) attack. To protect yourself against that risk, you can run the requests through a proxy and prevent the crawler from accidentally crawling internal resources.If've taken the necessary precautions, you can set `allow_dangerous_requests` to `True`.
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from models.models import GPT_4
from langchain_google_community import GoogleSearchAPIWrapper
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langchain_community.retrievers.web_research import WebResearchRetriever
from langchain.chains import RetrievalQAWithSourcesChain
from dotenv import load_dotenv
    
def langchain_qa(question):
    # loading variables from .env file
    load_dotenv()

    vectorstore = Chroma(embedding_function=OpenAIEmbeddings(), persist_directory="./chroma_db_oai")

    llm = GPT_4

    search = GoogleSearchAPIWrapper()
    # search = DuckDuckGoSearchAPIWrapper(region="de-de", time="d", max_results=10)

    
    web_research_retriever = WebResearchRetriever.from_llm(
    vectorstore=vectorstore,
    llm=llm,
    search=search,
    allow_dangerous_requests = True,
    num_search_results = 2,
    )
        
    qa_chain = RetrievalQAWithSourcesChain.from_chain_type(llm,retriever=web_research_retriever) 
    result = qa_chain.invoke({"question": question})
    
    return result["answer"]

# result = langchain_qa("Wie viel Uhr ist es in Berlin?")
# print(result["answer"])
# print(result["sources"])

    # # we get the results for user query with both answer and source url that were used to generate answer
    # print(result["answer"])
    # print(result["sources"])


