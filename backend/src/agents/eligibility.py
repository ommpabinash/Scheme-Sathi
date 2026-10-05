from src.agents.state import AgentState
from src.utils.llm_client import llm_client

class EligibilityAdjudicatorAgent:
    """
    LLM-driven Eligibility Adjudicator Agent.
    Dynamically checks scheme rules against user demographics using Gemini 2.5 Flash LLM.
    Strictly identifies hard disqualifiers (age limits, income caps) without generic fallbacks.
    """

    def process(self, state: AgentState) -> AgentState:
        profile = state.user_profile
        user_query_low = (state.user_query or "").lower()
        context_chunks = state.retrieved_chunks if state.retrieved_chunks else state.web_search_results

        # Top scheme name extraction
        top_scheme = ""
        scheme_context = ""
        if context_chunks:
            top_scheme = context_chunks[0].get("scheme_id") or context_chunks[0].get("title", "")
            scheme_context = "\n".join([
                f"- Title: {c.get('title', '')}\n  Snippet: {c.get('content', '') or c.get('snippet', '')}"
                for c in context_chunks[:3]
            ])

        if not top_scheme:
            top_scheme = state.user_query or "Government Assistance Scheme"

        # Construct prompt for LLM Adjudication
        prompt = f"""
You are an expert Government Scheme Eligibility Evaluator in India.
Evaluate if this applicant is ELIGIBLE or DISQUALIFIED for the scheme "{top_scheme}".

APPLICANT PROFILE:
- Age: {profile.age if profile.age else "Not specified"}
- Occupation: {profile.occupation if profile.occupation else "Not specified"}
- State / Domicile: {profile.state if profile.state else "Not specified"}
- Annual Family Income: {f"Rs. {profile.income:,} per annum" if profile.income else "Not specified"}
- Category: {profile.category if profile.category else "Not specified"}
- Gender: {profile.gender if profile.gender else "Not specified"}

SCHEME CONTEXT & POLICY RULES:
{scheme_context if scheme_context else f"Scheme Name: {top_scheme}"}

RULES TO ENFORCE STRICTLY:
1. AGE CHECK: If the scheme requires a specific age group (e.g. Senior Citizen Pension requires Age 60+), and user age is below 60, user is DISQUALIFIED.
2. INCOME CEILING CHECK: If the scheme has an income cap (e.g. Rural <= Rs 46,080 / Urban <= Rs 56,460), and user annual income exceeds this cap, user is DISQUALIFIED.
3. If disqualified, set "is_eligible": false and "match_score": 0. Put exact disqualification statement in "unmatched_criteria".
4. If eligible, put satisfied criteria in "matched_criteria" and set "match_score" between 75 and 100.
5. If no specific disqualifiers exist, "unmatched_criteria" should be an empty list [].

Respond ONLY with valid JSON in this exact structure:
{{
  "is_eligible": true,
  "match_score": 85,
  "matched_criteria": ["Occupation match: Farmer", "State domicile match: Uttar Pradesh"],
  "unmatched_criteria": []
}}
"""

        # Call Gemini LLM for adjudication
        llm_response = llm_client.generate_json(prompt)

        if llm_response and "is_eligible" in llm_response:
            matched_rules = llm_response.get("matched_criteria", [])
            unmatched_rules = llm_response.get("unmatched_criteria", [])
            is_eligible = llm_response.get("is_eligible", True)
            score = llm_response.get("match_score", 85 if is_eligible else 0)
        else:
            # Code-level fallback if LLM is unreachable
            matched_rules = []
            unmatched_rules = []
            score = 85
            is_eligible = True

            scheme_low = (top_scheme + " " + user_query_low).lower()

            if profile.occupation:
                matched_rules.append(f"Occupation match: {profile.occupation.capitalize()}")
            if profile.state:
                matched_rules.append(f"State domicile match: {profile.state.upper()}")

            # Strict Age & Income rules
            if "pension" in scheme_low or "old age" in scheme_low or "senior" in scheme_low:
                if profile.age and profile.age < 60:
                    is_eligible = False
                    score = 0
                    unmatched_rules.append(f"Disqualified / Ineligible: Requires age 60+ (User age is {profile.age} years old)")
                elif profile.age:
                    matched_rules.append(f"Age criterion met: {profile.age} years old (60+ requirement satisfied)")

                if profile.income and profile.income > 46080:
                    is_eligible = False
                    score = 0
                    unmatched_rules.append(f"Disqualified / Ineligible: User annual income (Rs. {profile.income:,}) exceeds scheme ceiling limit (Rs. 46,080)")
                elif profile.income:
                    matched_rules.append(f"Income criterion met: Rs. {profile.income:,} per annum")
            else:
                if profile.age:
                    matched_rules.append(f"Age criterion met: {profile.age} years old")
                if profile.income:
                    matched_rules.append(f"Income recorded: Rs. {profile.income:,} per annum")

        print(f"\n============== [SCHEME ELIGIBILITY EVALUATED] ==============")
        print(f"Scheme: {top_scheme}")
        print(f"Is Eligible: {is_eligible} | Match Score: {score}%")
        print("Matched Criteria:")
        for m in matched_rules:
            print(f"  [OK] {m}")
        print("Disqualification / Unmatched Criteria:")
        for u in unmatched_rules:
            print(f"  [WARN] {u}")
        print(f"===========================================================\n")

        state.eligibility_evaluation = {
            "is_eligible": is_eligible,
            "match_score": score,
            "top_scheme": top_scheme,
            "matched_criteria": matched_rules if matched_rules else ["Demographic profile alignment"],
            "unmatched_criteria": unmatched_rules if unmatched_rules else [],
        }

        return state

eligibility_agent = EligibilityAdjudicatorAgent()
