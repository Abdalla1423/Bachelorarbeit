from retriever.retriever import retrieve
from models.models import askModel


def veracityPrediction(claim, information):
  return askModel(f'''You are a well-informed and expert fact-checker.
You are provided with information regarding the following claim: {claim}
These is the provided information to verify the claim:
< {information}>
Based on the main claim and the information provided, You have to provide:
- claim: the original claim,
- rating: choose among true, half-true and false
- factcheck: and the detailed and elaborate fact-check paragraph.
please output your response in the demanded json format''')

def direct(claim):
    information = retrieve(claim)
    return veracityPrediction(claim, information)




