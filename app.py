import streamlit as st
import pandas as pd
import numpy as np
import pickle
import shap
import matplotlib.pyplot as plt

# --- 1. PAGE CONFIG ---
st.set_page_config(
    page_title="NCD Stock-out Predictor",
    page_icon="💊",
    layout="centered"
)

# --- 2. LOAD ASSETS ---
@st.cache_data
def load_assets():
    """Loads the model and background data."""
    with open('ncd_model.pkl', 'rb') as f:
        model = pickle.load(f)
    
    background_data = pd.read_csv("shap_background_data.csv")
    df_featured = pd.read_csv("ncd_stock_data_featured.csv")
    
    return model, background_data, df_featured

try:
    model, background_data, df_featured = load_assets()
    DRUG_LIST = sorted(df_featured['Drug'].unique())
    FEATURE_NAMES = model.feature_names_in_
except FileNotFoundError:
    st.error("Model or data files not found. Please run the training notebook and feature engineering script first.")
    st.stop()

# --- 3. UI ---
st.title("NCD Medication Stock-out Predictor 💊")
st.markdown("Enter current data to forecast the risk of a medication stock-out for next month.")
st.divider()

st.header("Step 1: Enter Current Month's Data")
col1, col2 = st.columns(2)
with col1:
    selected_drug = st.selectbox("Select Medication:", options=DRUG_LIST)
    opening_balance = st.number_input("Opening Balance", min_value=0, value=1500)
    quantity_received = st.number_input("Quantity Received", min_value=0, value=0)
with col2:
    consumption = st.number_input("Consumption", min_value=0, value=500)
    losses = st.number_input("Losses & Adjustments", min_value=0, value=20)

# --- 4. PREDICTION LOGIC ---
st.divider()
st.header("Step 2: Run Prediction")

if st.button("Forecast Stock-out Risk", type="primary", use_container_width=True):
    
    closing_balance = opening_balance + quantity_received - consumption - losses
    current_date = pd.to_datetime('today')
    
    input_data = pd.DataFrame(
        [[opening_balance, quantity_received, consumption, losses, closing_balance, 
          current_date.month, current_date.year, current_date.quarter, 
          consumption, consumption]], # Using current consumption as a proxy for lag/roll features
        columns=FEATURE_NAMES
    )
    
    st.write("---")
    st.subheader("Prediction Result:")
    
    prediction_proba = model.predict_proba(input_data)[0]
    prediction = model.predict(input_data)[0]
    risk_score = prediction_proba[1]

    if prediction == 1:
        st.error(f"High Risk of Stock-out (Risk Score: {risk_score:.0%})")
    else:
        st.success(f"Low Risk of Stock-out (Risk Score: {risk_score:.0%})")
        
    # --- SHAP EXPLANATION ---
    with st.expander("Why did the model make this prediction?"):
        
        # Use the more general shap.Explainer
        explainer = shap.Explainer(model.predict, background_data)
        shap_values = explainer(input_data)
        
        # Create a new figure for the plot
        fig, ax = plt.subplots()
        
        # For waterfall, we now have a clean shap_values object for a single prediction.
        # We select the first (and only) instance with [0].
        shap.plots.waterfall(shap_values[0], max_display=10, show=False)
        
        st.pyplot(fig)