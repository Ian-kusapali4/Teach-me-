"""Web scraping helpers (placeholder)."""
from bs4 import BeautifulSoup

def scrape_html(html: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")
    return {"title": soup.title.string if soup.title else None}
