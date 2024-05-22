# from langchain.agents import AgentType,initialize_agent,load_tools
# from langchain.chat_models import ChatOpenAI
# from dotenv import load_dotenv, dotenv_values
# load_dotenv()
# llm = ChatOpenAI(model_name="gpt-3.5-turbo-16k", temperature=0, streaming=True)
# tools=load_tools(["ddg-search"],llm=llm)
# agent=initialize_agent(tools,llm,agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,verbose=True, handle_parsing_errors=True)
# agent.run("top 5 business use case on LLM and generative ai")

from langchain.agents import AgentType, Tool, initialize_agent
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_openai import OpenAI
from dotenv import load_dotenv 
load_dotenv()


llm = OpenAI(temperature=0)

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
    "Who was president of the U.S. when superconductivitywas discovered?"
)