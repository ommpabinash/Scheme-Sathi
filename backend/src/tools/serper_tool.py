import requests
import json
import re
from src.utils.config import settings

def clean_serper_url(url: str) -> str:
    """Sanitizes raw URLs returned by Serper search by stripping trailing semicolons or punctuation."""
    if not url:
        return ""
    # Strip trailing semicolons, dots, quotes, commas
    cleaned = url.strip().rstrip(";").rstrip(".").rstrip(",")
    return cleaned

class SerperSearchTool:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or settings.SERPER_API_KEY
        self.endpoint = "https://google.serper.dev/search"

    def search_government_portals(self, query: str, num_results: int = 5):
        """
        Executes a targeted Google Search via Serper API, strictly constraining results to the official myscheme.gov.in portal.
        """
        # Strictly restrict search exclusively to official myscheme.gov.in portal
        domain_restricted_query = f"{query} site:myscheme.gov.in"

        if not self.api_key or self.api_key == "your_serper_api_key_here":
            print("[SERPER TOOL] Warning: No active SERPER_API_KEY configured. Returning fallback web results for myscheme.gov.in.")
            return self._fallback_response(query)

        headers = {
            "X-API-KEY": self.api_key,
            "Content-Type": "application/json"
        }

        payload = {
            "q": domain_restricted_query,
            "num": num_results,
            "gl": "in"  # Geo-location India
        }

        try:
            response = requests.post(self.endpoint, headers=headers, json=payload, timeout=10)
            if response.status_code == 200:
                data = response.json()
                organic_results = data.get("organic", [])

                formatted_results = []
                for item in organic_results:
                    raw_link = item.get("link", "")
                    clean_link = clean_serper_url(raw_link)
                    raw_title = item.get("title", "")

                    # Filter out internal rules subdomains if main scheme URL exists
                    if "rules.myscheme.gov.in" in clean_link:
                        continue

                    # Filter out generic site title noise
                    if "Enter scheme name to search" in raw_title:
                        # Extract scheme slug from link
                        slug = clean_link.split("/")[-1].replace("-", " ").title()
                        raw_title = f"{slug} - myScheme"

                    formatted_results.append({
                        "title": raw_title,
                        "link": clean_link,
                        "snippet": item.get("snippet", ""),
                        "domain": "myscheme.gov.in"
                    })

                return {
                    "success": True,
                    "query": query,
                    "domain_query": domain_restricted_query,
                    "total_results": len(formatted_results),
                    "results": formatted_results
                }
            else:
                return {
                    "success": False,
                    "error": f"Serper API HTTP Error {response.status_code}: {response.text}",
                    "results": []
                }

        except Exception as e:
            return {
                "success": False,
                "error": f"Serper API Request Failed: {str(e)}",
                "results": []
            }

    def _fallback_response(self, query: str):
        """Fallback response when Serper API Key is not yet set."""
        return {
            "success": True,
            "query": query,
            "domain_query": f"{query} site:myscheme.gov.in",
            "is_fallback": True,
            "total_results": 2,
            "results": [
                {
                    "title": f"myScheme Portal Details - {query}",
                    "link": f"https://www.myscheme.gov.in/search?q={query}",
                    "snippet": f"Official myScheme portal details and eligibility criteria for {query}.",
                    "domain": "myscheme.gov.in"
                },
                {
                    "title": f"myScheme Official Search",
                    "link": "https://www.myscheme.gov.in/",
                    "snippet": "National Government Portal consolidating central and state government schemes.",
                    "domain": "myscheme.gov.in"
                }
            ]
        }

    def search_scheme_benefits(self, scheme_name: str):
        """
        Searches specifically for scheme benefits on myscheme.gov.in.
        Returns a list of benefit strings parsed from Google's cached snippet.
        """
        if not self.api_key or self.api_key == "your_serper_api_key_here":
            return []

        benefits_query = f'"{scheme_name}" benefits site:myscheme.gov.in'
        headers = {
            "X-API-KEY": self.api_key,
            "Content-Type": "application/json"
        }
        payload = {
            "q": benefits_query,
            "num": 3,
            "gl": "in"
        }

        try:
            response = requests.post(self.endpoint, headers=headers, json=payload, timeout=10)
            if response.status_code == 200:
                data = response.json()
                results = data.get("organic", [])
                
                # Collect all snippets from myscheme results
                all_snippets = []
                for item in results:
                    link = item.get("link", "")
                    if "myscheme.gov.in" in link and "rules." not in link:
                        snippet = item.get("snippet", "")
                        if snippet and len(snippet) > 20:
                            all_snippets.append(snippet)

                if not all_snippets:
                    return []

                # Parse benefit points from snippets
                benefits = []
                for snippet in all_snippets:
                    # Split on common separators used in myScheme snippets
                    # Snippets often contain multiple benefits separated by periods, semicolons, or numbered lists
                    parts = re.split(r'(?:\.\s+|\;\s*|\d+\)\s*|\d+\.\s+)', snippet)
                    for part in parts:
                        cleaned = part.strip().rstrip('.').strip()
                        # Filter out noise - keep only meaningful benefit statements
                        if len(cleaned) > 15 and len(cleaned) < 300:
                            # Skip if it contains eligibility or exclusion criteria instead of benefits
                            skip_signals = ["applicant should", "must be", "eligibility", "exclusion", "not eligible", "who can apply", "required document", "age limit", "income limit", "domicile", "resident of"]
                            if not any(sig in cleaned.lower() for sig in skip_signals):
                                benefits.append(cleaned)

                # Deduplicate while preserving order
                seen = set()
                unique_benefits = []
                for b in benefits:
                    b_lower = b.lower()
                    if b_lower not in seen:
                        seen.add(b_lower)
                        unique_benefits.append(b)

                return unique_benefits[:6]  # Cap at 6 benefits max
            return []
        except Exception as e:
            print(f"[SERPER TOOL] Benefits search failed: {e}")
            return []

    def search_scheme_eligibility(self, scheme_name: str) -> str:
        """
        Searches specifically for scheme eligibility criteria on myscheme.gov.in.
        Returns the exact live eligibility text snippet.
        """
        if not self.api_key or self.api_key == "your_serper_api_key_here":
            return ""

        eligibility_query = f'"{scheme_name}" eligibility site:myscheme.gov.in'
        headers = {
            "X-API-KEY": self.api_key,
            "Content-Type": "application/json"
        }
        payload = {
            "q": eligibility_query,
            "num": 3,
            "gl": "in"
        }

        try:
            response = requests.post(self.endpoint, headers=headers, json=payload, timeout=10)
            if response.status_code == 200:
                data = response.json()
                results = data.get("organic", [])
                snippets = []
                for item in results:
                    snippet = item.get("snippet", "")
                    if snippet and len(snippet) > 20:
                        snippets.append(snippet)
                if snippets:
                    return " ".join(snippets[:2])
            return ""
        except Exception as e:
            print(f"[SERPER TOOL] Eligibility search failed: {e}")
            return ""

# Instantiated helper instance
serper_tool = SerperSearchTool()
