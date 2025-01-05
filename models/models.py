from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from openai import OpenAI
import ollama

load_dotenv()

# Models
GPT_4_mini = ChatOpenAI(model_name="gpt-4o-mini", temperature=0, streaming=False)
GPT_4 = ChatOpenAI(model_name="gpt-4", temperature=0, streaming=False)

def askModel(prompt, stop=None):
  answer = GPT_4.invoke(prompt, stop=stop)
  return answer.content
  # return askLlama(prompt, stop)

def askLlamaVllm(prompt, stopSeq):
  openai_api_key = "EMPTY"
  openai_api_base = "http://localhost:5000/v1"
  client = OpenAI(
      api_key=openai_api_key,
      base_url=openai_api_base,
  )
  completion = client.chat.completions.create(
      model="meta-llama/Meta-Llama-3.1-8B-Instruct",
      messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt},
    ],
      temperature=0,
      stop=stopSeq
  )

  return completion.choices[0].message.content

def askLlamaOllama(prompt, stopSeq):
  response = ollama.chat(model='llama3.1', messages=[
    {
      'role': 'user',
      'content': prompt,
    },
  ],
  stream= False,
  options = {"stop" : stopSeq}
  )
  return response['message']['content']

