Below is a **clean, production-ready AI agent prompt** created from your design instructions.
It is structured so an **AI UI generator, frontend agent, or code-generation model** can clearly understand the requirements.

---

# Venture Validator UI Design Prompt

## 1. Role

You are a **senior product designer and frontend UI architect** responsible for designing a **modern SaaS-style startup intelligence dashboard interface**.

Your task is to design a **clean, light-themed, professional UI** for a platform called **Venture Validator** that validates startup ideas using historical startup data.

The interface must feel like a **venture capital research tool**, not a chatbot or simple form.

---

# 2. Design Inspiration

The interface should visually resemble modern **startup intelligence and research tools**.

Use the following products as **design inspiration**:

* Stripe Dashboard
* Linear
* Notion analytics interface
* Google AI Studio

Key characteristics:

* Soft light palettes
* Card-based layouts
* Subtle shadows
* Clean typography
* Minimal but data-rich interface
* Analytical feel

The UI should look like a **startup intelligence research platform used by venture capital analysts**.

---

# 3. Color Palette (Light + Trustworthy)

Use a **cool and professional light theme**.

### Background

```
#F8FAFC
```

### Card Background

```
#FFFFFF
```

### Primary Accent (Buttons / Highlights)

```
#4F46E5  (Indigo)
```

### Secondary Accent

```
#06B6D4  (Cyan)
```

### Primary Text

```
#334155
```

### Borders / Dividers

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

The palette should feel:

* Modern
* Calm
* Analytical
* Credible

---

# 4. Background Design

The page background must **not be plain**.

Add a **very subtle grid pattern**.

Design specification:

* Light grid lines
* Opacity: **3–5%**
* Barely visible
* Creates a **data science workspace aesthetic**

---

# 5. Layout Style

Use a **card-based dashboard layout**.

Each major section should appear inside a **soft elevated card**.

Card properties:

* Rounded corners
* Soft shadow
* Thin border (`#E2E8F0`)
* Generous padding

Example page structure:

```
----------------------------------
Startup Idea Input
----------------------------------

----------------------------------
AI Keyword Extraction
----------------------------------

----------------------------------
Evidence from Dataset
----------------------------------

----------------------------------
Risk Score Dashboard
----------------------------------
```

---

# 6. Header Design

Top navigation header.

### Title

```
Venture Validator
```

### Subtitle

```
Evidence-Based Startup Intelligence
```

### Supporting tagline

```
Validate startup ideas using real historical data.
```

Include:

* Small **AI + data icon**
* Clean horizontal layout

---

# 7. Sidebar Navigation

Include a left sidebar with navigation.

Menu items:

```
Dashboard
Validate Idea
Evidence Dataset
Analysis History
About
```

Style:

* Minimal icons
* Hover highlight
* Soft divider lines

---

# 8. Startup Idea Input Panel

This section should feel like a **research submission interface**.

Fields:

```
Startup Name
Idea Description
Industry
Target Market
Technology
```

Main Input:

```
Describe your startup concept
[ Large text area ]
```

### CTA Button

Label:

```
Analyze Idea
```

Button style:

Gradient

```
Indigo → Cyan
```

Rounded edges with subtle shadow.

---

# 9. AI Keyword Extraction Section

Title:

```
AI Understanding of Your Idea
```

Display extracted keywords as **rounded tags/chips**.

Example tags:

```
AI
Logistics
Food Delivery
Prediction
```

Tag style:

Background

```
#EEF2FF
```

Text

```
#4338CA
```

Rounded pill style.

---

# 10. Evidence Section (Analytical Table)

This section must feel like **real data analysis**.

Table example:

| Startup     | Similarity | Outcome |
| ----------- | ---------- | ------- |
| Instacart   | 0.82       | Active  |
| QuickCart   | 0.74       | Closed  |
| FoodPredict | 0.71       | Failed  |

Use colored badges for outcomes.

Active

```
Green
```

Closed / Failed

```
Red
```

Acquired

```
Amber
```

Add:

* subtle row hover highlight
* optional similarity bars

Example visualization:

```
Instacart   ██████████ 0.82
QuickCart   ████████   0.74
FoodPredict ███████    0.71
```

---

# 11. Risk Dashboard

Create **three analytics cards**.

### Card 1

```
Failure Rate
60%
```

### Card 2

```
Competition Level
Medium
```

### Card 3

```
Similar Startups
5
```

Each card should contain:

* Icon
* Large number
* Small label

---

# 12. Risk Score Visualization

Use a **circular gauge indicator**.

Display:

```
Risk Score
5.7 / 10
Moderate Risk
```

Design:

Background ring

```
light gray
```

Progress ring

```
yellow
```

Optional implementation using **Plotly gauge chart**.

---

# 13. Evidence Explanation Panel

Title:

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

Include icon:

```
📊
```

---

# 14. Dataset Credibility Badge

Show data source clearly.

Example:

```
Data Source: Crunchbase Startup Dataset
```

This improves **credibility and trust**.

---

# 15. Small UI Details (Important)

### Tooltips

Example:

```
Failure Rate ⓘ
```

Hover should explain the metric.

---

### Dividers

Use soft divider lines:

```
#E2E8F0
```

---

### Evidence Confidence Badge

Example:

```
Evidence Strength: High
```

---

# 16. Typography

Use modern clean fonts.

Headings

```
Inter
```

Body

```
Source Sans
```

These fonts should create a **clean professional SaaS interface**.

---

# 17. UI Personality

The interface should feel like:

✔ Venture capital research tool
✔ Data intelligence platform
✔ Professional SaaS dashboard

Avoid looking like:

❌ AI chatbot
❌ student project form
❌ simple input-output tool

---

# 18. Landing Page (Optional)

Hero Section:

```
Venture Validator

Validate Startup Ideas Using Real Historical Data

Understand the risk of your startup concept
by comparing it with real companies from
startup datasets.

[ Validate Your Idea ]
```

---

# 19. How It Works Section

```
Step 1
Submit your startup idea

Step 2
AI extracts key concepts

Step 3
System finds similar startups

Step 4
Evidence-based risk score generated
```

---

# 20. Final Goal

When a user opens the interface, they should immediately think:

> "This looks like a professional startup intelligence dashboard used by investors."

The design must communicate:

* Data credibility
* Analytical depth
* Professional SaaS quality

---

If you'd like, I can also convert this into a **much more powerful prompt optimized for AI UI builders like**:

* v0 by Vercel
* Figma AI
* Cursor
* Bolt.new

That version produces **near-production React dashboards automatically**.
