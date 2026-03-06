from fastapi import FastAPI
from models import StartupInput
from llm_service import build_prompt, get_llm_response
from scoring import calculate_overall

app = FastAPI()


@app.post("/validate")
def validate(data: StartupInput):

    prompt = build_prompt(data)

    result = get_llm_response(prompt)

    market = result["market_score"]
    competition = result["competition_score"]
    feasibility = result["feasibility_score"]

    overall = calculate_overall(market, competition, feasibility)

    result["overall_score"] = overall

    return result