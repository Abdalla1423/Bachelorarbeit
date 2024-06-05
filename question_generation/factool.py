from openai import OpenAI
from dotenv import load_dotenv 
from langchain.agents import AgentType,initialize_agent,load_tools
from langchain.chat_models import ChatOpenAI

load_dotenv()
llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)


def gptAsk(prompt):
  answer = llm.invoke(prompt)
  return answer.content

def question_generation(claim):
  questions = gptAsk(f'''
You are a query generator designed to help users verify a given claim using
search engines. Your primary task is to generate a Python list of two effective
and skeptical search engine queries. These queries should assist users in critically evaluating the factuality of a provided claim using search engines. You
should only respond in format as described below (a Python list of queries).
PLEASE STRICTLY FOLLOW THE FORMAT. DO NOT RETURN ANYTHING ELSE. START YOUR RESPONSE WITH ’[’. [response format]:
['query1', 'query2']
Here are 3 examples: [claim]: The CEO of twitter is Bill Gates. [response]:
["Who is the CEO of twitter?", "CEO Twitter"]
[claim]: Michael Phelps is the most decorated Olympian of all time. [response]:
["Who is the most decorated Olympian of all time?", "Michael Phelps"]
[claim]: ChatGPT is created by Google. [response]: ["Who created ChatGPT?",
"ChatGPT"]
Now complete the following: [claim]: {claim}! [response]:
  
     ''')
  
  return questions

def questionAnswering(question):
  tools=load_tools(["ddg-search"],llm=llm)
  agent=initialize_agent(tools,llm,agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,verbose=True, handle_parsing_errors=True)
  return agent.run(question)


generated_questions = question_generation("McDonald’s makes you all sign noncompete contracts that you cannot go across town to try to get a job at Burger King.")
print(generated_questions)
