import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

generation_config = types.GenerateContentConfig(response_mime_type="application/json")


def extract_startup_details(user_idea_text: str):
    """
    Agent 1: Idea Understanding Agent
    Converts raw startup idea text into structured data.
    """

    system_prompt = """
You are an expert Startup Idea Analysis Agent.

Your job is to extract structured information from a startup idea.

Return ONLY JSON with the following fields:

{
 "startup_name": "",
 "industry": "",
 "target_market": "",
 "core_proposition": "",
 "revenue_model": ""
}

Rules:
- industry must be short (EdTech, FinTech, HealthTech, AI, E-commerce etc)
- core_proposition must be one sentence
- If startup_name not mentioned return "Unknown"
- Return ONLY JSON
"""

    prompt = f"{system_prompt}\n\nStartup Idea:\n{user_idea_text}"

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash", contents=prompt, config=generation_config
        )

        structured_data = json.loads(response.text)

        return structured_data

    except Exception as e:
        print("Agent1 Error:", e)

        return None
