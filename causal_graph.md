# Causal Graph for NCD Medication Stock-outs

## Author: Titus Afeo Azure Aduku
## Date: [Current Date]

---

### 1. Introduction

This document outlines a causal model for understanding the drivers of Non-Communicable Disease (NCD) medication stock-outs at a district hospital in Ghana. It moves beyond simple correlation to map the hypothesised cause-and-effect relationships that lead to a stock-out event. This first-principles thinking is the foundation for effective feature engineering and building a robust, context-aware predictive model.

The graph is structured from "upstream" (distant, root causes) to "downstream" (immediate, direct causes).

---

### 2. The Causal Model

#### **Upstream Factors (Systemic & Environmental)**

These are high-level factors that create the conditions for supply chain disruptions and demand fluctuations.

*   **Logistical Factors:**
    *   `National Supply Chain Health`: Issues at the central medical store can affect shipment size and timing.
    *   `Regional Transportation Infrastructure`: Road conditions, especially during the rainy season, can delay shipments.
*   **Public Health & Social Factors:**
    *   `Regional Events`: Market days or local festivals can cause temporary surges in the local population.
    *   `Public Health Campaigns`: A mass screening event for hypertension can lead to a sudden increase in newly diagnosed patients.

#### **Midstream Factors (Local & Behavioral)**

These are the direct drivers of monthly supply and demand at the hospital level.

*   **Drivers of Supply:**
    *   `Shipment Arrival & Size`: Whether a shipment arrives on time and if it is the full requested amount. (Caused by Upstream Logistical Factors).
    *   `Previous Month's Closing Balance`: The inventory carried over from the last period.
*   **Drivers of Demand:**
    *   `Local Disease Incidence & Prevalence`: The underlying rate of NCDs in the community. (Influenced by Public Health Campaigns).
    *   `Population Fluctuation`: Changes in the number of people seeking care in the district. (Influenced by Regional Events).
    *   `Patient Adherence & Attrition`: Factors like patients defaulting on treatment or traveling, which can decrease expected demand.

#### **Downstream Factors (The Immediate Precursors)**

These are the two variables that mathematically determine the risk of a stock-out in a given month.

*   `Stock Available During Month`: The total amount of a drug available for dispensing. (Determined by `Opening Balance` + `Shipment Arrival`).
*   `Monthly Consumption`: The total amount of a drug dispensed to patients. (Determined by the Drivers of Demand).

#### **The Final Outcome (Clinical Event)**

*   **`Stock-out Event`**: Occurs when `Monthly Consumption` exceeds the `Stock Available During Month`.

---

### 3. Implications for Predictive Modeling

This causal model directly informs our feature engineering strategy. A robust predictive model should include features that act as proxies for these causal drivers. For example:
*   `month` and `quarter` features can act as proxies for seasonal effects (like rainy season).
*   `consumption_lag_1` and `consumption_roll_mean_3` act as proxies for the underlying patient demand and adherence trends.

By understanding the causal structure of the problem, we can build a more effective and interpretable predictive system.