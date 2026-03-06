import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")


def build_prompt(data):

    prompt = f"""
You are a startup validation system.

Analyze the startup idea and return ONLY valid JSON.

Startup Name: {data.startup_name}
Idea Description: {data.idea_description}
Target Market: {data.target_market}
Revenue Model: {data.revenue_model}

Return JSON with:
market_score (0-10)
competition_score (0-10)
feasibility_score (0-10)
risk_level
swot:
  strengths
  weaknesses
  opportunities
  threats
recommendations
"""

    return prompt


def get_llm_response(prompt):

    response = model.generate_content(prompt)

    text = response.text.strip()

    try:
        return json.loads(text)
    except:
        return {"error": "Invalid JSON from model", "raw": text}