
import torch
from transformers import BertForQuestionAnswering
from transformers import BertTokenizer
import requests
from bs4 import BeautifulSoup
from rank_bm25 import BM25Okapi
import numpy as np
from dotenv import load_dotenv, dotenv_values 
import os
# loading variables from .env file
load_dotenv()
# Set up Google Custom Search API
API_KEY = os.getenv('GOOGLE_API_KEY')
SEARCH_ENGINE_ID = os.getenv('GOOGLE_CSE_ID')
NUMOFSITES = 5
SEARCH_URL = f'https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&num={NUMOFSITES}&q='

def qa(question, paragraph):
    #Model
    model = BertForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')

    #Tokenizer
    tokenizer = BertTokenizer.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
         
    encoding = tokenizer.encode_plus(text=question,text_pair=paragraph)

    inputs = encoding['input_ids']  #Token embeddings
    sentence_embedding = encoding['token_type_ids']  #Segment embeddings
    tokens = tokenizer.convert_ids_to_tokens(inputs) #input tokens
    output = model(input_ids=torch.tensor([inputs]), token_type_ids=torch.tensor([sentence_embedding]))
    start_index = torch.argmax(output.start_logits)
    end_index = torch.argmax(output.end_logits)

    answer = ' '.join(tokens[start_index:end_index+1])
    corrected_answer = ''

    for word in answer.split(): 
        #If it's a subword token
        if word[0:2] == '##':
            corrected_answer += word[2:]
        else:
            corrected_answer += ' ' + word
    
    return corrected_answer



# Function to query search engine and return search results
def search(query):
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

question = 'Where was Hitler born?'
print('Question: ' + question)
context_list = search(question)
context = ', '.join(context_list)
print('Context: ' + context)
answer = qa(question, context)
print('Answer: ' + answer)
    


