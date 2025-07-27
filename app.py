import streamlit as st
import pandas as pd
import numpy as np
import pickle
import shap
import matplotlib.pyplot as plt
import os

# ===================================================================
# --- 1. PAGE CONFIGURATION ---
# Sets the title, icon, and layout for the web page.
# This must be the first Streamlit command in the script.
# ===================================================================
st.set_page_config(
    page_title="NCD Stock-out Predictor",
    page_icon="💊",
    layout="centered"
)

# ===================================================================
# --- 2. ASSET LOADING ---
# Defines a function to load all necessary files (model, data).
# Uses @st.cache_data to ensure these heavy files are loaded only once,
# making the app much faster on subsequent runs.
# ===================================================================
@st.cache_data
def load_assets():
    """
    Loads all necessary assets using absolute paths to be robust in deployment environments.
    """
    # Get the absolute path to the directory where this script is located
    _this_file_path = os.path.dirname(os.path.abspath(__file__))
    
    # Define absolute paths to the asset files
    model_path = os.path.join(_this_file_path, 'ncd_model.pkl')
    background_data_path = os.path.join(_this_file_path, 'shap_background_data.csv')
    featured_data_path = os.path.join(_this_file_path, 'ncd_stock_data_featured.csv')

    # Load the assets using their full paths
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
        
    background_data = pd.read_csv(background_data_path)
    df_featured = pd.read_csv(featured_data_path)
    
    return model, background_data, df_featured

# Try to load the assets. If any file is missing, show a user-friendly error and stop the app.
try:
    model, background_data, df_featured = load_assets()
    DRUG_LIST = sorted(df_featured['Drug'].unique())
    FEATURE_NAMES = model.feature_names_in_
except FileNotFoundError:
    st.error("Model or data files not found. Please ensure all required files are present.")
    st.stop()

# ===================================================================
# --- 3. USER INTERFACE (The "Input" of I-P-O-S) ---
# This section defines all the interactive widgets for user input.
# ===================================================================
st.title("NCD Medication Stock-out Predictor 💊")
st.markdown("Enter the most recent data for a medication to forecast the risk of a stock-out for the next month.")
st.divider()

st.header("Step 1: Enter Current Month's Data")

# Use columns for a cleaner layout
col1, col2 = st.columns(2)
with col1:
    selected_drug = st.selectbox("Select Medication:", options=DRUG_LIST)
    # min_value=0 is a form of error handling, preventing negative inputs
    opening_balance = st.number_input("Opening Balance", min_value=0, value=1500, step=10)
    quantity_received = st.number_input("Quantity Received", min_value=0, value=0, step=10)
with col2:
    consumption = st.number_input("Consumption", min_value=0, value=500, step=10)
    losses = st.number_input("Losses & Adjustments", min_value=0, value=20, step=1)

# ===================================================================
# --- 4. PREDICTION LOGIC (The "Process" and "Output" of I-P-O-S) ---
# This block only runs when the user clicks the prediction button.
# ===================================================================
st.divider()
st.header("Step 2: Run Prediction")

if st.button("Forecast Stock-out Risk", type="primary", use_container_width=True):
    
    # --- Robustness Check: Add Error Handling for illogical inputs ---
    if consumption > (opening_balance + quantity_received):
        st.warning("Warning: Monthly consumption is greater than the total available stock. Please check your inputs.")
    
    # --- Process Part 1: Feature Engineering ---
    # Create the necessary features for the model from the user's inputs.
    closing_balance = opening_balance + quantity_received - consumption - losses
    current_date = pd.to_datetime('today')
    
    # Assemble the input data into a DataFrame with the exact column order and names the model was trained on.
    input_data = pd.DataFrame(
        [[opening_balance, quantity_received, consumption, losses, closing_balance, 
          current_date.month, current_date.year, current_date.quarter, 
          consumption, consumption]], # Using current consumption as a proxy for lag/roll features
        columns=FEATURE_NAMES
    )
    
    st.write("---")
    st.subheader("Prediction Result:")
    
    # --- Process Part 2: Prediction ---
    # Use the loaded model to predict the probability and the final class (0 or 1).
    prediction_proba = model.predict_proba(input_data)[0]
    prediction = model.predict(input_data)[0]
    risk_score = prediction_proba[1] # The probability of the "Stock-out" class

    # --- Output Part 1: Display the Prediction ---
    # Use color-coded outputs to clearly communicate the result.
    if prediction == 1:
        st.error(f"High Risk of Stock-out (Risk Score: {risk_score:.0%})")
    else:
        st.success(f"Low Risk of Stock-out (Risk Score: {risk_score:.0%})")
        
    # --- Output Part 2: Explain the Prediction ---
    # Use an expander to show the "why" without cluttering the UI.
    with st.expander("Why did the model make this prediction?"):
        
        # Create the SHAP explainer and calculate values for this specific prediction
        explainer = shap.Explainer(model.predict, background_data)
        shap_values = explainer(input_data)
        
        # Create a new matplotlib figure to prevent plots from overlapping
        fig, ax = plt.subplots()
        
        # Generate and display the waterfall plot for the single prediction
        shap.plots.waterfall(shap_values[0], max_display=10, show=False)
        st.pyplot(fig)