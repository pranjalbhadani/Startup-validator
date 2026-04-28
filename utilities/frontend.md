The design principle is:

* minimal friction
* big idea input box
* motivational copy
* optional structured fields
* clean SaaS style

---

# Streamlit Prompt Page (IdeaProof-style)

This creates:

* hero section
* big idea input box
* optional startup fields
* validation button
* progress spinner
* clean layout

```python
import streamlit as st

st.set_page_config(
    page_title="Startup Idea Validator",
    page_icon="🚀",
    layout="centered"
)

# ---------- HERO ----------
st.markdown(
"""
<h1 style='text-align:center;'>Validate Your Startup Idea</h1>
<p style='text-align:center; font-size:18px; color:gray;'>
Describe your startup idea and get instant analysis on market potential,
competition, and feasibility.
</p>
""",
unsafe_allow_html=True
)

st.divider()

# ---------- MAIN IDEA INPUT ----------
st.subheader("Your Startup Idea")

idea = st.text_area(
    "Describe your idea",
    placeholder="""
Example:
An AI tool that automatically summarizes long YouTube videos 
into short study notes for students.
""",
height=160
)

# ---------- OPTIONAL DETAILS ----------
with st.expander("Add more details (optional)"):
    
    col1, col2 = st.columns(2)

    with col1:
        problem = st.text_input(
            "Problem you are solving",
            placeholder="What pain point does your product fix?"
        )

        target = st.text_input(
            "Target customers",
            placeholder="Students, small businesses, freelancers..."
        )

    with col2:
        solution = st.text_input(
            "Your solution",
            placeholder="AI powered summarization tool"
        )

        revenue = st.selectbox(
            "Revenue model",
            [
                "Not sure yet",
                "Subscription",
                "Freemium",
                "Marketplace fees",
                "Ads",
                "One-time purchase"
            ]
        )

# ---------- VALIDATE BUTTON ----------
st.divider()

validate = st.button("Validate My Idea", use_container_width=True)

# ---------- PROCESS ----------
if validate:

    if idea.strip() == "":
        st.warning("Please describe your startup idea first.")
    
    else:
        with st.spinner("Analyzing your idea..."):
            
            import time
            time.sleep(2)

        st.success("Analysis Complete")

        st.subheader("Idea Summary")

        st.write(idea)

        st.subheader("Next Step")

        st.info(
            "Your idea will now be analyzed for market demand, "
            "competition, and feasibility."
        )
```

---

# UI Tricks That Make It Look Like a Real SaaS

Add these improvements:

### 1️⃣ Centered container width

```python
st.markdown(
"""
<style>
.block-container {
    max-width: 750px;
}
</style>
""",
unsafe_allow_html=True
)
```

---

### 2️⃣ Gradient title

```css
background: linear-gradient(90deg,#6366f1,#22c55e);
-webkit-background-clip: text;
color: transparent;
```

---

### 3️⃣ Feature section (below input)

Example:

```
✔ Market demand analysis  
✔ Competitor intelligence  
✔ Startup viability score  
✔ Actionable recommendations
```

---

# Optional Advanced UI (Recommended)

You can make it feel **very close to IdeaProof** with:

* step-based flow

```
1 Describe Idea
2 AI Analysis
3 Results
```

Using:

```
st.progress()
```

or

```
streamlit-ant-design
```

---