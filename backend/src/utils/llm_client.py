import requests
import json
import time
from src.utils.config import settings

class LLMClient:
    """
    Client for calling Gemini 2.5 Flash API for dynamic LLM eligibility checking,
    disqualification adjudication, and benefit/document extraction.
    Includes timeout protection (25s) and automatic 2-attempt retry logic.
    """
    def __init__(self, api_key: str = None):
        self.api_key = api_key or settings.GEMINI_API_KEY
        self.model = "gemini-2.5-flash"
        self.endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"

    def generate_json(self, prompt: str, max_retries: int = 2) -> dict:
        """Call Gemini API and request clean JSON output with retry logic."""
        if not self.api_key:
            return {}

        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }],
            "generationConfig": {
                "responseMimeType": "application/json",
                "temperature": 0.1
            }
        }

        for attempt in range(1, max_retries + 1):
            try:
                r = requests.post(self.endpoint, json=payload, timeout=25)
                if r.status_code == 200:
                    res_data = r.json()
                    candidates = res_data.get('candidates', [])
                    if candidates and 'content' in candidates[0]:
                        parts = candidates[0]['content'].get('parts', [])
                        if parts and 'text' in parts[0]:
                            return json.loads(parts[0]['text'])
                else:
                    print(f"[LLM CLIENT] Attempt {attempt} HTTP Error {r.status_code}: {r.text[:200]}")
            except (requests.exceptions.Timeout, requests.exceptions.RequestException) as e:
                print(f"[LLM CLIENT] Attempt {attempt} failed: {e}")
                if attempt < max_retries:
                    time.sleep(1)
            except Exception as e:
                print(f"[LLM CLIENT] Unexpected exception on attempt {attempt}: {e}")
                break

        print("[LLM CLIENT] All retries exhausted. Falling back to local rules.")
        return {}

llm_client = LLMClient()
