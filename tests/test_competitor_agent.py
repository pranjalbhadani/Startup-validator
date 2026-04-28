# ==========================================
# TEST THE AGENT
# ==========================================
if __name__ == "__main__":
    # UNCOMMENT THE LINE BELOW and run it ONCE to build your database using your clean CSV.
    # Then comment it out again so you don't rebuild it every time!
    
    # build_database_once("data/cleaned_crunchbase.csv")
    
    # Fake output from Agent 1 (Testing the hand-off)
    fake_agent1_data = {
        "startup_name": "MedConnect",
        "industry": "HealthTech",
        "target_market": "Elderly people in rural India",
        "core_proposition": "A video consultation platform connecting rural elderly with city doctors."
    }
    
    # Run Agent 2
    found_competitors = find_competitors(fake_agent1_data)
    
    print("--- AGENT 2 OUTPUT (Top 5 Competitors Found) ---")
    for comp in found_competitors:
        print(f"Name: {comp['competitor_name']} | Status: {comp['status']} | Market: {comp['market']}")
