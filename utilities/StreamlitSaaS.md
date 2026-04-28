# 🚀 Streamlit Super Prompt

# Venture Validator — AI Startup Intelligence Platform

---

# 1. Role

You are a **senior Python engineer, data visualization expert, and Streamlit application architect**.

Your task is to build a **professional SaaS-style Streamlit web application** called **Venture Validator**.

The platform analyzes startup ideas using **AI-based concept extraction and historical startup datasets** to generate an **evidence-based risk score**.

The interface should look like a **venture capital intelligence platform used by analysts**.

---

# 2. Tech Stack

Use the following tools:

Core

* Python
* Streamlit

Data

* Pandas
* NumPy

Visualization

* Plotly
* NetworkX (for similarity graph)
* Altair (optional)

UI Enhancements

* Custom CSS via `st.markdown`
* `st.columns`
* `st.container`
* `st.tabs`

Optional

* Sentence Transformers
* Scikit-learn clustering

---

# 3. Product Inspiration

The UI should resemble modern **startup intelligence dashboards** like:

* Stripe Dashboard
* Linear
* Notion analytics
* Google AI Studio

Design philosophy:

* minimal
* analytical
* card-based
* investor-grade

---

# 4. UI Theme

Light professional dashboard theme.

### Background

```
#F8FAFC
```

### Card Background

```
#FFFFFF
```

### Primary Accent

```
#4F46E5
```

### Secondary Accent

```
#06B6D4
```

### Text

```
#334155
```

### Borders

```
#E2E8F0
```

### Risk Colors

Low Risk

```
#22C55E
```

Moderate Risk

```
#F59E0B
```

High Risk

```
#EF4444
```

---

# 5. Layout Structure

The application should contain:

```
HEADER

SIDEBAR NAVIGATION

MAIN WORKSPACE

    Idea Input Panel

    AI Understanding Panel

    Evidence Dataset

    Evidence Analytics Dashboard

    Similarity Visualization

    Risk Score Dashboard

    Explanation Panel

FOOTER
```

---

# 6. Sidebar Navigation

Create navigation inside:

```
st.sidebar
```

Menu:

```
Dashboard
Validate Idea
Evidence Explorer
Startup Network
Analysis History
About
```

---

# 7. Idea Input Panel

Create a **research submission style panel**.

Fields:

* Startup Name
* Idea Description
* Industry
* Target Market
* Technology

Example UI elements:

```
st.text_input
st.text_area
st.selectbox
```

Primary button:

```
Analyze Idea
```

Button should trigger the analysis pipeline.

---

# 8. AI Understanding Panel

Title:

```
AI Understanding of Your Idea
```

Display extracted keywords as **tag chips**.

Example:

```
AI
Logistics
Food Delivery
Prediction
```

Tags should appear inside small rounded boxes.

---

# 9. Evidence Dataset Panel

Show similar startups retrieved from the dataset.

Example:

| Startup     | Similarity | Outcome |
| ----------- | ---------- | ------- |
| Instacart   | 0.82       | Active  |
| QuickCart   | 0.74       | Closed  |
| FoodPredict | 0.71       | Failed  |

Display using:

```
st.dataframe
```

Add color-coded outcome badges.

---

# 10. Evidence Analytics Dashboard

Create **three metric cards**.

Use:

```
st.columns(3)
```

Metrics:

Failure Rate

```
60%
```

Competition Level

```
Medium
```

Similar Startups

```
5
```

Use:

```
st.metric
```

---

# 11. Advanced Visualization 1

# Animated Risk Gauge

Use **Plotly gauge chart**.

Display:

```
Risk Score: 5.7 / 10
Moderate Risk
```

Color ranges:

```
0–3  → Green
3–6  → Yellow
6–10 → Red
```

Animate the gauge when the score is generated.

---

# 12. Advanced Visualization 2

# Startup Similarity Graph

Create a **network graph** using NetworkX.

Structure:

```
User Idea → node

Connected nodes:
Instacart
QuickCart
FoodPredict
```

Edges represent similarity scores.

Edge thickness = similarity.

Display using Plotly scatter network.

---

# 13. Advanced Visualization 3

# Startup Clustering Map

Use **embedding + clustering** to visualize startup categories.

Possible methods:

* Sentence embeddings
* PCA or UMAP
* KMeans clustering

Visualization:

```
2D scatter plot
```

Clusters represent:

```
FinTech
AI
HealthTech
Logistics
Ecommerce
```

User idea appears as a **highlighted point**.

---

# 14. Advanced Visualization 4

# Similarity Bar Chart

Show similarity scores visually.

Example:

```
Instacart   ██████████ 0.82
QuickCart   ████████   0.74
FoodPredict ███████    0.71
```

Use:

```
Plotly horizontal bar chart
```

---

# 15. Evidence Explanation Panel

Title:

```
Why This Score?
```

Example explanation:

```
3 out of 5 similar startups failed in the market.

This domain has moderate competition with several
existing logistics platforms.

Historical startup data indicates operational risk.
```

Include small icon:

```
📊
```

---

# 16. Evidence Explorer Page

Create an **interactive dataset explorer**.

Features:

Filters:

* Industry
* Funding stage
* Outcome

Charts:

* Startup outcomes distribution
* Industry failure rates

Use:

```
st.selectbox
st.multiselect
```

---

# 17. Startup Network Page

Visualize startup relationships.

Graph showing:

```
startup similarity clusters
```

User idea appears as central node.

Use:

* NetworkX
* Plotly

---

# 18. Data Credibility Section

Display dataset source.

Example:

```
Data Source:
Crunchbase Startup Dataset
```

This increases trust.

---

# 19. Code Structure

Generate **clean modular code**.

Example:

```
app.py

components/
    sidebar.py
    input_panel.py
    risk_gauge.py
    evidence_table.py

visualizations/
    similarity_graph.py
    clustering_map.py
```

---

# 20. UI Personality

The app must feel like:

✔ Venture capital research dashboard
✔ Startup intelligence platform
✔ Data science tool

Avoid:

❌ chatbot interface
❌ basic student form
❌ plain Streamlit prototype

---

# 21. Final Goal

When someone opens the app they should immediately think:

> This looks like a real startup intelligence SaaS product.

The design should communicate:

* credibility
* analytical depth
* modern data platform

---