
import nltk
import spacy
from keybert import KeyBERT
import pytextrank
from rake_nltk import Rake
from yake import KeywordExtractor
import spacy
from collections import Counter
from string import punctuation
from retriever.retriever import retrieve
from models.models import askModel




# Set up nltk
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('punkt_tab')

# Set up spaCy
nlp = spacy.load("en_core_web_sm")
nlp.add_pipe("textrank")

def extract_keywords_0(text):
    doc = nlp(text)
    return doc.ents


def extract_keywords(text):
    '''
    The function first tokenizes the input text into individual words using word_tokenize() from the nltk.tokenize module.
    It removes common stop words (e.g., 'the', 'is', 'and') from the tokenized words list using stopwords.words('english') from the nltk.corpus module.
    Next, it counts the frequency of each remaining word using a Counter object.
    Finally, it selects the top 10 most frequent words and returns them as keywords.
    '''
    # # Tokenize the text
    # tokens = word_tokenize(text)
    
    # # Remove stop words
    # stop_words = set(stopwords.words('english'))
    # filtered_tokens = [word.lower() for word in tokens if word.isalnum() and word.lower() not in stop_words]
    
    # # Get word frequency
    # word_freq = Counter(filtered_tokens)
    
    # # Get top keywords
    # top_keywords = word_freq.most_common(5)
    # return [keyword for keyword, _ in top_keywords]
    # Load the BERT model and create a new tokenizer 
    kw_model = KeyBERT()
    #weighted_key_words = kw_model.extract_keywords(text, vectorizer=KeyphraseCountVectorizer())
    weighted_key_words = kw_model.extract_keywords(text,keyphrase_ngram_range=(1, 2), stop_words=None)
    return " ".join([x[0] for x in weighted_key_words])

def extract_entities(text):
    '''
    It loads the English language model for spaCy (en_core_web_sm) using spacy.load().
    The function then processes the input text using the loaded spaCy model, which performs named entity recognition (NER).
    Each detected named entity is represented as a tuple containing the text of the entity and its label (e.g., PERSON, ORGANIZATION).
    The function collects all detected entities and returns them as a list of tuples.
    '''
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities

# Installation

def extract_keywords_2(text):

    # load a spaCy model, depending on language, scale, etc.

    # add PyTextRank to the spaCy pipeline
    
    doc = nlp(text)

    # examine the top-ranked phrases in the document
    
    return " ".join([phrase.text for phrase in doc._.phrases[:5]])

def extract_keywords_3(text):
    

    # Create a Rake instance
    r = Rake()

    # Extract keywords from the text
    r.extract_keywords_from_text(text)

    # Get the ranked keywords
    keywords = r.get_ranked_phrases()

    # Print the extracted keywords and their scores
    # for score, kw in keywords:
    #     print("Keyword:", kw, "Score:", score)
    return " ".join([x for x in keywords])

def extract_keywords_4(text):
    # Create a KeywordExtractor instance
    language = "en"
    max_ngram_size = 2
    deduplication_threshold = 0.3
    numOfKeywords = 5
    kw_extractor = KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_threshold, top=numOfKeywords, features=None)
    

    # Extract keywords from the text
    keywords = kw_extractor.extract_keywords(text)
    # for kw in keywords:
    #     print("Keyword:", kw[0], "Score:", kw[1])

    return " ".join([x[0] for x in keywords])


def get_hotwords(text):
    result = []
    pos_tag = ['PROPN', 'ADJ', 'NOUN'] 
    doc = nlp(text.lower()) 
    for token in doc:
        if(token.text in nlp.Defaults.stop_words or token.text in punctuation):
            continue
        if(token.pos_ in pos_tag):
            result.append(token.text)
    return result

def extract_keywords_5(text):
    output = set(get_hotwords(text))
    most_common_list = Counter(output).most_common(10)
    return " ".join([x[0] for x in most_common_list])

def veracityPrediction(claim, information):
  return askModel(f'''You are a well-informed and expert fact-checker.
You are provided with information regarding the following claim: {claim}
These is the provided information to verify the claim:
< {information}>
Based on the main claim and the information provided, You have to provide:
- claim: the original claim,
- rating: choose among true, half-true and false
- factcheck: and the detailed and elaborate fact-check paragraph.
please output your response in the demanded json format without any additional characters''')

def keyword(claim):
    # TEXTRANK
    keyword_sentence = extract_keywords_2(claim)
    information = retrieve(keyword_sentence)
    return veracityPrediction(claim, information)

# claim = "Alan Grayson stated on July 9, 2015 in an announcement video: In the past two years in Congress, I’ve written more bills, passed more amendments on the floor of the House and enacted more of my bills into law than any other member of the House."
# print(extract_keywords_0(claim))
# print("-------KEYBERT-------")
# print(extract_keywords(claim))
# print("-------TEXTRANK-------")
# print(extract_keywords_2(claim))
# print("-------RAKE-------")
# print(extract_keywords_3(claim))
# print("-------YAKE-------")
# print(extract_keywords_4(claim))
# print("-------SPACY2-------")
# print(extract_keywords_5(claim))


