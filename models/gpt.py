from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()


def askGPT4(prompt, stop=None):
    GPT_4 = ChatOpenAI(model_name="gpt-4o", temperature=0, streaming=False)
    answer = GPT_4.invoke(prompt, stop=stop)
    return answer.content
