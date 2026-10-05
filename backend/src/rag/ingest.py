import os
import glob
from pypdf import PdfReader
import chromadb
from chromadb.utils import embedding_functions
from src.utils.config import settings

def load_pdf_documents():
    """Parses all PDFs in the raw_pdfs folder and extracts text + metadata."""
    pdf_files = glob.glob(os.path.join(settings.RAW_PDFS_DIR, "*.pdf"))
    documents = []

    print(f"[LOAD] Found {len(pdf_files)} PDF files in '{settings.RAW_PDFS_DIR}'")

    for pdf_path in pdf_files:
        try:
            reader = PdfReader(pdf_path)
            full_text = ""
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    full_text += text + "\n"
            
            filename = os.path.basename(pdf_path)
            scheme_id = filename.replace(".pdf", "")

            if full_text.strip():
                documents.append({
                    "id": scheme_id,
                    "filename": filename,
                    "text": full_text.strip()
                })
        except Exception as e:
            print(f"[ERROR] Error reading {pdf_path}: {e}")

    return documents

def split_text_into_chunks(text, chunk_size=500, overlap=100):
    """Splits document text into overlapping semantic chunks."""
    words = text.split()
    chunks = []
    
    if len(words) <= chunk_size:
        return [text]

    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk_words = words[start:end]
        chunks.append(" ".join(chunk_words))
        start += (chunk_size - overlap)

    return chunks

def ingest_documents_to_chroma():
    """Processes PDF documents and persists embeddings into ChromaDB."""
    print("[START] Starting RAG Document Ingestion Pipeline...")
    
    # 1. Load PDFs
    docs = load_pdf_documents()
    if not docs:
        print("[ERROR] No PDF documents found to ingest!")
        return

    # 2. Initialize ChromaDB client with persistent storage
    os.makedirs(settings.CHROMA_PERSIST_DIR, exist_ok=True)
    chroma_client = chromadb.PersistentClient(path=settings.CHROMA_PERSIST_DIR)

    # 3. Use default lightweight sentence-transformer embedding function
    embedding_fn = embedding_functions.ONNXMiniLM_L6_V2()

    # 4. Create or reset Chroma collection
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

    # 5. Process and insert chunks
    total_chunks = 0
    chunk_ids = []
    chunk_texts = []
    chunk_metadatas = []

    for doc in docs:
        chunks = split_text_into_chunks(doc["text"])
        for idx, chunk_text in enumerate(chunks):
            total_chunks += 1
            chunk_id = f"{doc['id']}_chunk_{idx}"
            
            chunk_ids.append(chunk_id)
            chunk_texts.append(chunk_text)
            chunk_metadatas.append({
                "scheme_id": doc["id"],
                "filename": doc["filename"],
                "chunk_index": idx
            })

    # Batch insert into ChromaDB
    print(f"[INDEXING] Indexing {total_chunks} chunks into ChromaDB collection '{collection_name}'...")
    
    batch_size = 100
    for i in range(0, len(chunk_ids), batch_size):
        end_idx = i + batch_size
        collection.add(
            ids=chunk_ids[i:end_idx],
            documents=chunk_texts[i:end_idx],
            metadatas=chunk_metadatas[i:end_idx]
        )

    print(f"[SUCCESS] Ingested {len(docs)} documents ({total_chunks} chunks) into ChromaDB at:\n'{settings.CHROMA_PERSIST_DIR}'!")

if __name__ == "__main__":
    ingest_documents_to_chroma()
