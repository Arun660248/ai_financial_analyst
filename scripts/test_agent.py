import os
import sys

# Ensure backend directory is in the Python path so data_fetcher can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

from dotenv import load_dotenv

# Load env variables from root directory if running from scripts/ or root
load_dotenv(dotenv_path=os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env")))

try:
    from data_fetcher import agent_executor
except ImportError as e:
    print(f"Error importing agent_executor: {e}")
    sys.exit(1)

def run_test_query(query: str):
    print("=" * 60)
    print(f"Executing query: '{query}'")
    print("=" * 60)
    try:
        result = agent_executor.invoke({"messages": [("user", query)]})
        response = result["messages"][-1].content
        print("\n--- AGENT RESPONSE ---")
        print(response)
        print("\n--- GENERATED CHARTS ---")
        static_chart = os.path.join(os.path.dirname(__file__), "..", "backend", "static", "financial_chart.png")
        if os.path.exists(static_chart):
            print(f"[SUCCESS] Financial chart generated successfully: {static_chart}")
        else:
            print("[INFO] No chart was generated for this query.")
    except Exception as e:
        print(f"[ERROR] Execution failed: {e}")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    # Check if Google API Key is set
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("[WARNING] GOOGLE_API_KEY is not set in environment or .env file.")
        print("Please configure your .env file in the root directory before running.")
        sys.exit(1)
        
    test_query = "Can you plot the financial trends for Microsoft (MSFT)?"
    run_test_query(test_query)
