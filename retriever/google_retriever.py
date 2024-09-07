#Custom Search JSON API provides 100 search queries per day for free. If you need more, you may sign up for billing in the API Console. Additional requests cost $5 per 1000 queries, up to 10k queries per day.
# from bs4 import BeautifulSoup
# from rank_bm25 import BM25Okapi
# import numpy as np
import requests
from dotenv import load_dotenv 
import os
# loading variables from .env file
load_dotenv()
# Set up Google Custom Search API
API_KEY = os.getenv('GOOGLE_API_KEY')
SEARCH_ENGINE_ID = os.getenv('GOOGLE_CSE_ID')
NUMOFSITES = 5
SEARCH_URL = f'https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&num={NUMOFSITES}&q='

def google_search(query):
    response = requests.get(SEARCH_URL + query)
    search_results = response.json()
    return [item['snippet'] for item in search_results['items']]  # Extract snippets from search results
    # return search_results # Extract snippets from search results

# def extract_text_from_website(url):
#     try:
#         response = requests.get(url)
#         soup = BeautifulSoup(response.content, 'html.parser')
#         # Extract text from the website, limit to the first 100 words
#         text = ' '.join([p.text for p in soup.find_all('p') if p.text])
#         return ' '.join(text.split())  # Limit to the first 100 words
#     except Exception as e:
#         print(f"Failed to extract text from {url}: {str(e)}")
#         return None
    
# def search_and_extract(query):
#     search_results = search(query)
#     extracted_texts = []

#     if search_results and 'items' in search_results:
#         for item in search_results['items']:
#             link = item.get('link', '')
#             text = extract_text_from_website(link)
#             if text:
#                 extracted_texts.append(text)

#     return extracted_texts

# def bm25_extract(query, texts):
#     tokenized_texts = [text.split() for text in texts]
#     bm25 = BM25Okapi(tokenized_texts)
#     tokenized_query = query.split()
#     scores = bm25.get_scores(tokenized_query)
#     top_text_index = np.argmax(scores) 
#     return texts[top_text_index]

