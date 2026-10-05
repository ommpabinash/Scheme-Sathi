import os
import glob
import re
import chromadb
from chromadb.utils import embedding_functions

from src.utils.config import settings
from src.tools.playwright_scraper import playwright_scraper

# List of major core myScheme URLs for automated Playwright scraping
TARGET_SCHEMES = [
    {"id": "Mukhyamantri Krishak Durghatna Kalyan Yojana", "url": "https://www.myscheme.gov.in/schemes/kdky"},
    {"id": "Uttar Pradesh Old Age Pension Scheme", "url": "https://www.myscheme.gov.in/schemes/upoaps"},
    {"id": "PM Kisan Samman Nidhi", "url": "https://www.myscheme.gov.in/schemes/pm-kisan"},
    {"id": "Pradhan Mantri Fasal Bima Yojana", "url": "https://www.myscheme.gov.in/schemes/pmfby"},
    {"id": "Ayushman Bharat PM-JAY Health Scheme", "url": "https://www.myscheme.gov.in/schemes/ab-pmjay"},
    {"id": "PM Surya Ghar Free Electricity Solar Scheme", "url": "https://www.myscheme.gov.in/schemes/pmsgmby"},
    {"id": "Kisan Credit Card (KCC) Scheme", "url": "https://www.myscheme.gov.in/schemes/kcc"},
]

def run_playwright_scraping_and_ingest():
    """
    Launches Playwright headless Chromium to scrape clean DOM sections for target myScheme URLs,
    saves clean text files, and ingests them into ChromaDB Vector Store.
    """
    print("[PLAYWRIGHT INGEST] Starting Playwright myScheme Web DOM Scraping...")

    processed_dir = settings.PROCESSED_DATA_DIR
    os.makedirs(processed_dir, exist_ok=True)

    scraped_documents = []

    for item in TARGET_SCHEMES:
        scheme_id = item["id"]
        url = item["url"]

        print(f"\n[PLAYWRIGHT INGEST] Scraping DOM for: {scheme_id} ({url})")
        dom_data = playwright_scraper.scrape_scheme_details(url)

        benefits_str = "\n".join([f"• {b}" for b in dom_data.get("benefits", [])])
        eligibility_str = dom_data.get("eligibility_text", "")
        docs_str = "\n".join([f"• {d}" for d in dom_data.get("docs", [])])
        process_str = "\n".join(dom_data.get("process_steps", []))

        full_doc_text = f"""
SCHEME TITLE: {scheme_id}
PORTAL URL: {url}

ELIGIBILITY CRITERIA:
{eligibility_str}

SCHEME BENEFITS:
{benefits_str}

DOCUMENTS REQUIRED:
{docs_str}

APPLICATION PROCESS:
{process_str}
""".strip()

        # Save clean text file
        safe_filename = re.sub(r'[^a-zA-Z0-9_-]', '_', scheme_id.lower()) + ".txt"
        file_path = os.path.join(processed_dir, safe_filename)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(full_doc_text)

        scraped_documents.append({
            "id": scheme_id,
            "filename": safe_filename,
            "text": full_doc_text,
            "url": url
        })

    # Ingest scraped documents + PDFs into ChromaDB
    print("\n[CHROMA INGEST] Initializing ChromaDB vectorstore...")
    os.makedirs(settings.CHROMA_PERSIST_DIR, exist_ok=True)
    chroma_client = chromadb.PersistentClient(path=settings.CHROMA_PERSIST_DIR)
    embedding_fn = embedding_functions.ONNXMiniLM_L6_V2()

    collection_name = "government_schemes"
    try:
        chroma_client.delete_collection(name=collection_name)
    except Exception:
        pass

    collection = chroma_client.create_collection(
        name=collection_name,
        embedding_function=embedding_fn,
        metadata={"hnsw:space": "cosine"}
    )

    chunk_ids = []
    chunk_texts = []
    chunk_metadatas = []
    total_chunks = 0

    def split_text_into_chunks(text, chunk_size=400, overlap=80):
        words = text.split()
        if len(words) <= chunk_size:
            return [text]
        chunks = []
        start = 0
        while start < len(words):
            end = start + chunk_size
            chunks.append(" ".join(words[start:end]))
            start += (chunk_size - overlap)
        return chunks

    for doc in scraped_documents:
        chunks = split_text_into_chunks(doc["text"])
        for idx, chunk_text in enumerate(chunks):
            total_chunks += 1
            chunk_id = f"{re.sub(r'[^a-zA-Z0-9_-]', '_', doc['id'].lower())}_chunk_{idx}"
            chunk_ids.append(chunk_id)
            chunk_texts.append(chunk_text)
            chunk_metadatas.append({
                "scheme_id": doc["id"],
                "filename": doc["filename"],
                "chunk_index": idx,
                "url": doc.get("url", "https://www.myscheme.gov.in")
            })

    # Batch insert into ChromaDB
    batch_size = 100
    for i in range(0, len(chunk_ids), batch_size):
        end_idx = i + batch_size
        collection.add(
            ids=chunk_ids[i:end_idx],
            documents=chunk_texts[i:end_idx],
            metadatas=chunk_metadatas[i:end_idx]
        )

    print(f"\n[SUCCESS] Ingested {len(scraped_documents)} Playwright-scraped myScheme documents ({total_chunks} chunks) into ChromaDB!")

if __name__ == "__main__":
    run_playwright_scraping_and_ingest()
