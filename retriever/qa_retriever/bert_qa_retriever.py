
import torch
from transformers import BertForQuestionAnswering, BertTokenizer
from dotenv import load_dotenv 
import os
from retriever.google_retriever import google_search
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


question = 'Who was president of the U.S. when superconductivitywas discovered?'
print('Question: ' + question)
context_list = google_search(question)
context = ', '.join(context_list)
print('Context: ' + context)
answer = qa(question, context)
print('Answer: ' + answer)
    


