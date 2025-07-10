import arxiv
import requests
from bs4 import BeautifulSoup
import feedparser
# ----------- 1. Fetch Academic Papers from arXiv -----------
def fetch_arxiv_papers(query="Artificial intelligence", max_results=3):
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )
    papers = []
    for result in search.results():
        papers.append({
            "title": result.title.strip(),
            "summary": result.summary.strip(),
            "url": result.entry_id
        })
    return papers

# ----------- 2. Fetch News from Google News RSS -----------
def fetch_google_news(query="Artificial intelligence", max_articles=3):
    url = f"https://news.google.com/rss/search?q={query.replace(' ', '+')}&hl=en-US&gl=US&ceid=US:en"
    feed = feedparser.parse(url)
    news_items = []
    for entry in feed.entries[:max_articles]:
        news_items.append({
            "title": entry.title.strip(),
            "summary": entry.summary.strip(),
            "link": entry.link
        })
    return news_items
"""
# ----------- 3. Scrape Company News from Plug Power -----------
def scrape_plug_power_news(max_articles=3):
    url = "https://www.plugpower.com/news/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    articles = soup.select("div.news-list-item")
    news_items = []
    for article in articles[:max_articles]:
        title = article.select_one("h3").get_text(strip=True)
        summary = article.select_one("p").get_text(strip=True)
        link = article.find("a")["href"]
        news_items.append({
            "title": title,
            "summary": summary,
            "link": link
        })
    return news_items
"""