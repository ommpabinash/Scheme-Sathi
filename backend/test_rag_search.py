import sys
import os

# Add backend directory to sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

from src.tools.vector_tool import vector_tool

def test_queries():
    sample_queries = [
        "I am a 45 year old farmer from UP with income under 1 lakh, what scheme can help me?",
        "Health insurance cover for senior citizens aged 70 years and above",
        "Education loan without collateral for college student",
        "Free electricity solar rooftop scheme PM Surya Ghar",
        "Monthly pension for unorganized street vendors and workers"
    ]

    print("==================================================")
    print("🔎 TESTING CHROMADB VECTOR SEARCH & RETRIEVAL")
    print("==================================================\n")

    for idx, q in enumerate(sample_queries, 1):
        print(f"Query {idx}: '{q}'")
        res = vector_tool.search_schemes(q, top_k=2)
        
        print(f"-> Max Cosine Similarity Score: {res['max_similarity_score']}")
        print(f"-> Passed Similarity Threshold (>= 0.70): {res['threshold_passed']}")
        
        for r_idx, match in enumerate(res['results'], 1):
            print(f"   Match {r_idx}: [{match['scheme_id']}] (Score: {match['similarity_score']})")
            snippet = match['content'][:150].replace("\n", " ")
            print(f"   Snippet: {snippet}...\n")
        print("-" * 50)

if __name__ == "__main__":
    test_queries()
