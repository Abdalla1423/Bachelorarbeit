# free but rate limit
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
import re

def ddg_search(query):
    wrapper = DuckDuckGoSearchAPIWrapper(region="de-de", time="d", max_results=10)
    # search = DuckDuckGoSearchResults(api_wrapper=wrapper, source="news")
    search = DuckDuckGoSearchRun()
    return search.run(query)

# print(ddg_search("Obama's first name?"))

