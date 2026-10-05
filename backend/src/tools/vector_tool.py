import os
import chromadb
from chromadb.utils import embedding_functions
from src.utils.config import settings

class VectorStoreTool:
    def __init__(self, collection_name="government_schemes"):
        self.collection_name = collection_name
        self.chroma_client = chromadb.PersistentClient(path=settings.CHROMA_PERSIST_DIR)
        self.embedding_fn = embedding_functions.ONNXMiniLM_L6_V2()
        
        try:
            self.collection = self.chroma_client.get_collection(
                name=collection_name,
                embedding_function=self.embedding_fn
            )
        except Exception:
            self.collection = None

    def _get_collection(self):
        if not self.collection:
            try:
                self.collection = self.chroma_client.get_collection(
                    name=self.collection_name,
                    embedding_function=self.embedding_fn
                )
            except Exception:
                self.collection = None
        return self.collection

    def search_schemes(self, query: str, top_k: int = 4):
        """
        Queries ChromaDB vector database and returns matching document chunks with similarity scores.
        Cosine similarity score S = 1 - distance.
        """
        collection = self._get_collection()
        if not collection:
            return {
                "success": False,
                "error": "Vector database collection not found. Please run ingestion first.",
                "results": [],
                "max_similarity_score": 0.0
            }

        try:
            results = collection.query(
                query_texts=[query],
                n_results=top_k,
                include=["documents", "metadatas", "distances"]
            )

            retrieved_chunks = []
            max_score = 0.0

            if results and results["documents"] and len(results["documents"][0]) > 0:
                docs = results["documents"][0]
                metas = results["metadatas"][0]
                distances = results["distances"][0]

                for doc, meta, dist in zip(docs, metas, distances):
                    # For cosine distance, similarity_score = 1.0 - distance
                    similarity_score = max(0.0, min(1.0, 1.0 - dist))
                    if similarity_score > max_score:
                        max_score = similarity_score

                    retrieved_chunks.append({
                        "content": doc,
                        "scheme_id": meta.get("scheme_id", "unknown"),
                        "filename": meta.get("filename", ""),
                        "similarity_score": round(similarity_score, 4),
                        "distance": round(dist, 4)
                    })

            return {
                "success": True,
                "query": query,
                "max_similarity_score": round(max_score, 4),
                "threshold_passed": max_score >= settings.COSINE_SIMILARITY_THRESHOLD,
                "results": retrieved_chunks
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "results": [],
                "max_similarity_score": 0.0
            }

# Instantiated helper instance
vector_tool = VectorStoreTool()
