import sys
import os
from fastapi.testclient import TestClient

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

from src.api.main import app

client = TestClient(app)

def test_api_endpoints():
    print("==================================================")
    print("[TEST] PHASE 4: FASTAPI REST API SERVER ENDPOINTS")
    print("==================================================\n")

    # 1. Health Check Endpoint
    print("1. Testing GET /api/health...")
    r1 = client.get("/api/health")
    print(f"-> Status: {r1.status_code}")
    print(f"-> Output: {r1.json()}\n")

    # 2. All Schemes Endpoint
    print("2. Testing GET /api/schemes...")
    r2 = client.get("/api/schemes")
    print(f"-> Status: {r2.status_code}")
    print(f"-> Total Pre-indexed Schemes: {r2.json().get('total_schemes')}\n")

    # 3. Chat Endpoint (Local RAG query)
    print("3. Testing POST /api/chat...")
    payload = {
        "query": "I am a 45 year old farmer from UP with income 80,000 per year",
        "target_language": "hi"
    }
    r3 = client.post("/api/chat", json=payload)
    print(f"-> Status: {r3.status_code}")
    data = r3.json()
    print(f"-> API Status: {data.get('status')}")
    if data.get("response"):
        resp = data["response"]
        print(f"   Top Scheme Matched: {resp.get('top_scheme')}")
        print(f"   Match Score: {resp.get('match_score')}%")
        print(f"   Retrieval Mode: {resp.get('retrieval_mode')}")
        print(f"   Summary: {resp.get('summary')}")
        print(f"   Document Checklist: {resp.get('document_checklist')[:2]}")
    print("\n")

    # 4. Text-to-Speech Endpoint
    print("4. Testing POST /api/text-to-speech...")
    r4 = client.post("/api/text-to-speech", json={"text": "Hello, testing text to speech conversion", "language": "en"})
    print(f"-> Status: {r4.status_code}")
    print(f"-> Media Content Type: {r4.headers.get('content-type')}\n")

if __name__ == "__main__":
    test_api_endpoints()
