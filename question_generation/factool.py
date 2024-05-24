from openai import OpenAI
from dotenv import load_dotenv 

load_dotenv()

client = OpenAI()

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages = [ 
    {"role": "user", "content": '''
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
Now complete the following: [claim]: US hospitals caught injecting experimental Ebola vaccine that sheds! [response]:
     '''}
  ]
)

print(completion.choices[0].message)