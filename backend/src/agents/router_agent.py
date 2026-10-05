from src.agents.state import AgentState
from src.utils.config import settings

class RouterAgent:
    """
    Day 9: Router Agent.
    Evaluates RAG similarity scores against settings.COSINE_SIMILARITY_THRESHOLD (0.70).
    Decides whether to route to Local RAG or Serper API Web Search.
    """

    def process(self, state: AgentState) -> AgentState:
        # Check similarity score from previous RAG retrieval attempt if available
        score = state.max_similarity_score
        threshold = settings.COSINE_SIMILARITY_THRESHOLD

        if score >= threshold:
            state.retrieval_mode = "rag"
            print(f"[ROUTER AGENT] RAG similarity score {score} >= {threshold}. Routing to Local RAG Engine.")
        else:
            state.retrieval_mode = "web_search"
            print(f"[ROUTER AGENT] RAG similarity score {score} < {threshold}. Routing to Serper Web Search Agent.")

        return state

router_agent = RouterAgent()
