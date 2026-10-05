import re
from typing import Dict, Any, List
from playwright.sync_api import sync_playwright

class PlaywrightMySchemeScraper:
    """
    Playwright DOM Scraper for myScheme.gov.in.
    Launches headless Chromium to render Next.js SPA pages and extracts exact inner text
    from #benefits, #eligibility, #documents-required, and #application-process DOM elements.
    Clicks 'Offline' tab explicitly to extract both Online and Offline process steps.
    """

    def scrape_scheme_details(self, portal_url: str) -> Dict[str, Any]:
        """
        Navigates to a myScheme portal URL and extracts exact DOM sections.
        """
        if not portal_url or "myscheme.gov.in" not in portal_url:
            return {}

        clean_url = portal_url.strip().rstrip(";").rstrip(".").rstrip(",")
        print(f"[PLAYWRIGHT SCRAPER] Launching Chromium to scrape all tabs from: {clean_url}")

        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.goto(clean_url, wait_until="domcontentloaded", timeout=15000)

                # Wait for React elements to hydrate
                page.wait_for_timeout(2500)

                # 1. Benefits
                benefits_el = page.query_selector("#benefits") or page.query_selector("[id*='benefit']")
                raw_benefits = benefits_el.inner_text() if benefits_el else ""

                # 2. Eligibility
                eligibility_el = page.query_selector("#eligibility") or page.query_selector("[id*='eligib']")
                raw_eligibility = eligibility_el.inner_text() if eligibility_el else ""

                # 3. Documents Required
                docs_el = (
                    page.query_selector("#documents-required") or 
                    page.query_selector("#documents") or 
                    page.query_selector("[id*='docu']")
                )
                raw_docs = docs_el.inner_text() if docs_el else ""

                # 4. Application Process - Online Tab
                process_el = (
                    page.query_selector("#application-process") or 
                    page.query_selector("#process") or 
                    page.query_selector("[id*='process']")
                )
                raw_process_online = process_el.inner_text() if process_el else ""

                # Extract explicit hyperlinks inside process section
                extracted_links = []
                if process_el:
                    anchors = process_el.query_selector_all("a[href]")
                    for a in anchors:
                        href = a.get_attribute("href")
                        anchor_text = a.inner_text().strip()
                        if href and href.startswith("http"):
                            extracted_links.append((anchor_text or "official website", href))

                # 5. Application Process - Click Offline Tab
                raw_process_offline = ""
                try:
                    offline_tab = (
                        page.query_selector("span:has-text('Offline')") or 
                        page.query_selector("button:has-text('Offline')") or 
                        page.query_selector("div:has-text('Offline')")
                    )
                    if offline_tab:
                        offline_tab.click(force=True)
                        page.wait_for_timeout(1000)
                        process_el_off = (
                            page.query_selector("#application-process") or 
                            page.query_selector("#process") or 
                            page.query_selector("[id*='process']")
                        )
                        if process_el_off:
                            raw_process_offline = process_el_off.inner_text()
                except Exception as off_err:
                    print(f"[PLAYWRIGHT SCRAPER] Offline tab click note: {off_err}")

                browser.close()

                print(f"[PLAYWRIGHT SCRAPER] Successfully extracted DOM text (Benefits, Eligibility, Docs, Online & Offline Process)!")

                return {
                    "raw_benefits": raw_benefits,
                    "raw_eligibility": raw_eligibility,
                    "raw_docs": raw_docs,
                    "raw_process_online": raw_process_online,
                    "raw_process_offline": raw_process_offline,
                    "extracted_links": extracted_links
                }
        except Exception as e:
            print(f"[PLAYWRIGHT SCRAPER] Scrape exception: {e}")
            return {}

playwright_scraper = PlaywrightMySchemeScraper()
