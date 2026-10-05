import requests
from bs4 import BeautifulSoup
import re

class WebScraperTool:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9,hi;q=0.8"
        }

    def scrape_clean_text(self, url: str, max_words: int = 1500):
        """
        Fetches web page HTML, removes script/style/nav noise, and returns clean plain text.
        """
        if not url or not url.startswith("http"):
            return {
                "success": False,
                "error": "Invalid URL provided.",
                "url": url,
                "clean_text": ""
            }

        try:
            response = requests.get(url, headers=self.headers, timeout=8)
            if response.status_code != 200:
                return {
                    "success": False,
                    "error": f"HTTP status {response.status_code}",
                    "url": url,
                    "clean_text": ""
                }

            soup = BeautifulSoup(response.text, "html.parser")

            # Remove unwanted tags
            for tag in soup(["script", "style", "nav", "footer", "header", "aside", "form", "svg"]):
                tag.decompose()

            # Extract text from main content area if available, else body
            main_content = soup.find("main") or soup.find("article") or soup.find("body") or soup
            raw_text = main_content.get_text(separator="\n")

            # Clean up whitespace and empty lines
            lines = [line.strip() for line in raw_text.splitlines() if line.strip()]
            cleaned_text = "\n".join(lines)

            # Limit word length
            words = cleaned_text.split()
            if len(words) > max_words:
                cleaned_text = " ".join(words[:max_words]) + "..."

            return {
                "success": True,
                "url": url,
                "title": soup.title.string.strip() if soup.title else "",
                "clean_text": cleaned_text,
                "word_count": len(words)
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"Scraping error: {str(e)}",
                "url": url,
                "clean_text": ""
            }

# Instantiated helper instance
web_scraper = WebScraperTool()
