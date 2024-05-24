from googleapiclient.discovery import build
from transformers import RagTokenizer, RagTokenForGeneration, RagRetriever

class GoogleSearchRetriever:
    def __init__(self, api_key, cse_id):
        self.service = build("customsearch", "v1", developerKey=api_key)
        self.cse_id = cse_id

    def retrieve(self, query, num_results=10):
        res = self.service.cse().list(
            q=query,
            cx=self.cse_id,
            num=num_results
        ).execute()
        return [item['snippet'] for item in res.get('items', [])]

class CustomGoogleRagRetriever(RagRetriever):
    def __init__(self, config, question_encoder_tokenizer, generator_tokenizer, google_retriever):
        super().__init__(config, question_encoder_tokenizer, generator_tokenizer)
        self.google_retriever = google_retriever

    def retrieve(self, query, top_k=10):
        return self.google_retriever.retrieve(query, top_k)

# Initialize GoogleSearchRetriever
API_KEY = 'AIzaSyDg0fyxzCryy5HLzATM4o6JorjkopyJosU'
SEARCH_ENGINE_ID = '110107dc3540c43cf'
google_retriever = GoogleSearchRetriever(API_KEY, SEARCH_ENGINE_ID)

# Initialize RAG model
tokenizer = RagTokenizer.from_pretrained("facebook/rag-token-nq")
model = RagTokenForGeneration.from_pretrained("facebook/rag-token-nq")

# Initialize custom retriever
retriever = CustomGoogleRagRetriever(model.config, tokenizer, tokenizer, google_retriever)

# Example query
query = "What is the capital of France?"
input_ids = tokenizer(query, return_tensors="pt").input_ids

# Generate answers
output = model.generate(input_ids, retriever=retriever)
answer = tokenizer.decode(output[0], skip_special_tokens=True)

print("Question:", query)
print("Answer:", answer)
