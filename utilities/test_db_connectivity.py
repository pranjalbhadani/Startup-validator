import os
import requests
import chromadb
from chromadb.utils import embedding_functions

def test_chromadb_direct_connection():
    """Test direct connectivity to the ChromaDB vector database."""
    print("=" * 60)
    print("1. Testing Direct ChromaDB Connectivity")
    print("=" * 60)
    
    # Points to d:\startup_validator\data\startup_vectordb
    project_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
    db_path = os.path.join(project_root, "data", "startup_vectordb")
    print(f"Checking database at: {db_path}")
    
    if not os.path.exists(db_path):
        print("[ERROR] Database directory not found!")
        return False
        
    try:
        chroma_client = chromadb.PersistentClient(path=db_path)
        sentence_transformer_ef = embedding_functions.DefaultEmbeddingFunction()
        
        # The competitor_agent creates a collection named "crunchbase_startups"
        collection = chroma_client.get_collection(
            name="crunchbase_startups", 
            embedding_function=sentence_transformer_ef
        )
        
        count = collection.count()
        print(f"[SUCCESS] Successfully connected to ChromaDB.")
        print(f"[INFO] Collection 'crunchbase_startups' contains {count} records.")
        
        if count == 0:
            print("[WARNING] The database is empty. You need to run the data loading script in competitor_agent.py.")
        
        return True
    except ValueError as e:
        print(f"[ERROR] Collection 'crunchbase_startups' does not exist. {e}")
        return False
    except Exception as e:
        print(f"[ERROR] Failed to connect to ChromaDB: {e}")
        return False

def test_backend_api_connectivity():
    """Test that the backend API can run the pipeline and access the database."""
    print("\n" + "=" * 60)
    print("2. Testing Backend API Connectivity (app.py integration point)")
    print("=" * 60)
    
    # This is the same endpoint that backend/app.py uses
    api_url = "http://127.0.0.1:8000/validate"
    print(f"Sending test request to {api_url}...")
    
    test_payload = {
        "startup_name": "TestAI",
        "idea_description": "An AI tool for generating automated test scripts for software engineers.",
        "target_market": "Software Developers",
        "revenue_model": "SaaS Subscription"
    }
    
    try:
        response = requests.post(api_url, json=test_payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print("[SUCCESS] Successfully communicated with the Backend API.")
            print(f"[INFO] Competitors found by the pipeline: {len(result.get('competitors', []))}")
            print(f"[INFO] Overall Validation Score: {result.get('overall_validation_score', 'N/A')}/10")
            print("Connectivity test PASSED!")
            return True
        else:
            print(f"[ERROR] Backend returned status code {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("[ERROR] Connection refused. Is the FastAPI backend running?")
        print("Please run `uvicorn main:app --reload` in the backend directory.")
        return False
    except requests.exceptions.Timeout:
        print("[ERROR] Request timed out. The pipeline might be taking too long.")
        return False
    except Exception as e:
        print(f"[ERROR] An unexpected error occurred: {e}")
        return False

if __name__ == "__main__":
    db_ok = test_chromadb_direct_connection()
    if db_ok:
        test_backend_api_connectivity()
