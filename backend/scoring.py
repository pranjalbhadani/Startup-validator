"""
Scoring Engine
Integrates scores from all agents using a weighted formula.
"""


def calculate_overall(
    market_score: int, competition_score: int, feasibility_score: int
) -> float:
  
    
    overall = (
        competition_score
    )

    return round(overall, 2)
