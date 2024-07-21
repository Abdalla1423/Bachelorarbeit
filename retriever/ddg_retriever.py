# free but rate limit
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper

def ddg_search(query):
    wrapper = DuckDuckGoSearchAPIWrapper(region="de-de", time="d", max_results=2)
    search = DuckDuckGoSearchResults(api_wrapper=wrapper, source="news")
    return search.run(query)

print(ddg_search("Obama's first name?"))