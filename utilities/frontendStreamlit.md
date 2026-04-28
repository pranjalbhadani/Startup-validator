Below is a **Streamlit-optimized AI agent prompt** rewritten from your instructions.
This version tells an AI coding agent to **generate a full Streamlit dashboard UI**, not a generic frontend.

---

# Streamlit App Generation Prompt

## Venture Validator — Startup Idea Intelligence Dashboard

---

# 1. Role

You are a **senior Python developer and Streamlit UI architect**.

Your task is to build a **professional Streamlit web application** called **Venture Validator** that evaluates startup ideas using historical startup data and AI-based analysis.

The interface should feel like a **venture capital research dashboard**, not a simple form.

The final output must be **clean, modular, production-ready Streamlit code**.

---

# 2. Technology Stack

Build the application using:

* **Python**
* **Streamlit**
* **Pandas**
* **Plotly** (for charts and gauge)
* Optional styling via **custom CSS injected with `st.markdown`**

The layout should use:

* `st.sidebar`
* `st.container`
* `st.columns`
* `st.metric`
* `st.dataframe`
* `st.plotly_chart`

---

# 3. Design Inspiration

The UI should resemble modern **data intelligence dashboards** such as:

* Stripe Dashboard
* Linear
* Notion analytics
* Google AI Studio

Key visual characteristics:

* Light modern UI
* Card-based layout
* Minimal but analytical
* Subtle shadows
* Rounded containers

---

# 4. UI Theme (Light)

Implement a **clean and trustworthy light theme**.

### Background

```
#F8FAFC
```

### Cards

```
#FFFFFF
```

### Primary Accent

```
#4F46E5 (Indigo)
```

### Secondary Accent

```
#06B6D4 (Cyan)
```

### Text Color

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

Add styling via **custom CSS inside Streamlit**.

---

# 5. Page Layout Structure

The page should follow a **dashboard structure**.

```
HEADER

SIDEBAR NAVIGATION

MAIN WORKSPACE
    Startup Idea Input
    AI Keyword Extraction
    Evidence Dataset Table
    Risk Dashboard
    Risk Gauge
    Evidence Explanation

FOOTER
```

---

# 6. Header Section

Top section of the page:

Title

```
Venture Validator
```

Subtitle

```
Evidence-Based Startup Intelligence
```

Description

```
Validate startup ideas using real historical startup data.
```

Display using:

```
st.title()
st.subheader()
st.markdown()
```

---

# 7. Sidebar Navigation

Create a sidebar using:

```
st.sidebar
```

Menu items:

```
Dashboard
Validate Idea
Evidence Dataset
Analysis History
About
```

Optional: Use icons or emojis.

---

# 8. Startup Idea Input Panel

Create a **research-style submission panel**.

Fields:

* Startup Name
* Idea Description (large text area)
* Industry
* Target Market
* Technology

Example Streamlit inputs:

```
st.text_input()
st.text_area()
st.selectbox()
```

CTA button:

```
Analyze Idea
```

Button should trigger the analysis pipeline.

---

# 9. AI Keyword Extraction Section

Section title:

```
AI Understanding of Your Idea
```

Display extracted keywords as **tag-like chips**.

Example:

```
AI
Logistics
Food Delivery
Prediction
```

Use styled markdown or small containers to mimic **tags**.

---

# 10. Evidence from Startup Dataset

Display a table of similar startups.

Example dataset:

| Startup     | Similarity | Outcome |
| ----------- | ---------- | ------- |
| Instacart   | 0.82       | Active  |
| QuickCart   | 0.74       | Closed  |
| FoodPredict | 0.71       | Failed  |

Use:

```
st.dataframe()
```

Add optional **similarity bars** or formatting.

Outcome labels should be color coded:

* Active → Green
* Closed / Failed → Red
* Acquired → Amber

---

# 11. Evidence Analytics Dashboard

Create **three metric cards** using `st.columns`.

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

Implementation:

```
col1, col2, col3 = st.columns(3)

col1.metric("Failure Rate", "60%")
col2.metric("Competition Level", "Medium")
col3.metric("Similar Startups", "5")
```

---

# 12. Risk Score Visualization

Create a **professional risk gauge** using Plotly.

Display:

```
Risk Score: 5.7 / 10
Moderate Risk
```

Use a **Plotly gauge chart**.

Color ranges:

0–3 → Green
3–6 → Yellow
6–10 → Red

Embed using:

```
st.plotly_chart()
```

---

# 13. Evidence Explanation Panel

Section title:

```
Why This Score?
```

Example explanation:

```
3 out of 5 similar startups failed in the market.

This domain has moderate competition with several
existing logistics platforms.

Historical data indicates moderate operational risk.
```

Add a small analytics icon:

```
📊
```

---

# 14. Data Source Credibility

Display a small badge:

```
Data Source: Crunchbase Startup Dataset
```

Place below the evidence table.

This improves **credibility of analysis**.

---

# 15. UI Details That Improve Quality

Add the following subtle improvements.

### Divider Lines

Use:

```
st.divider()
```

---

### Tooltips

Explain metrics like:

```
Failure Rate ⓘ
```

---

### Evidence Strength Badge

Example:

```
Evidence Strength: High
```

---

# 16. Typography

Preferred fonts:

Headings

```
Inter
```

Body

```
Source Sans
```

If fonts cannot be installed, use Streamlit defaults with similar spacing.

---

# 17. Expected Code Structure

The AI should generate **clean modular code**.

Example structure:

```
app.py

components/
    sidebar.py
    input_panel.py
    evidence_table.py
    risk_dashboard.py
    risk_gauge.py
```

Keep logic separated from UI when possible.

---

# 18. UI Personality

The interface must feel like:

* Venture capital research tool
* Startup intelligence dashboard
* Analytical platform

Avoid:

* Chatbot UI
* Student form UI
* Minimal prototype appearance

---

# 19. Final Objective

When someone opens the Streamlit app they should immediately think:

> This looks like a professional startup intelligence dashboard used by investors.

The design must communicate:

* Data credibility
* Analytical depth
* Professional SaaS quality

---

✅ If you want, I can also give you a **much stronger “Streamlit super-prompt”** that makes AI generate a **10× more impressive dashboard** with:

* animated risk gauges
* similarity graphs
* startup clustering visualization
* interactive evidence explorer

which makes **college demos look like real SaaS products**.
