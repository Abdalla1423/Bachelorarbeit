import spacy
from retriever.retriever import retrieve
from models.models import askModel
import pytextrank
from prompt_frameworks.veracity_prediction import veracityPrediction



# Set up spaCy
nlp = spacy.load("en_core_web_sm")
nlp.add_pipe("textrank")


def extract_keywords_2(text):

    # load a spaCy model, depending on language, scale, etc.

    # add PyTextRank to the spaCy pipeline
    
    doc = nlp(text)

    # examine the top-ranked phrases in the document
    
    return " ".join([phrase.text for phrase in doc._.phrases[:5]])

def keyword(claim):
    # TEXTRANK
    # pure_claim = claim.split("says")[1]
    keyword_sentence = extract_keywords_2(claim)
    information = retrieve(keyword_sentence)
    return veracityPrediction(claim, information)



