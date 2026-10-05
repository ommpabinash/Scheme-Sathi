import sys
import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

from src.agents.orchestrator import orchestrator

def test_multi_agent_pipeline():
    test_queries = [
        "I am a 45 year old farmer from UP with income of 80000 rupees per year",
        "Senior citizen health insurance for age 72 years",
        "Tell me about the brand new solar rooftop scheme PM Surya Ghar"
    ]

    print("==================================================")
    print("[TEST] PHASE 2: MULTI-AGENT PIPELINE TEST")
    print("==================================================\n")

    for idx, q in enumerate(test_queries, 1):
        print(f"--- QUERY {idx}: '{q}' ---")
        state = orchestrator.run(q)

        output = state.final_output
        print(f"-> Clarification Needed: {output.get('clarification_needed', False)}")
        if output.get('clarification_needed'):
            print(f"   Prompt: {output.get('prompt')}\n")
            continue

        print(f"-> Retrieval Mode Used: {output.get('retrieval_mode')}")
        print(f"-> Top Scheme: {output.get('top_scheme')}")
        print(f"-> Match Score: {output.get('match_score')}% (Eligible: {output.get('is_eligible')})")
        print(f"-> Summary: {output.get('summary')}")
        print(f"-> Matched Criteria: {output.get('matched_criteria')}")
        print(f"-> Document Checklist: {output.get('document_checklist')[:2]}...")
        print(f"-> Citations: {output.get('citations')}\n")

if __name__ == "__main__":
    test_multi_agent_pipeline()
