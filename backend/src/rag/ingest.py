import os
import glob
import re
from pypdf import PdfReader
import chromadb
from chromadb.utils import embedding_functions
from src.utils.config import settings

COLLECTION_NAME = "government_schemes"


def classify_scheme_category(text: str, filename: str = "") -> str:
    """Assign a broad category using the scheme title/filename and PDF text."""
    sample = f"{filename} {text}".lower().replace("_", " ").replace("-", " ")
    rules = [
        ("scholarship", [
            "scholarship", "post matric", "pre matric", "post-matric", "pre-matric",
            "student stipend", "education stipend", "tuition fee reimbursement",
            "national scholarship portal", "merit scholarship", "scholarship scheme",
            "financial assistance to students", "financial assistance for students",
            "student scholarship", "education grant"
        ]),
        ("agriculture", [
            "pm kisan", "pm-kisan", "kisan", "farmer", "farmers", "agriculture",
            "crop insurance", "fasal bima", "krishi", "agricultural", "kisan credit",
            "cultivator", "farming"
        ]),
        ("healthcare", [
            "ayushman bharat", "health insurance", "medical treatment", "healthcare",
            "hospitalisation", "hospitalization", "health scheme", "pm jay", "pm-jay"
        ]),
        ("energy", ["solar rooftop", "pm surya ghar", "solar subsidy", "renewable energy"]),
        ("housing", ["housing scheme", "awas yojana", "pmay", "pradhan mantri awas", "house construction"]),
        ("pension", ["old age pension", "widow pension", "disability pension", "pension scheme"]),
        ("employment", ["skill development", "employment scheme", "job training", "self employment", "livelihood mission"]),
        ("education", ["education scheme", "student", "school education", "higher education", "college student", "university student", "tuition fee"]),
    ]
    for category, keywords in rules:
        if any(keyword in sample for keyword in keywords):
            return category
    return "general"


def load_pdf_documents():
    """Parse PDFs in the configured raw_pdfs folder and retain useful metadata."""
    pdf_files = glob.glob(os.path.join(settings.RAW_PDFS_DIR, "*.pdf"))
    documents = []
    print(f"[LOAD] Found {len(pdf_files)} PDF files in '{settings.RAW_PDFS_DIR}'")

    for pdf_path in pdf_files:
        try:
            reader = PdfReader(pdf_path)
            pages = []
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    pages.append(text)
            full_text = "\n".join(pages).strip()
            filename = os.path.basename(pdf_path)
            scheme_id = os.path.splitext(filename)[0]

            if not full_text:
                print(f"[WARN] No extractable text in {filename}; OCR may be required.")
                continue

            category = classify_scheme_category(full_text, filename)
            documents.append({
                "id": scheme_id,
                "filename": filename,
                "text": full_text,
                "category": category,
            })
            print(f"[LOAD] {filename} -> category={category}")
        except Exception as exc:
            print(f"[ERROR] Error reading {pdf_path}: {exc}")

    return documents


def split_text_into_chunks(text, chunk_size=500, overlap=100):
    words = text.split()
    if not words:
        return []
    if len(words) <= chunk_size:
        return [text]
    chunks = []
    step = max(1, chunk_size - overlap)
    for start in range(0, len(words), step):
        chunk = " ".join(words[start:start + chunk_size])
        if chunk:
            chunks.append(chunk)
    return chunks


def ingest_documents_to_chroma():
    print("[START] Starting RAG Document Ingestion Pipeline...")
    docs = load_pdf_documents()
    if not docs:
        print("[ERROR] No readable text PDFs found. No collection was changed.")
        return

    os.makedirs(settings.CHROMA_PERSIST_DIR, exist_ok=True)
    client = chromadb.PersistentClient(path=settings.CHROMA_PERSIST_DIR)
    embedding_fn = embedding_functions.ONNXMiniLM_L6_V2()

    # Rebuild only after at least one readable PDF was found.
    try:
        client.delete_collection(name=COLLECTION_NAME)
    except Exception:
        pass

    collection = client.create_collection(
        name=COLLECTION_NAME,
        embedding_function=embedding_fn,
        metadata={"hnsw:space": "cosine"},
    )

    ids, texts, metadatas = [], [], []
    for doc in docs:
        for idx, chunk in enumerate(split_text_into_chunks(doc["text"])):
            ids.append(f"{doc['id']}_chunk_{idx}")
            texts.append(chunk)
            metadatas.append({
                "scheme_id": doc["id"],
                "filename": doc["filename"],
                "chunk_index": idx,
                "category": doc["category"],
            })

    print(f"[INDEXING] Indexing {len(texts)} chunks into '{COLLECTION_NAME}'...")
    batch_size = 100
    for start in range(0, len(ids), batch_size):
        end = start + batch_size
        collection.add(ids=ids[start:end], documents=texts[start:end], metadatas=metadatas[start:end])

    print(f"[SUCCESS] Ingested {len(docs)} PDFs / {len(texts)} chunks into {settings.CHROMA_PERSIST_DIR}")
    print("[SUMMARY] Category counts:")
    counts = {}
    for doc in docs:
        counts[doc["category"]] = counts.get(doc["category"], 0) + 1
    for category, count in sorted(counts.items()):
        print(f"  - {category}: {count} PDF(s)")


if __name__ == "__main__":
    ingest_documents_to_chroma()
