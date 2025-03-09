
import os
from dotenv import load_dotenv
from serpapi import GoogleSearch
from tqdm import tqdm

load_dotenv()
SERP_API_KEY = os.environ.get('SERP_API_KEY')
url = "https://google.serper.dev/search"

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
        answer = None

    return answer


def grounding(question):
    try:
        print(question)
        ga = google(question)
        return ga
    except:
        return None

print(grounding("Did the 2017 tax bill deliver the largest tax cuts in American history?"))

class Khansir():
    def __init__(self, length):
        self.length = length