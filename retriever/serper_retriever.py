# 2500 free searches
import requests
from bs4 import BeautifulSoup
import requests
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
import requests
import json
import os
from dotenv import load_dotenv
import ast
from serpapi import GoogleSearch
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from newspaper import Article
from PyPDF2 import PdfReader
from io import BytesIO
import time
# nltk.download('punkt')
# nltk.download('punkt_tab')

from retriever.info import retrieved_information

load_dotenv()
SERPER_API_KEY = os.environ.get('SERPER_API_KEY')
SERP_API_KEY = os.environ.get('SERP_API_KEY')
url = "https://google.serper.dev/search"


fact_checking_domains = [
    "snopes.com",
    "politifact.com",
    "politifact",
    "factcheck.org",
    "truthorfiction.com",
    "fullfact.org",
    "leadstories.com",
    "factcheck.afp.com",
    "reuters.com/fact-check",
    "washingtonpost.com/news/fact-checker",
    "apnews.com/APFactCheck",
    "mediabiasfactcheck.com",
    "theferret.scot",
    "africacheck.org",
    "poynter.org",
    "checkyourfact.com",
    "vox.com/fact-check",
    "opensecrets.org",
    "hoax-slayer.com",
    "facta.news",
    "maldita.es",
    "verafiles.org",
    "boomlive.in",
    "altnews.in"
]

social_media_websites = [
    "facebook.com",
    "twitter.com",
    "x.com",
    "instagram.com",
    "reddit.com",
    "youtube.com",
]

fake_news_websites = [
    "infowars.com",
    "breitbart.com",
    "yournewswire.com",
    "theonion.com",  # Satirical site often confused with real news
    "naturalnews.com",
    "prntly.com",
    "rt.com",  # Russian state-sponsored outlet often accused of disinformation
    "sputniknews.com",  # Another Russian state-sponsored news site
    "newswars.com",
    "beforeitsnews.com",
    "conservativedailypost.com",
    "americannews.com",
    "libertywriters.com",
    "truepundit.com",
    "gatewaypundit.com",
    "dailywire.com",
    "wakingtimes.com",
    "neonnettle.com",
    "worldtruth.tv",
    "realnewsrightnow.com",  # Satirical
    "now8news.com"
]

# List of restricted domains
restricted_domains = fact_checking_domains + social_media_websites + fake_news_websites
# restricted_domains = ["politifact", "factcheck.org", "snopes.com"]


def scrape_website_content(url):
    try:
        
      headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com",
      }
      response = requests.get(url, headers=headers, timeout=5)
      response.raise_for_status()  # Check if the request was successful
      
      # Check if the content type is PDF
      # Check the content type
      content_type = response.headers.get('Content-Type', '').lower()
      
      if 'text/html' in content_type or 'application/xhtml+xml' in content_type or 'text/xml' in content_type:
          # Handle HTML or XML content with BeautifulSoup
          try:
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract text from paragraphs
            paragraphs = soup.find_all('p')
            content = "\n".join([para.get_text() for para in paragraphs])

            return content
          except:
            return None

      elif 'application/pdf' in content_type:
          # Handle PDF content with PyPDF2
          try:
            pdf_content = BytesIO(response.content)
            reader = PdfReader(pdf_content)
            text = ""
            for page in reader.pages:
                text += page.extract_text()

            return text
          except:
            return None

      else:
          # Reject any other content type
          print(f"Unsupported content type: {content_type}. Only HTML, XML, and PDF are accepted.")
          return None

    except requests.exceptions.RequestException as e:
      try:
        # print("Trying newspaper...")
        article = Article(url=url, language='en')
        article.download()
        article.parse()
        return article.text
      except:
        print(f"Failed to retrieve {url}: {e}")
      return None

# Function to rank sentences by similarity to the query using TF-IDF and cosine similarity
def rank_sentences(text, query, top_n = 2):
    sentences = nltk.sent_tokenize(text)
    # Combine the query and sentences to create a corpus
    corpus = [query] + sentences

    # Vectorize the corpus using TF-IDF
    vectorizer = TfidfVectorizer().fit_transform(corpus)
    vectors = vectorizer.toarray()

    # Calculate cosine similarity between the query vector and all sentence vectors
    try:
      cosine_similarities = cosine_similarity(vectors[0:1], vectors[1:]).flatten()
    except:
       return None

    # Get the top_n most relevant sentences
    relevant_indices = cosine_similarities.argsort()[-top_n:][::-1]
    relevant_passages = [sentences[i] for i in relevant_indices]
    return relevant_passages

def extract_and_rank(url, query):
  content = scrape_website_content(url)
  if content:
    ranked_sentences = rank_sentences(content, query)
    if ranked_sentences:
      result = "".join([sentence for sentence in ranked_sentences])
      return result
    else:
       return None
  else:
    return None

def serper_search(query):
  time.sleep(2)
  payload = json.dumps({
    "q": query,
    "num": 5,
  })
  headers = {
    'X-API-KEY': SERPER_API_KEY,
    'Content-Type': 'application/json'
  }

  response = requests.request("POST", url, headers=headers, data=payload, timeout=30)
  
  response = ast.literal_eval(response.text)
  
  information = []
  
  info_and_source = []
  
  if 'organic' not in response:
    return ['No information']
    
    # Extract snippets and filter out restricted domains
  for item in response['organic']:
      snippet = item.get('snippet', '')
      domain = item.get('link', '')
      # print("DOMAIN", domain)
      if not any(restricted_domain in domain for restricted_domain in restricted_domains):
        # content = extract_and_rank(domain, query)
        # if content:
        #   information.append(content)
        #   info_and_source.append((content, domain))
        information.append(snippet)
        info_and_source.append((snippet, domain))
        # if snippet:
        #   information.append(snippet)
        #   info_and_source.append((snippet, domain))
        
  retrieved_information.append((query, info_and_source))
  
  return information

def google(question):
    params = {
        "api_key": SERP_API_KEY,
        "engine": "google",
        "q": question,
        "google_domain": "google.com",
        "gl": "us",
        "hl": "en",
    }

    search = GoogleSearch(params)
    result = search.get_dict()

    if "answer_box" in result.keys() and "answer" in result["answer_box"].keys():
        answer = result["answer_box"]["answer"]
    elif "answer_box" in result.keys() and "snippet" in result["answer_box"].keys():
        answer = result["answer_box"]["snippet"]
    elif (
        "answer_box" in result.keys()
        and "snippet_highlighted_words" in result["answer_box"].keys()
    ):
        answer = result["answer_box"]["snippet_highlighted_words"][0]
    elif "snippet" in result["organic_results"][0].keys():
        answer = result["organic_results"][0]["snippet"]
    else:
        answer = "No results found"

    return answer
  