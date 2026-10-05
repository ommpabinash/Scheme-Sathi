import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

from src.tools.serper_tool import serper_tool
from src.tools.web_scraper import web_scraper

def test_serper_and_scraper():
    print("==================================================")
    print("[TEST] DAY 5: SERPER API WEB SEARCH TOOL")
    print("==================================================\n")

    query = "PM Surya Ghar Muft Bijli Yojana eligibility criteria"
    print(f"Executing Query: '{query}'")
    search_res = serper_tool.search_government_portals(query, num_results=2)

    print(f"-> Success: {search_res['success']}")
    print(f"-> Total Results: {search_res['total_results']}")

    for idx, r in enumerate(search_res['results'], 1):
        print(f"   [{idx}] Title: {r['title']}")
        print(f"       Link: {r['link']}")
        print(f"       Snippet: {r['snippet']}\n")

    print("==================================================")
    print("[TEST] DAY 6: WEB SCRAPER & CONTENT CLEANER")
    print("==================================================\n")

    test_url = "https://www.myscheme.gov.in/"
    print(f"Scraping Clean Text from: '{test_url}'")
    scrape_res = web_scraper.scrape_clean_text(test_url, max_words=100)

    print(f"-> Success: {scrape_res['success']}")
    print(f"-> Page Title: {scrape_res['title']}")
    print(f"-> Word Count: {scrape_res['word_count']}")
    print(f"-> Clean Snippet:\n{scrape_res['clean_text'][:300]}...\n")

if __name__ == "__main__":
    test_serper_and_scraper()
