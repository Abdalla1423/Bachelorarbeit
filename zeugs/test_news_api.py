import requests
from newspaper import Article

api_key = "fd36408a907743d68d736c0382899f73"

url = "https://newsapi.org/v2/everything?q=apple&sortBy=publishedAt&apiKey=fd36408a907743d68d736c0382899f73&language=en"
response = requests.get(url)
data = response.json()
article_url = data["articles"][3]["url"]

try:
    article = Article("https://www.engadget.com/oppenheimer-ruled-2024-oscars-as-apple-tv-and-netflix-were-nearly-shut-out-052543094.html?guccounter=1&guce_referrer=aHR0cHM6Ly9uZXdzYXBpLm9yZy8&guce_referrer_sig=AQAAADU64llrEKA8HalOxdSKY7cyl5xJYNFJY97GxdX4z2sOSNkCNUpPZODEWFDHNMM6IOxlVOSP29utATeivQFM0eSEDn79fKN15ilv-miQ1d1WuD0LGAXY-BR3-IiRD3XQxW18JRAY0M4iEJ07G0HA15CJp96x8LESqFbnYr0oXktM")
    article.download()
    article.parse()
    print(article.text)
except Exception as e:
    print(f"Error: {e}")

