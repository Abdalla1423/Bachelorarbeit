from langchain.agents import AgentType,initialize_agent,load_tools
from models.models import GPT_3
from dotenv import load_dotenv
load_dotenv()
llm = GPT_3
tools=load_tools(["ddg-search"],llm=llm)
agent=initialize_agent(tools,llm,agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,verbose=True, handle_parsing_errors=True)
agent.run("Does the Ebola vaccine shed?")

