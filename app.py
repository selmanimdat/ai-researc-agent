import feedparser
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import markdown
import pdfkit
from scrapers import fetch_arxiv_papers,fetch_google_news
import os
from dotenv import load_dotenv


load_dotenv()
# ----------- 4. Summarize using OpenRouter model -----------
def summarize_items_openrouter(items, section_title, api_key):
    combined_text = "\n\n".join([f"Title: {item['title']}\nSummary: {item['summary']}" for item in items])
    prompt = f"""You're an data scientist. Summarize the following {section_title.lower()} into 3–5 concise bullet points:\n\n{combined_text}"""

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        json={
            "model": "qwen/qwen2.5-vl-32b-instruct:free",  # <-- kontrol et
            "messages": [
                {"role": "user", "content": prompt}
            ]
        },
        headers={
            "Authorization": f"Bearer {api_key}"
        }
    )

    print("DEBUG STATUS:", response.status_code)
    print("DEBUG RESPONSE:", response.text)  # <-- hata cevabını yazdır

    result = response.json()
    
    if "choices" not in result:
        raise ValueError(f"OpenRouter API response error: {result}")
    
    return result["choices"][0]["message"]["content"].strip()

# ----------- 5. Build the Daily Report -----------
def build_daily_report(api_key):
    today = datetime.today().strftime('%Y-%m-%d')
    report = f"# 🔋 Daily Artificial Inteligence Report ({today})\n\n"

    print("Fetching academic papers from arXiv...")
    arxiv_data = fetch_arxiv_papers()

    print("Fetching news from Google News...")
    google_news_data = fetch_google_news()

    print("Summarizing arXiv papers with OpenRouter...")
    arxiv_summary = summarize_items_openrouter(arxiv_data, "Academic Papers", api_key)
    report += "## 📘 Academic Papers (arXiv)\n" + arxiv_summary + "\n\n"

    print("Summarizing news articles with OpenRouter...")
    news_summary = summarize_items_openrouter(google_news_data, "News Articles", api_key)
    report += "## 🗞 News Articles (Google News)\n" + news_summary + "\n\n"

    return report

def save_as_pdf_md(md_text, filename=f"report ({today}).pdf"):
    html = markdown.markdown(md_text)
    pdfkit.from_string(html, filename)

# ----------- 6. Run It! -----------
if __name__ == "__main__":
    api_key = os.getenv("API_KEY")
    API_KEY = api_key
    final_report = build_daily_report(API_KEY)
    print(final_report)
    save_as_pdf_md(final_report)
