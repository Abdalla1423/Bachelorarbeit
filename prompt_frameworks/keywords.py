import spacy
from retriever.retriever import retrieve
from prompt_frameworks.veracity_prediction import veracityPrediction
import pytextrank


def extract_keywords(text):
    # Set up spaCy
    nlp = spacy.load("en_core_web_sm")
    nlp.add_pipe("textrank")

    # add PyTextRank to the spaCy pipeline
    doc = nlp(text)

    # extract the top-ranked phrases in the document
    return " ".join([phrase.text for phrase in doc._.phrases[:5]])


# The 'keyword' search uses keyword phrases to retrieve external information:
#
# Step 1: Extract the most relevant keywords from the claim via PyTextRank (spaCy pipeline).
#         and form a keyword sentence out of them
# Step 2: Use the keywords sentence to retrieve external information.
# Step 3: Pass the original claim and retrieved data to the veracityPrediction
#         to determine the claim’s veracity.

def keyword(claim):
    keyword_sentence = extract_keywords(claim)
    information = retrieve(keyword_sentence)
    return veracityPrediction(claim, information)
