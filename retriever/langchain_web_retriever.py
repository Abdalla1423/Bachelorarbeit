import requests
from bs4 import BeautifulSoup
import requests
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import re
import time
import requests
import json
import os
from dotenv import load_dotenv
import ast
from serpapi import GoogleSearch
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from selenium import webdriver
from newspaper import Article
nltk.download('punkt')
nltk.download('punkt_tab')
load_dotenv()
SERPER_API_KEY = os.environ.get('SERPER_API_KEY')
SERP_API_KEY = os.environ.get('SERP_API_KEY')
url = "https://google.serper.dev/search"

import logging
import re
from typing import List

from langchain_community.document_loaders import AsyncHtmlLoader
from langchain_community.document_transformers import Html2TextTransformer

from langchain_core.documents import Document

from retriever.info import vectorstore, text_splitter, url_database

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


logger = logging.getLogger(__name__)
       
def _get_relevant_documents(
        query: str,
    ) -> List[Document]:
        """Search Google for documents related to the query input.

        Args:
            query: user query

        Returns:
            Relevant documents from all various urls.
        """

    
        # Get urls
        logger.info("Searching for relevant urls...")
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
        
        urls_to_look = []
        
        if 'organic' not in response:
            return ['No information']
    
    # Extract snippets and filter out restricted domains
        for item in response['organic']:
            domain = item.get('link', '')
            # print("DOMAIN", domain)
            if not any(restricted_domain in domain for restricted_domain in restricted_domains):
                urls_to_look.append(domain)
        # Relevant urls
        urls = set(urls_to_look)
        print(urls)

        # Check for any new urls that we have not processed
        new_urls = list(urls.difference(url_database))

        logger.info(f"New URLs to load: {new_urls}")
        # Load, split, and add new urls to vectorstore
        if new_urls:
            loader = AsyncHtmlLoader(new_urls, ignore_load_errors=True)
            html2text = Html2TextTransformer()
            logger.info("Indexing new urls...")
            docs = loader.load()
            docs = list(html2text.transform_documents(docs))
            docs = text_splitter.split_documents(docs)
            vectorstore.add_documents(docs)
            url_database.extend(new_urls)

        # Search for relevant splits
        # TODO: make this async
        logger.info("Grabbing most relevant splits from urls...")
        docs = []
        docs.extend(vectorstore.similarity_search(query, k = 2))

        # Get unique docs
        unique_documents_dict = {
            (doc.page_content, tuple(sorted(doc.metadata.items()))): doc for doc in docs
        }
        unique_documents = list(unique_documents_dict.values())
        page_contents = [doc.page_content for doc in unique_documents]
        return page_contents



# print(_get_relevant_documents('Who are Havel-Hakimi algorithm named after?'))
