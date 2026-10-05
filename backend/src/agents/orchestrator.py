from typing import List, Dict, Any
from src.agents.state import AgentState, ConversationTurn
from src.agents.profile_agent import profile_agent
from src.agents.rag_agent import rag_agent
from src.agents.router_agent import router_agent
from src.agents.web_agent import web_agent
from src.agents.eligibility import eligibility_agent
from src.agents.counselor import counselor_agent


class MultiAgentOrchestrator:
    """
    Day 14: Unified Multi-Agent Orchestration Pipeline.
    Now supports conversation_history for multi-turn context continuity.
    Pipeline: Profile -> RAG -> Router -> [Serper Web] -> Adjudicator -> Counselor
    """

    def run(self, user_query: str, conversation_history: List[Dict[str, Any]] = None) -> AgentState:
        # 1. Reconstruct typed history from raw dicts
        typed_history = []
        if conversation_history:
            for turn in conversation_history:
                try:
                    typed_history.append(ConversationTurn(**turn))
                except Exception:
                    pass  # Skip malformed turns

        # 2. Initialize State with history
        state = AgentState(
            user_query=user_query,
            conversation_history=typed_history,
        )

        # 3. Profile Extraction + Intent Detection (uses conversation history)
        state = profile_agent.process(state)
        if state.clarification_needed:
            state.final_output = {
                "clarification_needed": True,
                "prompt": state.clarification_prompt,
                "missing_fields": state.user_profile.missing_fields,
            }
            return state

        # If listing all schemes or providing application steps, go straight to counselor
        if state.intent in ("list_schemes", "apply_info"):
            state = counselor_agent.process(state)
            return state

        # 4. Local RAG Retrieval
        state = rag_agent.process(state)

        # 5. Similarity Routing (threshold >= 0.70)
        state = router_agent.process(state)

        # 6. Fallback Serper Web Search if RAG confidence is low
        if state.retrieval_mode == "web_search":
            state = web_agent.process(state)

        # 7. Eligibility Adjudication
        state = eligibility_agent.process(state)

        # 8. Counselor Summary, Checklist & Citations
        state = counselor_agent.process(state)

        return state


orchestrator = MultiAgentOrchestrator()
