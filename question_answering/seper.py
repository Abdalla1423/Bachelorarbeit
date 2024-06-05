from langchain.agents import AgentType, Tool, initialize_agent
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_openai import OpenAI
from dotenv import load_dotenv 
from langchain.chat_models import ChatOpenAI

load_dotenv()


llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)
search = GoogleSerperAPIWrapper()
tools = [
    Tool(
        name="Intermediate Answer",
        func=search.run,
        description="useful for when you need to ask with search",
    )
]

self_ask_with_search = initialize_agent(
    tools, llm, agent=AgentType.SELF_ASK_WITH_SEARCH, verbose=True, handle_parsing_errors=True
)
self_ask_with_search.run(
    "What are the requirements for health risk exceptions in the abortion amendment in Florida?"
)