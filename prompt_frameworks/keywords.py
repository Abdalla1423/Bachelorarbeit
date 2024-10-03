import spacy
from retriever.retriever import retrieve
from models.models import askModel


# Set up spaCy
nlp = spacy.load("en_core_web_sm")
nlp.add_pipe("textrank")


def extract_keywords_2(text):

    # load a spaCy model, depending on language, scale, etc.

    # add PyTextRank to the spaCy pipeline
    
    doc = nlp(text)

    # examine the top-ranked phrases in the document
    
    return " ".join([phrase.text for phrase in doc._.phrases[:5]])


def veracityPrediction(claim, information):
  return askModel(f'''You are a well-informed and expert fact-checker.
You are provided with information regarding the following claim: {claim}
It is guaranteed that the person made the claim, so focus only on the contents of the claim!
These is the provided information to verify the claim:
< {information}>
Based on the main claim and the information provided, You have to provide:
- claim: the original claim,
- rating: choose between true, false and NEI(not enough information),
- factcheck: and the detailed and elaborate fact-check paragraph.
please output your response in the demanded json format without any additional characters''')

def keyword(claim):
    # TEXTRANK
    pure_claim = claim.split("says")[1]
    keyword_sentence = extract_keywords_2(pure_claim)
    information = retrieve(keyword_sentence)
    return veracityPrediction(claim, information)



