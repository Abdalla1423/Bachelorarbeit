from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()

# Models
GPT_3 = ChatOpenAI(model_name="gpt-3.5-turbo-16k", temperature=0, streaming=False)
GPT_4 = ChatOpenAI(model_name="gpt-4", temperature=0, streaming=False)

def askModel(prompt, stop=None):
  # answer = GPT_4.invoke(prompt, stop=stop)
  # return answer.content
  return askLlama(prompt, stop)

def askLlama(prompt, stopSeq):
  openai_api_key = "ollama"
  openai_api_base = "http://localhost:11434/v1"
  client = OpenAI(
      api_key=openai_api_key,
      base_url=openai_api_base,
  )
  completion = client.completions.create(
      model="llama3.1",
      prompt=prompt,
      temperature=0,
      stop=stopSeq
  )

  return completion.choices[0].text