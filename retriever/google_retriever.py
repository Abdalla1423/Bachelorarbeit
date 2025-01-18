import requests
from dotenv import load_dotenv 
import os
load_dotenv()
API_KEY = os.getenv('GOOGLE_API_KEY')
SEARCH_ENGINE_ID = os.getenv('GOOGLE_CSE_ID')
NUMOFSITES = 5
SEARCH_URL = f'https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&num={NUMOFSITES}&q='

def google_search(query):
    response = requests.get(SEARCH_URL + query)
    search_results = response.json()
    return [item['snippet'] for item in search_results['items']]  # Extract snippets from search results
    # return search_results # Extract snippets from search results
