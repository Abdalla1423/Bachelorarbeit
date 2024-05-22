from langchain.agents import AgentType, Tool, initialize_agent
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_openai import OpenAI
from dotenv import load_dotenv 
load_dotenv()

llm = OpenAI(temperature=0)
search = GoogleSerperAPIWrapper(type="news")
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
    "Who was president of the U.S. when superconductivitywas discovered?"
)