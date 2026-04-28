import sys
import os
from dotenv import load_dotenv

# Ensure we can import from MVP folder
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'MVP')))

# Explicitly load the MVP .env variables for the agent before it attempts to import
env_path = os.path.join(os.path.dirname(__file__), '..', 'MVP', '.env')
if os.path.exists(env_path):
    load_dotenv(dotenv_path=env_path)
else:
    load_dotenv()

from agents.idea_agent import extract_startup_details

def test_idea_extraction():
    sample_idea = "We are building an AI-powered platform for farmers to predict crop yields using satellite imagery. We plan to charge a monthly subscription fee based on farm size."
    
    print("Testing Idea Agent with sample idea...")
    result = extract_startup_details(sample_idea)
    
    assert result is not None, "Failed to get a response from the model. Check if API key is valid."
    assert isinstance(result, dict), "The response should be a JSON object (dictionary)."
    
    expected_keys = ["startup_name", "industry", "target_market", "core_proposition", "revenue_model"]
    for key in expected_keys:
        assert key in result, f"Missing key in JSON response: {key}"
        
    print("Idea Agent returned structured data successfully:")
    import json
    print(json.dumps(result, indent=2))
    return True

if __name__ == "__main__":
    result = test_idea_extraction()
    if not result:
        exit(1)
