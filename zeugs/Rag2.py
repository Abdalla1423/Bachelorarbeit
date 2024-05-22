import torch
from transformers import RagTokenizer, RagRetriever, RagTokenForGeneration
import requests

# Set up Google Custom Search API
API_KEY = 'AIzaSyDg0fyxzCryy5HLzATM4o6JorjkopyJosU'
SEARCH_ENGINE_ID = '110107dc3540c43cf'
SEARCH_URL = f'https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q='

# Instantiate RAG tokenizer
tokenizer = RagTokenizer.from_pretrained("facebook/rag-token-nq")

# Set up retriever
retriever = RagRetriever.from_pretrained("facebook/rag-token-nq", index_name="exact", use_dummy_dataset=True)

# Set retriever
generator = RagTokenForGeneration.from_pretrained("facebook/rag-token-nq")
generator.set_retriever(retriever)

# Function to query search engine and return search results
def search(query):
    response = requests.get(SEARCH_URL + query)
    data = response.json()
    return [item['snippet'] for item in data['items']]  # Extract snippets from search results

# Function to generate context and perform question answering
def ask_question(question):
    search_results = search(question)
    context = " ".join(search_results)  # Concatenate snippets to form context
    context_input = tokenizer(context, return_tensors="pt", padding=True, truncation=True)
    n_docs = context_input["input_ids"].shape[0]  # Calculate the number of documents
    inputs = {
        "input_ids": context_input["input_ids"],
        "attention_mask": context_input["attention_mask"],
        "decoder_input_ids": tokenizer(question, return_tensors="pt").input_ids,
        "context_input_ids": context_input["input_ids"].repeat(1, 1),  # Repeat to match n_docs
        "context_attention_mask": context_input["attention_mask"].repeat(1, 1),  # Repeat to match n_docs
        "doc_scores": torch.ones((1, context_input["input_ids"].shape[1]), dtype=torch.float),  # Dummy
        "n_docs": n_docs
    }

    # Generate answer
    generated_ids = generator.generate(**inputs, max_length=20)
    answer = tokenizer.decode(generated_ids[0], skip_special_tokens=True)
    
    return answer


# Example usage
question = "Who was president of the U.S. when superconductivity was discovered?"
answer = ask_question(question)
print("Answer:", answer)

