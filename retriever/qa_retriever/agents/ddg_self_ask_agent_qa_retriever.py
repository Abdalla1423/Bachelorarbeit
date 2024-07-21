from langchain.agents import AgentType, Tool, initialize_agent
from langchain_community.tools import DuckDuckGoSearchRun
from models.models import GPT_3
from dotenv import load_dotenv 
load_dotenv()


llm = GPT_3
search = search = DuckDuckGoSearchRun()
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
    "Who is the president of the US?"
)