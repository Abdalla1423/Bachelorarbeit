import requests

# Set up Google Custom Search API
API_KEY = 'AIzaSyDg0fyxzCryy5HLzATM4o6JorjkopyJosU'
SEARCH_ENGINE_ID = '110107dc3540c43cf'
SEARCH_URL = f'https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q='

# Function to query search engine and return search results
def search(query):
    response = requests.get(SEARCH_URL + query)
    data = response.json()
    return [item['snippet'] for item in data['items']]  # Extract snippets from search results

print(search(''))