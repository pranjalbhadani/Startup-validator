import streamlit as st
import requests

st.title("Startup Idea Validator")

name = st.text_input("Startup Name")
idea = st.text_area("Idea Description")
market = st.text_input("Target Market")
revenue = st.text_input("Revenue Model")

if st.button("Validate"):

    response = requests.post(
        "http://127.0.0.1:8000/validate",
        json={
            "startup_name": name,
            "idea_description": idea,
            "target_market": market,
            "revenue_model": revenue
        }
    )

    st.json(response.json())