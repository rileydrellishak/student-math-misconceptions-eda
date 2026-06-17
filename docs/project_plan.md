# Project Plan: Student Math Misconceptions EDA
**Course:** [AI Fluency: Framework & Foundations](https://anthropic.skilljar.com/ai-fluency-framework-foundations) — Project Planning and Delegation Exercise\
**Dataset:** MAP – Charting Student Math Misunderstandings ([Kaggle](https://www.kaggle.com/competitions/map-charting-student-math-misunderstandings/data))

---

## Project Overview

An exploratory data analysis (EDA) of student math misconceptions in grades 4–8, presented as an interactive web dashboard. The analysis is framed through an educator's lens — distinguishing procedural errors from conceptual misunderstandings — and is designed as a portfolio piece for both EdTech and data/analytics audiences.

---

## Success Criteria

- A polished, hosted, interactive web dashboard presenting EDA findings
- Educator perspective woven throughout the narrative and framing
- Pedagogically grounded recommendations, not just data summaries
- Shareable via link (GitHub Pages or similar) for portfolio use
- Meaningful to both EdTech employers and data/analytics employers

---

## Delegation Key

| Symbol | Meaning |
|--------|---------|
| 👤 | Primarily human |
| 🤖 | Primarily AI |
| 🤝 | Collaborative — highest impact zone |

---

## Phase 1 — EDA in Python

### Task 1: Load and Clean the Dataset

**Skills & capabilities needed:**
Python (pandas), understanding of competition dataset structure, ability to identify data quality issues (nulls, duplicates, mismatched IDs, inconsistent formatting)

| Role | Responsibility |
|------|---------------|
| 🤖 AI | Write all boilerplate cleaning code — loading files, checking dtypes, identifying nulls, merging dataframes, outputting a summary report |
| 👤 Human | Review the summary output and make judgment calls on anomalies (drop, fill, or flag) based on understanding of what the data represents |
| 🤝 Collaborate | Interpreting unexpected findings during cleaning — talking through surprises before deciding how to handle them |

**Delegation rationale:** Cleaning code is well-defined and repeatable — a strong AI task. Human energy is better spent on analysis and interpretation, not boilerplate. The cleaning script should output a plain-language summary (row counts, null counts, column names and types) so the human can do a quick sanity check without getting bogged down in code.

---

### Task 2: Explore Misconception Category Distributions

**Skills & capabilities needed:**
Python (pandas, matplotlib/seaborn), statistical thinking about distributions, domain knowledge of what misconception categories mean in a real math classroom

| Role | Responsibility |
|------|---------------|
| 🤖 AI | Generate visualization code, calculate frequency tables, produce a plain-language "here's what I notice" briefing of the distribution |
| 👤 Human | React to the AI briefing with educator lens — identify whether frequency patterns are surprising or expected based on classroom experience |
| 🤝 Collaborate | Interpreting spikes or anomalies in the distribution — human responds to AI summary rather than staring at raw data |

**Delegation rationale:** The human's cognitive strength is pattern *interpretation*, not pattern *detection*. AI generates the briefing; human provides the pedagogical reaction. This is a more natural and effective workflow than open-ended raw data exploration.

**Key question to drive this task:** *Is this a procedural error or a conceptual misunderstanding?* This distinction — which has fundamentally different implications for instruction — is a primary organizing lens for the entire dashboard.

---

### Task 3: Identify Patterns by Topic and Grade Level

**Skills & capabilities needed:**
Python grouped analysis (pandas groupby), understanding of math curriculum scope and sequence across grades 4–8, ability to distinguish statistically meaningful patterns from noise

| Role | Responsibility |
|------|---------------|
| 🤖 AI | Generate grouped visualizations, run cross-tabulations between misconception type and grade/topic, flag statistically notable patterns |
| 👤 Human | Connect grade-level patterns to curriculum sequence knowledge (e.g., recognizing that a grade 6 spike relates to the additive-to-multiplicative thinking transition) |
| 🤝 Collaborate | The moment of interpretation — AI surfaces a pattern, human provides the pedagogical explanation of *why* it exists |

**Delegation rationale:** Curriculum knowledge is irreplaceable human expertise here. AI has no intuition about when fractions are introduced, what makes proportional reasoning hard, or what conceptual leap a particular grade represents. This is where the educator's background creates the most differentiated value.

**Key output from this task:** Begin tagging patterns as *procedural vs. conceptual* — this categorization, grounded in teaching experience, becomes a primary organizing framework for the dashboard.

---

## Phase 2 — Educator Lens Analysis

### Task 1: Categorize Misconceptions as Procedural vs. Conceptual

**Skills & capabilities needed:**
Deep familiarity with math pedagogy, knowledge of how students develop mathematical thinking across grades 4–8, ability to reason about *why* a student would make a particular error — not just *that* they made it

| Role | Responsibility |
|------|---------------|
| 🤖 AI | Prepare the categorization workbench — pull unique misconception categories from the data and format them into a clean list ready for tagging; write concise descriptions of each category after tagging is complete |
| 👤 Human | Perform error analysis — examine the question, correct answer, and student answer; reverse-engineer the student's logic by replicating their missteps; apply the procedural vs. conceptual label based on teaching judgment |
| 🤝 Collaborate | Edge cases — misconceptions that sit in the grey zone between procedural and conceptual; AI surfaces how math education researchers have historically classified similar errors; human makes the final call |

**Delegation rationale:** This is the purest expression of teaching expertise in the entire project. The categorization process requires holding a mental model of how students think — not just what they got wrong. AI cannot replicate the intuition that comes from having been in the room when a student confidently produces a wrong answer. The categorization is also a *spectrum*, not a binary — some misconceptions are clearly one or the other, and some sit in between, which is itself an interesting finding.

**Method:** Examine question + correct answer + student answer → work backwards to identify what procedure or belief would produce that answer → determine whether the root cause is a broken procedure or a broken concept. Requires looking at actual student responses alongside misconception labels, not just category names in isolation.

---

### Task 2: Identify Instructional Implications

**Skills & capabilities needed:**
Knowledge of instructional strategies for math misconceptions, understanding of the difference between remediation (fixing a procedural gap) and re-teaching (rebuilding a conceptual model from scratch), familiarity with what's feasible in a real middle school classroom

| Role | Responsibility |
|------|---------------|
| 🤖 AI | Help cross-reference recommendations against general math education research to add supporting context; assist with articulating recommendations clearly and concisely for dashboard format |
| 👤 Human | Generate the actual recommendations — drawing on classroom experience to specify *what a teacher should do*, not just *what the problem is*; distinguish between a five-minute warm-up fix and a two-week re-teaching unit |
| 🤝 Collaborate | Prioritization — identifying which misconception patterns are most frequent, most impactful, and most actionable to focus human recommendation-writing energy where it matters most |

**Delegation rationale:** Specificity is what makes a recommendation credible to an educator audience. Generic advice ("address the misconception") is useless in practice. Human expertise is required to know which misconceptions respond to manipulatives, which need number talks, and which need a completely different representational approach.

**Key design principle:** Reduce teacher decision fatigue. Don't present everything equally — surface a prioritized "start here" recommendation based on frequency, grade relevance, and whether the error is conceptual (higher priority; harder to self-correct) vs. procedural.

---

### Task 3: Write the Educator Narrative

**Skills & capabilities needed:**
Clear, accessible writing for a mixed audience, ability to translate data findings into human-centered stories, a voice credible to educators without alienating data/analytics viewers

| Role | Responsibility |
|------|---------------|
| 🤖 AI | Draft, edit, and ensure consistency of narrative copy; help adapt tone for different dashboard sections; assist translating findings for dual audiences without writing two separate dashboards |
| 👤 Human | Provide the stories and the voice — real classroom moments (anonymized), the misconception that appeared on every test no matter what was tried, the re-teaching approach that finally clicked; make judgment calls on how much narrative is enough |
| 🤝 Collaborate | The central thesis / throughline — the framing statement that every section of the dashboard connects back to; getting this right is a back-and-forth conversation |

**Delegation rationale:** Authenticity is the key asset here. Classroom stories and a credible educator voice cannot be generated — they can only be edited. AI's role is to sharpen and shape what the human brings, not to originate it.

**Draft throughline:** *"Student math errors aren't random — they follow predictable patterns rooted in specific conceptual gaps, and knowing which gap is which changes everything about how you respond."*

---

## Phase 3 — Dashboard Build (JavaScript/React)

### Task 1: Design the Dashboard Layout and Information Architecture

**Skills & capabilities needed:**
UX thinking, narrative structure, understanding of how non-technical viewers scan and process visual information, knowledge of which findings are most important to lead with vs. build toward

| Role | Responsibility |
|------|---------------|
| 🤖 AI | Generate layout options and wireframe structures to react to; propose two or three dashboard architectures with different storytelling approaches (scrollytelling vs. tabbed navigation vs. single-page flow); flag UX patterns that work well for data storytelling dashboards |
| 👤 Human | Make the narrative sequencing decisions — determine what a teacher needs to understand first before a finding makes sense; apply pedagogical judgment to the order of sections |
| 🤝 Collaborate | The opening section — the first thing a viewer sees determines whether they keep scrolling; collaborating on the hook (headline, framing statement, first visual) is worth significant time |

**Delegation rationale:** The order of sections is a pedagogical decision as much as a design decision. Showing "most common misconceptions" before explaining the procedural vs. conceptual framework would be like giving someone the punchline before the setup. That sequencing judgment requires domain expertise.

---

### Task 2: Build the Data Pipeline from Python to Dashboard

**Skills & capabilities needed:**
Python (pandas, JSON export), understanding of what data shape React components expect, thinking ahead about what aggregations the dashboard needs so heavy computation doesn't happen in the browser

| Role | Responsibility |
|------|---------------|
| 🤖 AI | Write the export scripts once the required data shape is defined; suggest ideal JSON structures based on planned visualizations |
| 👤 Human | Decide what the dashboard actually needs — raw response-level data vs. pre-aggregated summaries; whether procedural/conceptual tags live in the JSON or are computed on the fly |
| 🤝 Collaborate | Catching mismatches early — talk through planned visualizations and data structure together before writing any code to prevent building a component and finding the data isn't shaped correctly |

**Delegation rationale:** The decision about data shape requires understanding both the analysis and the frontend simultaneously — a human judgment call. The export code itself, once the shape is defined, is well-defined and delegatable.

---

### Task 3: Build the Interactive Visualizations

**Skills & capabilities needed:**
React, charting library (Recharts or Chart.js), understanding of which chart types communicate which kinds of findings most clearly, accessibility awareness

| Role | Responsibility |
|------|---------------|
| 🤖 AI | Scaffold starter components for each visualization type — boilerplate Recharts/Chart.js code that the human then customizes and refines |
| 👤 Human | Select chart types based on what each visualization is communicating; decide which interactive filters are worth building based on which comparisons are most meaningful (grade vs. grade, topic vs. topic, procedural vs. conceptual) |
| 🤝 Collaborate | The procedural vs. conceptual visualization specifically — this is the most original analytical contribution and deserves a visualization that does it justice; exploring how to represent a spectrum (not just a binary) interactively |

**Delegation rationale:** Chart type selection and interaction design require understanding the *meaning* of the data, not just its structure. Component scaffolding is boilerplate — a strong AI task that frees human focus for communication decisions.

---

### Task 4: Build the Narrative Layer

**Skills & capabilities needed:**
React (text components, callout cards, recommendation panels), UX writing, ability to integrate narrative and data without one overwhelming the other

| Role | Responsibility |
|------|---------------|
| 🤖 AI | Build the UI components that house the narrative — recommendation cards, callout boxes, the "start here" priority highlight, tooltips that surface educator context on hover; edit and tighten narrative copy for clarity and concision |
| 👤 Human | Write the content for recommendation cards, callout boxes, and "what this means in your classroom" sections from lived experience; make judgment calls on how much narrative is enough |
| 🤝 Collaborate | The prioritization component — designing the logic and UI for how priority is communicated (ranking, highlight, suggested sequence) is a collaborative design problem requiring both pedagogical judgment and UX pattern knowledge |

**Delegation rationale:** The content is irreplaceable — it comes from lived classroom experience and will be immediately apparent to educator readers as authentic. The UI components that house it are well-defined React work that AI can scaffold efficiently.

---

## Phase 4 — Portfolio Packaging

### Task 1: Host the Dashboard

**Skills & capabilities needed:**
GitHub Pages or Netlify deployment, basic build configuration for a React app

| Role | Responsibility |
|------|---------------|
| 🤖 AI | Handle deployment configuration — build scripts, GitHub Actions setup, routing gotchas on static hosts |
| 👤 Human | Make the platform decision (GitHub Pages vs. Netlify vs. Vercel) based on existing portfolio setup and professional presentation goals |
| 🤝 Collaborate | Troubleshooting if anything breaks during deployment — fast back-and-forth beats solo debugging |

---

### Task 2: Write the README

**Skills & capabilities needed:**
Technical writing, ability to communicate project context and significance to both technical and non-technical readers

| Role | Responsibility |
|------|---------------|
| 🤖 AI | Structure, formatting, and technical sections — installation instructions, tech stack, data sources — following well-established README conventions |
| 👤 Human | The origin story — why a former middle school math teacher learned to code and built this; this narrative is uniquely human and the most compelling part of the README |
| 🤝 Collaborate | The project description paragraph at the top — the two or three sentences that determine whether someone keeps reading; worth a collaborative drafting session |

---

### Task 3: Portfolio Framing

**Skills & capabilities needed:**
Self-presentation, understanding of what each target audience values, ability to connect this project to a broader developer story

| Role | Responsibility |
|------|---------------|
| 🤖 AI | Help articulate the "so what" clearly and concisely; draft the one-paragraph project summary for portfolio site or LinkedIn |
| 👤 Human | Determine how this project fits into the Ada journey and what it says about you as a developer; own the interview narrative about your process |
| 🤝 Collaborate | The portfolio summary — making the teaching experience + technical skills narrative land for both audiences simultaneously |

**Key portfolio narrative:** Teaching experience *amplifies* technical skills rather than being separate from them. Five years in a middle school math classroom made this analysis richer than a purely technical approach could achieve. This project demonstrates that domain expertise and engineering capability are more powerful in combination than either alone.

---

## Notes

- **Primary analysis file:** `train.csv` (~90% of the work)
- **Supporting files:** `test.csv` (no labels, limited EDA value), `sample_submission.csv` (competition format only)
- **Tech stack:** Python for EDA, JavaScript/React for interactive dashboard, GitHub Pages or Netlify for hosting
- **Out of scope:** Building a predictive model, reproducing competition results, analyzing the test set
- **Design principle:** Reduce teacher decision fatigue — surface prioritized "start here" recommendations, don't present everything equally

---

*Last updated: All four phases fully documented. June 16, 2026*