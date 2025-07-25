# Validated Learnings from a Human-Centered Design Process

## Project: NCD Medication Stock-out Predictor

This document outlines the key design hypotheses and validated learnings from the development of the NCD Stock-out Predictor dashboard. The design process was guided by a deep understanding of the end-user: a busy clinician (pharmacist or senior nurse) in a resource-constrained district hospital in Ghana.

### Core Design Hypothesis

Our central hypothesis was that for a predictive tool to be adopted in this environment, it must prioritize **simplicity, trust, and accessibility** over feature density. The goal was not to build a complex data science platform, but a "single-question, single-answer" tool that could integrate into an existing workflow in under 30 seconds, providing an immediate and understandable forecast.
---

### Key Design Decisions & Validated Learnings

**1. Learning: Simplicity Over Data Density**
*   **Decision:** We intentionally chose *not* to display complex historical charts or statistical tables on the main user interface. The UI is built around a simple set of inputs and a single primary action button.
*   **Justification:** Based on my own frontline clinical experience, I know that clinicians face a high cognitive load. An interface cluttered with extraneous data would be perceived as a burden, not a tool, leading to poor adoption.
*   **Validation:** The final MVP interface is built around a single primary action ("Forecast Risk") and provides a single, color-coded output, directly validating our "simplicity-first" approach.

**2. Learning: Interpretability as a Prerequisite for Trust**
*   **Decision:** We chose to include a "Why did the model make this prediction?" expander, which displays the top SHAP features driving the forecast.
*   **Justification:** A "black box" prediction, even if accurate, would be met with skepticism. By providing the *reasons* for a prediction (e.g., "High Risk BECAUSE: Opening Balance was low"), we translate the model's logic into a language the clinician can understand and verify against their own professional judgment. This is the cornerstone of building trust in clinical AI.

**3. Learning: Knowledge Translation is the Ultimate Goal**
*   **Decision:** The final output of the project was not a research paper or a model file, but a deployed, interactive dashboard.
*   **Justification:** The project's ultimate success is not measured by model accuracy, but by its potential to be translated into a real-world intervention. The Streamlit dashboard is an act of **knowledge translation**, bridging the gap between abstract data science and the concrete, daily decisions of a healthcare professional. This artifact demonstrates a commitment to creating tangible impact, not just theoretical findings.
