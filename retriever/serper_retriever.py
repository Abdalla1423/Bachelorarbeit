# 2500 free searches
import requests
import json
import os
from dotenv import load_dotenv
import ast
load_dotenv()
SERPER_API_KEY = os.environ.get('SERPER_API_KEY')
url = "https://google.serper.dev/search"

# List of restricted domains
restricted_domains = ["politifact.com", "factcheck.org", "snopes.com"]

def serper_search(query):
  payload = json.dumps({
    "q": query,
    "num": 10,
  })
  headers = {
    'X-API-KEY': SERPER_API_KEY,
    'Content-Type': 'application/json'
  }

  response = requests.request("POST", url, headers=headers, data=payload)
  response = ast.literal_eval(response.text)
  
  information = []
    
    # Extract snippets and filter out restricted domains
  for item in response['organic']:
      snippet = item.get('snippet', '')
      domain = item.get('link', '')
      if not any(restricted_domain in domain for restricted_domain in restricted_domains):
          information.append(snippet)
  
  return information
  
  # information =  [item.get('snippet', '') for item in response['organic']]  # Extract snippets from search results

  
# print(serper_search('Apple'))