# 2500 free searches
import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()
SERPER_API_KEY = os.environ.get('SERPER_API_KEY')
url = "https://google.serper.dev/search"

def serper_search(query):
  payload = json.dumps({
    "q": query
  })
  headers = {
    'X-API-KEY': SERPER_API_KEY,
    'Content-Type': 'application/json'
  }

  response = requests.request("POST", url, headers=headers, data=payload)
  
  return response.text

print(serper_search('Apple'))