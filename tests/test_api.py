import os
from google import genai
from dotenv import load_dotenv


def test_google_api_key():
    # Check current directory, or try MVP directory specifically
    env_path = os.path.join(os.path.dirname(__file__), "..", "MVP", ".env")
    if os.path.exists(env_path):
        load_dotenv(dotenv_path=env_path)
    else:
        load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY")
    assert api_key is not None, "GEMINI_API_KEY is not set. Check your .env file."
    assert api_key != "YOUR_GEMINI_API_KEY_HERE", (
        "GEMINI_API_KEY still has the dummy placeholder."
    )

    print("API Key found. Testing authentication...")

    try:
        # Initialize the new client
        client = genai.Client(api_key=api_key)

        # Using a fast lightweight model for testing key validity
        response = client.models.generate_content(
            model="gemini-2.5-flash", contents="Reply with exactly the word 'SUCCESS'."
        )

        assert response.text is not None
        print("API test successful. Response from Gemini:", response.text.strip())
        return True

    except Exception as e:
        print(f"API test failed. Error detail: {e}")
        return False


if __name__ == "__main__":
    result = test_google_api_key()
    if not result:
        exit(1)
