from src.agents.state import AgentState
from src.tools.serper_tool import serper_tool
from src.utils.translator import translator, safe_print

class SerperWebSearchAgent:
    """
    Serper API Web Search Agent.
    Triggers live Google Searches strictly on myscheme.gov.in domain when RAG confidence is low.
    Translates non-English queries to English before searching to avoid irrelevant results.
    """

    def _translate_query_to_english(self, query: str) -> str:
        """
        If query is in a regional language, translate it to English first.
        Serper/Google returns better scheme results for English queries on myscheme.gov.in.
        """
        try:
            translated = translator.translate_text(query, target_lang="en")
            # If translation returned same text, it was already English
            if translated and translated.strip() != query.strip():
                safe_print(f"[WEB AGENT] Translated query: '{translated[:80]}'")
                return translated
        except Exception:
            pass
        return query

    def process(self, state: AgentState) -> AgentState:
        query = state.user_query

        # Translate to English for better myscheme.gov.in search results
        english_query = self._translate_query_to_english(query)
        safe_print(f"[WEB AGENT] Executing Serper search on myscheme.gov.in for query: '{english_query[:80]}'")

        res = serper_tool.search_government_portals(english_query, num_results=3)

        if res["success"]:
            state.web_search_results = res["results"]
        else:
            state.web_search_results = []

        return state

web_agent = SerperWebSearchAgent()
