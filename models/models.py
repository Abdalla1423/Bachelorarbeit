#export PYTHONPATH=$PYTHONPATH:/Users/abdallaeltayeb/Desktop/clean_shit
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()

# Models
GPT_3 = ChatOpenAI(model_name="gpt-3.5-turbo-16k", temperature=0, streaming=True)
GPT_4 = ChatOpenAI(model_name="gpt-4", temperature=0, streaming=True)

#invoke GPT
def gptAsk(prompt, stop=None):
  answer = GPT_3.invoke(prompt, stop=stop)
  return answer.content

