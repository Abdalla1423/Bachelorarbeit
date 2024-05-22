import requests
import json
import nltk
import spacy
import gensim
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
import string
from gensim.parsing.preprocessing import remove_stopwords
from newspaper import Article
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import transformers
import torch
from keybert import KeyBERT
from keyphrase_vectorizers import KeyphraseCountVectorizer


# Set up nltk
nltk.download('punkt')
nltk.download('stopwords')

# Set up spaCy
nlp = spacy.load("en_core_web_sm")

# New York Times API key
api_key = 'aDWAAlAO3sGXFORte4D8KnObpxxp6g4R'

def get_article_text(topic):
    # Step 1: Use the New York Times API to retrieve the URL of the most recent article
    url = f'https://api.nytimes.com/svc/search/v2/articlesearch.json?q={topic}&api-key={api_key}'
    response = requests.get(url)
    if response.status_code != 200:
        print("Error:", response.status_code)
        return None
    
    data = response.json()
    if not data['response']['docs']:
        print("Error: No article found")
        return None
    
    # Extract the URL of the most recent article
    article_url = data['response']['docs'][0]['web_url']
    
    # Step 2: Use the URL obtained to fetch the HTML content of the article
    try:
        article = Article(article_url)
        article.download()
        article.parse()
        return article.text
    except Exception as e:
        print(f"Error: {e}")
        return None


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
    weighted_key_words = kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 1), stop_words=None)
    return [x[0] for x in weighted_key_words]

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

def extract_topics(text):
    '''
    It removes common stop words and punctuation from the input text to clean it using remove_stopwords() from gensim.parsing.preprocessing and string.punctuation.
    The cleaned text is then tokenized into individual words.
    Next, it constructs a dictionary mapping each word to a unique integer ID using Dictionary from gensim.corpora.
    Using this dictionary, it creates a bag-of-words representation of the text, where each word is represented by its ID and its frequency.
    Finally, it trains an LDA model using LdaMulticore from gensim.models on the bag-of-words representation to identify the underlying topics present in the text.
    '''
    # Remove stopwords, punctuation, single letters, and quotes
    text = remove_stopwords(text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # Tokenize the text
    tokens = word_tokenize(text)
    
    # Filter out single letters, quotes, and empty strings
    filtered_tokens = [token for token in tokens if len(token) > 1 and not token.isdigit() and token.lower() != 'the']
    
    # Create a dictionary from the filtered tokens
    dictionary = gensim.corpora.Dictionary([filtered_tokens])
    
    # Create a bag of words representation
    bow_corpus = [dictionary.doc2bow(filtered_tokens)]
    
    # Train an LDA model
    lda_model = gensim.models.LdaMulticore(bow_corpus, num_topics=2, id2word=dictionary, passes=2)
    
    # Get the top word for each topic, ensuring diversity
    topics = []
    used_words = set()  # Keep track of words already used for topics
    for _, topic_words in lda_model.print_topics():
        for word in topic_words.split(" + "):
            word = word.split("*")[1].strip('"')
            if word not in used_words:
                topics.append(word)
                used_words.add(word)
                break
    
    return topics

def get_wikipedia_summary(topic):
    # try:
    #     article = Article(f"en.wikipedia.org/w/api.php?action=query&titles={topic}&prop=extracts&format=json")
    #     article.download()
    #     article.parse()
    #     return article.text
    # except Exception as e:
    #     print(f"Error: {e}")
    #     return None
    
    try:
        response = requests.get(f"https://en.wikipedia.org/api/rest_v1/page/summary/{topic}")
        response.raise_for_status()
        data = response.json()
        return data.get("extract", "")
    except requests.exceptions.RequestException as e:
        print("Error retrieving Wikipedia summary:", e)
        return ""

def get_reddit_posts(topic):
    try:
        response = requests.get(f"https://www.reddit.com/search.json?q={topic}", headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
        data = response.json()
        posts = [post["data"]["title"] for post in data["data"]["children"]]
        return " ".join(posts)
    except requests.exceptions.RequestException as e:
        print("Error retrieving Reddit posts:", e)
        return ""

def summarize_text(text):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, 2)  # Summarize to 2 sentences
    return " ".join(str(sentence) for sentence in summary)

def get_article_summaries(topics):
    article_summaries = []
    for topic in topics:
        wikipedia_summary = get_wikipedia_summary(topic)
        reddit_posts = get_reddit_posts(topic)
        #news summaries: https://newsapi.ai/documentation?tab=searchArticles
        #wikipedia_summary_summary = summarize_text(wikipedia_summary)
        reddit_posts_summary = summarize_text(reddit_posts)
        article_summaries.append((topic, wikipedia_summary, reddit_posts_summary))
    return article_summaries

if __name__ == "__main__":
    # Example article ID
    topic = 'Navalny'
    
    # Retrieve the article
    article_text = get_article_text(topic)
    if article_text:
        print(article_text)
    # if article_data:
    #     #print(article_data["response"]['docs'][2]['abstract'])
    #     # Extract text from the article
    #     article_text = ''
    #     for doc in article_data['response']['docs']:
    #         article_text += doc['abstract'] + ' '  # Assuming abstract contains the main text
    #     #print(article_text)

        # Extract keywords
        keywords = extract_keywords(article_text)
        print("Keywords:", keywords)

        # Extract entities
        entities = extract_entities(article_text)
        print("Entities:", entities)

        # Extract topics
        topics = extract_topics(article_text)
        print("Topics:")
        for topic in topics:
            print(topic)

        article_summaries = get_article_summaries(topics)

        # Output summarized articles
        for i, (topic, wikipedia_summary, reddit_posts_summary) in enumerate(article_summaries):
            print(f"Topic {i+1} Summary for topic '{topic}':")
            print("Wikipedia Summary:")
            print(wikipedia_summary)
            print("\nReddit Posts Summary:")
            print(reddit_posts_summary)
            print("\n---\n")
    else:
        print("Failed to retrieve article.")
