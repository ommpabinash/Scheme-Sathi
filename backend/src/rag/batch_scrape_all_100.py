import os
import glob
import re
import chromadb
from chromadb.utils import embedding_functions
from pypdf import PdfReader

from src.utils.config import settings
from src.tools.playwright_scraper import playwright_scraper
from src.tools.serper_tool import serper_tool

def clean_scheme_name_from_filename(filename: str) -> str:
    """Converts a pdf filename like 'pm_kisan_samman_nidhi.pdf' to 'PM Kisan Samman Nidhi'."""
    name = filename.replace(".pdf", "").replace("_", " ").title()
    name = re.sub(r'\bPm\b', 'PM', name)
    name = re.sub(r'\bUp\b', 'UP', name)
    name = re.sub(r'\bMh\b', 'MH', name)
    name = re.sub(r'\bMp\b', 'MP', name)
    name = re.sub(r'\bWb\b', 'WB', name)
    name = re.sub(r'\bKcc\b', 'KCC', name)
    name = re.sub(r'\bTb\b', 'TB', name)
    name = re.sub(r'\bPmjay\b', 'PM-JAY', name)
    return name

def run_batch_scrape_and_ingest():
    """
    Batch Playwright scraper for all 100+ PDF schemes in data/raw_pdfs.
    Extracts clean myScheme DOM text and persists into ChromaDB Vector Store.
    """
    pdf_files = glob.glob(os.path.join(settings.RAW_PDFS_DIR, "*.pdf"))
    print(f"[BATCH SCRAPE] Found {len(pdf_files)} PDF files in '{settings.RAW_PDFS_DIR}'")

    processed_dir = settings.PROCESSED_DATA_DIR
    os.makedirs(processed_dir, exist_ok=True)

    all_scraped_docs = []

    # Map of known slugs for fast direct Playwright navigation
    KNOWN_SLUGS = {
        "kisan_credit_card": "https://www.myscheme.gov.in/schemes/kcc",
        "pm_kisan_samman_nidhi": "https://www.myscheme.gov.in/schemes/pm-kisan",
        "pradhan_mantri_fasal_bima": "https://www.myscheme.gov.in/schemes/pmfby",
        "ayushman_bharat_pmjay": "https://www.myscheme.gov.in/schemes/ab-pmjay",
        "pm_surya_ghar": "https://www.myscheme.gov.in/schemes/pmsgmby",
        "nsap_old_age_pension": "https://www.myscheme.gov.in/schemes/upoaps",
    }

    for idx, pdf_path in enumerate(pdf_files, 1):
        filename = os.path.basename(pdf_path)
        base_key = filename.replace(".pdf", "").lower()
        scheme_title = clean_scheme_name_from_filename(filename)

        print(f"\n[{idx}/{len(pdf_files)}] Processing: {scheme_title} ({filename})")

        # 1. Determine myScheme target URL
        portal_url = None
        for k, url in KNOWN_SLUGS.items():
            if k in base_key:
                portal_url = url
                break

        if not portal_url:
            # Fallback to Serper search for myScheme portal URL
            search_query = f'"{scheme_title}" site:myscheme.gov.in/schemes'
            res = serper_tool.search_government_portals(search_query)
            if isinstance(res, dict) and res.get("results"):
                for r in res["results"]:
                    link = r.get("link", "")
                    if "myscheme.gov.in/schemes/" in link:
                        portal_url = link
                        break

        # 2. Extract DOM via Playwright if portal_url found
        dom_data = {}
        if portal_url:
            print(f"  -> Scraping Playwright Chromium DOM from: {portal_url}")
            dom_data = playwright_scraper.scrape_scheme_details(portal_url)

        # 3. Read raw PDF text as fallback/supplement
        pdf_text = ""
        try:
            reader = PdfReader(pdf_path)
            for page in reader.pages:
                t = page.extract_text()
                if t: pdf_text += t + "\n"
        except Exception:
            pass

        # Combine Playwright DOM text + PDF text
        benefits_str = "\n".join([f"• {b}" for b in dom_data.get("benefits", [])])
        eligibility_str = dom_data.get("eligibility_text", "")
        docs_str = "\n".join([f"• {d}" for d in dom_data.get("docs", [])])
        process_str = "\n".join(dom_data.get("process_steps", []))

        full_doc_text = f"""
SCHEME TITLE: {scheme_title}
PORTAL URL: {portal_url or 'https://www.myscheme.gov.in'}

ELIGIBILITY CRITERIA:
{eligibility_str if eligibility_str else pdf_text[:800]}

SCHEME BENEFITS:
{benefits_str if benefits_str else pdf_text[800:1600]}

DOCUMENTS REQUIRED:
{docs_str if docs_str else '• Aadhaar Card\n• Bank Passbook\n• Domicile Proof'}

APPLICATION PROCESS:
{process_str if process_str else 'Visit official website www.myscheme.gov.in to apply.'}

FULL POLICY SUMMARY:
{pdf_text}
""".strip()

        safe_txt_filename = base_key + ".txt"
        save_path = os.path.join(processed_dir, safe_txt_filename)
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(full_doc_text)

        all_scraped_docs.append({
            "id": scheme_title,
            "filename": safe_txt_filename,
            "text": full_doc_text,
            "url": portal_url or "https://www.myscheme.gov.in"
        })

    # Ingest ALL 100+ documents into ChromaDB Vector Store
    print(f"\n[CHROMA INGEST] Initializing ChromaDB vectorstore for ALL {len(all_scraped_docs)} schemes...")
    os.makedirs(settings.CHROMA_PERSIST_DIR, exist_ok=True)
    chroma_client = chromadb.PersistentClient(path=settings.CHROMA_PERSIST_DIR)
    embedding_fn = embedding_functions.DefaultEmbeddingFunction()

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

    for doc in all_scraped_docs:
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

    print(f"\n[SUCCESS] Ingested ALL {len(all_scraped_docs)} scheme documents ({total_chunks} chunks) into ChromaDB at:\n'{settings.CHROMA_PERSIST_DIR}'!")

if __name__ == "__main__":
    run_batch_scrape_and_ingest()
