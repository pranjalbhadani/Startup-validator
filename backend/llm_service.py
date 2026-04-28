"""
LLM Service
Shared utility for interacting with the Gemini API.
Used by individual agents that need direct LLM access.
"""

import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize the Gemini client (shared across the service)
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def get_llm_response(prompt: str) -> dict:
    """
    Sends a prompt to the Gemini model and returns a parsed JSON response.
    Falls back to an error dict if JSON parsing fails.
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(response_mime_type="application/json"),
    )

    text = response.text.strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"error": "Invalid JSON from model", "raw": text}
