from src.agents.state import AgentState
from src.tools.vector_tool import vector_tool

class RAGRetrievalAgent:
    """
    Day 10: Local RAG Retrieval Agent.
    Queries ChromaDB vector database and attaches top-K ground-truth scheme context.
    """

    def process(self, state: AgentState) -> AgentState:
        query = state.user_query
        
        # Translate to English if query is in a regional language
        search_query = query
        try:
            from src.utils.translator import translator, safe_print
            translated = translator.translate_text(query, target_lang="en")
            if translated and translated.strip().lower() != query.strip().lower():
                safe_print(f"[RAG AGENT] Translated query for DB search: '{translated}'")
                search_query = translated
        except Exception as e:
            from src.utils.translator import safe_print
            safe_print(f"[RAG AGENT] Translation error: {e}")

        res = vector_tool.search_schemes(search_query, top_k=4)

        if res["success"]:
            state.retrieved_chunks = res["results"]
            state.max_similarity_score = res["max_similarity_score"]
        else:
            state.retrieved_chunks = []
            state.max_similarity_score = 0.0

        return state

rag_agent = RAGRetrievalAgent()
