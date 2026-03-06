def calculate_overall(market, competition, feasibility):

    overall = (
        0.4 * market +
        0.3 * feasibility +
        0.3 * (10 - competition)
    )

    return round(overall, 2)