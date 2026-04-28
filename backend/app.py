"""
Streamlit Frontend
User-facing interface for the Startup Idea Validator.
Connects to the FastAPI backend to run the multi-agent pipeline.

Design: IdeaProof-style — centered, minimal friction, big idea input,
optional structured fields, clean SaaS aesthetic.
"""

import streamlit as st
import requests

# ---------- Page Config ----------
st.set_page_config(
    page_title="Startup Idea Validator",
    page_icon="🚀",
    layout="centered",
)

# ---------- Custom CSS ----------
st.markdown(
    """
<style>
/* Restrict container width for a focused, SaaS feel */
.block-container {
    max-width: 750px;
}

/* Gradient hero title */
.hero-title {
    text-align: center;
    font-size: 2.6rem;
    font-weight: 800;
    background: linear-gradient(90deg, #6366f1, #22c55e);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.2rem;
}

.hero-subtitle {
    text-align: center;
    font-size: 1.05rem;
    color: #888;
    margin-bottom: 2rem;
    line-height: 1.6;
}

/* Feature bullets row */
.features {
    display: flex;
    justify-content: center;
    gap: 1.2rem;
    flex-wrap: wrap;
    margin-bottom: 1.5rem;
}
.features span {
    font-size: 0.88rem;
    color: #555;
}

/* Score cards */
.score-card {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    padding: 1.5rem;
    border-radius: 12px;
    text-align: center;
    color: white;
    margin-bottom: 1rem;
}
.score-value {
    font-size: 2.4rem;
    font-weight: 800;
}
.score-label {
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    opacity: 0.8;
}

/* Hide default Streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
""",
    unsafe_allow_html=True,
)

# ---------- HERO SECTION ----------
st.markdown(
    '<div class="hero-title">Validate Your Startup Idea</div>',
    unsafe_allow_html=True,
)
st.markdown(
    """
    <div class="hero-subtitle">
        Describe your startup idea and get instant analysis on market potential,
        competition, and feasibility.
    </div>
    """,
    unsafe_allow_html=True,
)

# Feature highlights
st.markdown(
    """
    <div class="features">
        <span>✔ Market demand analysis</span>
        <span>✔ Competitor intelligence</span>
        <span>✔ Startup viability score</span>
        <span>✔ Actionable recommendations</span>
    </div>
    """,
    unsafe_allow_html=True,
)

st.divider()

# ---------- MAIN IDEA INPUT ----------
st.subheader("Your Startup Idea")

idea_description = st.text_area(
    "Describe your idea",
    placeholder=(
        "Example:\n"
        "An AI tool that automatically summarizes long YouTube videos\n"
        "into short study notes for students."
    ),
    height=160,
)

# ---------- OPTIONAL DETAILS (Expander) ----------
with st.expander("Add more details (optional)"):
    col1, col2 = st.columns(2)

    with col1:
        startup_name = st.text_input(
            "Startup name",
            placeholder="e.g., EduAI",
        )
        target_market = st.text_input(
            "Target customers",
            placeholder="Students, small businesses, freelancers...",
        )

    with col2:
        revenue_model = st.selectbox(
            "Revenue model",
            [
                "Not sure yet",
                "Subscription",
                "Freemium",
                "Marketplace fees",
                "Ads",
                "One-time purchase",
            ],
        )

st.divider()

# ---------- VALIDATE BUTTON ----------
validate = st.button("Validate My Idea", use_container_width=True)

# ---------- PROCESS ----------
if validate:
    if not idea_description or idea_description.strip() == "":
        st.warning("Please describe your startup idea first.")
    else:
        # Default startup_name if not provided
        name = startup_name if startup_name else "My Startup"
        market = target_market if target_market else "General"
        revenue = revenue_model if revenue_model != "Not sure yet" else ""

        with st.spinner("🤖 Analyzing your idea... This may take 15-30 seconds."):
            try:
                response = requests.post(
                    "http://127.0.0.1:8000/validate",
                    json={
                        "startup_name": name,
                        "idea_description": idea_description,
                        "target_market": market,
                        "revenue_model": revenue,
                    },
                    timeout=120,
                )

                if response.status_code == 200:
                    result = response.json()

                    st.success("Analysis Complete!")
                    st.divider()

                    # --- Score Cards ---
                    st.subheader("📊 Validation Scores")
                    c1, c2, c3, c4 = st.columns(4)

                    with c1:
                        st.markdown(
                            f"""
                            <div class="score-card">
                                <div class="score-label">Market</div>
                                <div class="score-value">{result.get("market_score", "N/A")}/10</div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                    with c2:
                        st.markdown(
                            f"""
                            <div class="score-card">
                                <div class="score-label">Competition</div>
                                <div class="score-value">{result.get("competition_score", "N/A")}/10</div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                    with c3:
                        st.markdown(
                            f"""
                            <div class="score-card">
                                <div class="score-label">Feasibility</div>
                                <div class="score-value">{result.get("feasibility_score", "N/A")}/10</div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                    with c4:
                        overall = result.get("overall_validation_score", "N/A")
                        st.markdown(
                            f"""
                            <div class="score-card" style="background: linear-gradient(135deg, #0f3443 0%, #34e89e 100%);">
                                <div class="score-label">Overall</div>
                                <div class="score-value">{overall}/10</div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                    st.divider()

                    # --- Idea Summary ---
                    st.subheader("🏷️ Idea Summary")
                    st.write(
                        f"**Industry Detected:** {result.get('industry_detected', 'N/A')}"
                    )
                    st.write(
                        f"**Core Proposition:** {result.get('core_proposition', 'N/A')}"
                    )
                    keywords = result.get("keywords", [])
                    if keywords:
                        st.write(f"**Keywords:** {', '.join(keywords)}")

                    st.divider()

                    # --- Risk & Market Assessment ---
                    col_left, col_right = st.columns(2)

                    with col_left:
                        st.subheader("⚠️ Risk Assessment")
                        risk_level = result.get("risk_level", "Unknown")
                        risk_icons = {"Low": "🟢", "Medium": "🟡", "High": "🔴"}
                        st.write(
                            f"**Risk Level:** {risk_icons.get(risk_level, '⚪')} {risk_level}"
                        )
                        st.write(
                            f"**Assessment:** {result.get('risk_reasoning', 'N/A')}"
                        )
                        st.write(
                            f"**Market Assessment:** {result.get('market_reasoning', 'N/A')}"
                        )

                    with col_right:
                        st.subheader("🏆 Competitors Found")
                        competitors = result.get("competitors", [])
                        if competitors:
                            for i, comp in enumerate(competitors, 1):
                                st.write(
                                    f"**{i}. {comp.get('competitor_name', 'N/A')}** — "
                                    f"{comp.get('market', 'N/A')} "
                                    f"(Status: {comp.get('status', 'N/A')})"
                                )
                        else:
                            st.info("No competitors found in the database.")

                    st.divider()

                    # --- Next Step ---
                    st.subheader("Next Step")
                    st.info(
                        "Your idea has been analyzed for market demand, "
                        "competition, and feasibility. Use these insights "
                        "to refine your strategy!"
                    )

                    # --- Raw JSON ---
                    with st.expander("🔧 View Raw JSON Response"):
                        st.json(result)

                else:
                    st.error(f"Backend returned status code: {response.status_code}")
                    st.json(response.json())

            except requests.exceptions.ConnectionError:
                st.error(
                    "Could not connect to the backend server. "
                    "Make sure `uvicorn main:app --reload` is running in the MVP folder."
                )
            except requests.exceptions.Timeout:
                st.error("Request timed out. The pipeline is taking too long.")
            except Exception as e:
                st.error(f"An error occurred: {e}")
