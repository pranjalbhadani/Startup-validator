"""
Agent 1: Idea Understanding Agent
Analyzes raw startup idea text and extracts structured information.
"""

import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load environment variables from MVP/.env
load_dotenv()

# Initialize the Gemini client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Force JSON output from the model
generation_config = types.GenerateContentConfig(response_mime_type="application/json")


def extract_startup_details(
    user_idea_text: str,
    startup_name: str = "Unknown",
    target_market: str = "",
    revenue_model: str = "",
):
    """
    Takes raw startup idea text and optional metadata.
    Returns a structured dictionary with extracted fields:
      - startup_name, industry, keywords, target_market,
        core_proposition, revenue_model
    """

    system_prompt = f"""
You are an expert Startup Idea Analysis Agent.

Your job is to extract structured information from a startup idea.

Return ONLY valid JSON with the following fields:

{{
  "startup_name": "",
  "industry": "",
  "keywords": [],
  "target_market": "",
  "core_proposition": "",
  "revenue_model": ""
}}

Rules:
- startup_name: Use "{startup_name}" if provided, otherwise extract from idea or return "Unknown"
- industry: Must be short (EdTech, FinTech, HealthTech, AI, E-commerce, SaaS, etc.)
- keywords: List of 3-5 relevant keywords describing the idea
- target_market: Use "{target_market}" if provided, otherwise extract from idea
- core_proposition: Must be one sentence summarizing the core value
- revenue_model: Use "{revenue_model}" if provided, otherwise extract from idea
- Return ONLY valid JSON, no extra text
"""

    prompt = f"{system_prompt}\n\nStartup Idea:\n{user_idea_text}"

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash", contents=prompt, config=generation_config
        )

        structured_data = json.loads(response.text)
        print("[Agent 1 - Idea Agent] Successfully extracted startup details.")
        return structured_data

    except Exception as e:
        print(f"[Agent 1 - Idea Agent] Error: {e}")
        # Return a fallback structure so the pipeline doesn't break
        return {
            "startup_name": startup_name,
            "industry": "Unknown",
            "keywords": [],
            "target_market": target_market,
            "core_proposition": user_idea_text[:100],
            "revenue_model": revenue_model,
        }
