import chromadb
from chromadb.utils import embedding_functions
from src.utils.config import settings


def _normalize_category(value):
    """Normalize category labels shared by ingestion and counselor."""
    if not value:
        return None
    value = str(value).strip().lower().replace("-", "_").replace(" ", "_")
    aliases = {
        "scholarship": "education",
        "student": "education",
        "education_and_scholarship": "education",
        "farm": "agriculture",
        "farmer": "agriculture",
        "agri": "agriculture",
        "healthcare": "health",
        "medical": "health",
        "housing": "housing",
        "pension": "pension",
        "employment": "employment",
        "solar": "energy",
    }
    return aliases.get(value, value)


def _query_category(query):
    """Detect an explicit topic in the current user query."""
    text = (query or "").lower()
    groups = {
        "education": (
            "scholarship", "scholarships", "student", "students", "education",
            "school", "college", "tuition", "fellowship", "post matric",
            "post-matric", "pre matric", "pre-matric", "stipend",
        ),
        "agriculture": (
            "farmer", "farmers", "agriculture", "agricultural", "kisan",
            "krishi", "crop", "fasal", "farming", "pm-kisan", "pm kisan",
        ),
        "health": ("health", "healthcare", "hospital", "medical", "treatment", "ayushman"),
        "housing": ("housing", "house construction", "awas", "pmay"),
        "energy": ("solar", "electricity", "surya ghar"),
        "pension": ("pension", "senior citizen", "old age"),
        "employment": ("employment", "job", "livelihood", "skill development"),
        "women": ("women", "woman", "girl child", "mahila", "maternity"),
    }
    for category, terms in groups.items():
        if any(term in text for term in terms):
            return category
    return None


class VectorStoreTool:
    def __init__(self, collection_name="government_schemes"):
        self.collection_name = collection_name
        self.chroma_client = chromadb.PersistentClient(path=settings.CHROMA_PERSIST_DIR)
        self.embedding_fn = embedding_functions.ONNXMiniLM_L6_V2()
        self.collection = None
        self._get_collection()

    def _get_collection(self):
        if self.collection is None:
            try:
                self.collection = self.chroma_client.get_collection(
                    name=self.collection_name,
                    embedding_function=self.embedding_fn,
                )
            except Exception:
                self.collection = None
        return self.collection

    def search_schemes(self, query: str, top_k: int = 4):
        collection = self._get_collection()
        if collection is None:
            return {
                "success": False,
                "error": "Vector database collection not found. Run ingestion first.",
                "results": [],
                "max_similarity_score": 0.0,
            }

        try:
            requested_category = _query_category(query)
            # Retrieve more candidates than the final top_k. This gives the
            # caller a chance to find relevant education chunks when they are
            # not among the four nearest chunks globally.
            candidate_k = min(max(top_k * 8, 24), collection.count())
            if candidate_k < 1:
                return {
                    "success": True,
                    "query": query,
                    "results": [],
                    "max_similarity_score": 0.0,
                    "threshold_passed": False,
                }

            raw = collection.query(
                query_texts=[query],
                n_results=candidate_k,
                include=["documents", "metadatas", "distances"],
            )

            docs = (raw.get("documents") or [[]])[0]
            metas = (raw.get("metadatas") or [[]])[0]
            distances = (raw.get("distances") or [[]])[0]

            candidates = []
            for doc, meta, dist in zip(docs, metas, distances):
                meta = meta or {}
                scheme_id = str(meta.get("scheme_id", "unknown"))
                filename = str(meta.get("filename", ""))
                category = _normalize_category(meta.get("category"))
                similarity = max(0.0, min(1.0, 1.0 - float(dist)))

                candidates.append({
                    "content": doc or "",
                    "scheme_id": scheme_id,
                    "filename": filename,
                    "category": category,
                    "metadata": dict(meta),
                    "similarity_score": round(similarity, 4),
                    "distance": round(float(dist), 4),
                })

            # When metadata says this is a category-specific request, prioritize
            # matching category chunks. If no matching metadata is present (e.g.
            # an older index), do not silently relabel unrelated results.
            if requested_category:
                matching = [
                    item for item in candidates
                    if item.get("category") == requested_category
                ]
                # For older indexes without category metadata, return the broader
                # candidates with metadata intact; counselor-side text filtering
                # can classify them. Never invent a category for them here.
                if matching:
                    candidates = matching

            candidates.sort(
                key=lambda item: item.get("similarity_score", 0.0),
                reverse=True,
            )
            final_results = candidates[:top_k]
            max_score = max(
                (item["similarity_score"] for item in final_results),
                default=0.0,
            )
            return {
                "success": True,
                "query": query,
                "requested_category": requested_category,
                "max_similarity_score": round(max_score, 4),
                "threshold_passed": max_score >= settings.COSINE_SIMILARITY_THRESHOLD,
                "results": final_results,
            }
        except Exception as exc:
            return {
                "success": False,
                "error": str(exc),
                "results": [],
                "max_similarity_score": 0.0,
            }


vector_tool = VectorStoreTool()
