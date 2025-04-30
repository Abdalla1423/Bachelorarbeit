# 2500 free searches
import requests
import json
import os
from dotenv import load_dotenv
import ast
import time


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
restricted_domains = fact_checking_domains + \
    social_media_websites + fake_news_websites


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

    response = requests.request(
        "POST", url, headers=headers, data=payload, timeout=30)

    response = ast.literal_eval(response.text)

    information = []

    info_and_source = []

    if 'organic' not in response:
        return ['No information']

        # Extract snippets and filter out restricted domains
    for item in response['organic']:
        snippet = item.get('snippet', '')
        domain = item.get('link', '')
        if not any(restricted_domain in domain for restricted_domain in restricted_domains):
            information.append(snippet)
            info_and_source.append((snippet, domain))

    retrieved_information.append((query, info_and_source))

    return information
