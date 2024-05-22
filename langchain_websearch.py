# https://www.youtube.com/watch?v=JtZgVN84cN8
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
import os
from langchain_google_community import GoogleSearchAPIWrapper
from langchain.retrievers.web_research import WebResearchRetriever
from langchain.chains import RetrievalQAWithSourcesChain
from dotenv import load_dotenv
from langchain_community.tools import DuckDuckGoSearchRun
    
# loading variables from .env file
load_dotenv()

vectorstore = Chroma(embedding_function=OpenAIEmbeddings(), persist_directory="./chroma_db_oai")

llm = ChatOpenAI(model_name="gpt-3.5-turbo-16k", temperature=0, streaming=True, openai_api_key=os.getenv("OPENAI_API_KEY"))

search = GoogleSearchAPIWrapper()

web_research_retriever = WebResearchRetriever.from_llm(
vectorstore=vectorstore,
llm=llm,
search=search,
num_search_results=4,

)

user_input = "What is the first name of Barack Obama?"
qa_chain = RetrievalQAWithSourcesChain.from_chain_type(llm,retriever=web_research_retriever) 
result = qa_chain({"question": user_input})

# we get the results for user query with both answer and source url that were used to generate answer
print(result["answer"])
print(result["sources"])


