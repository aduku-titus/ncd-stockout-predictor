import streamlit as st
import datetime

# --- Page Configuration (Set this at the very top) ---
st.set_page_config(
    page_title="AdherenceAide",
    page_icon="💊",
    layout="centered"
)

# --- 1. STATE MANAGEMENT (The "S" in IPOS) ---
# Initialize the logbook in session_state if it doesn't exist.
# This code runs ONCE per session.
if 'dose_log' not in st.session_state:
    st.session_state.dose_log = []

# --- 2. USER INTERFACE (The "I" and "O" in IPOS) ---
st.title("AdherenceAide 💊")
st.markdown("Welcome, Mr. George! Press the button below each time you take your morning pill.")

st.divider() # Visual separator

# The INPUT widget: A big button
if st.button("Log My Morning Pill", type="primary", use_container_width=True):
    # --- 3. PROCESS (The "P" in IPOS) ---
    # This block of code only runs WHEN the button is clicked.
    
    # Get the current time
    now = datetime.datetime.now()
    
    # Add the new timestamp to the front of our list in STATE
    st.session_state.dose_log.insert(0, now)
    
    # Show a temporary success message (Part of OUTPUT)
    st.success(f"Dose logged successfully at {now.strftime('%I:%M %p on %A, %B %d')}")

st.divider()

# The OUTPUT display area
st.header("Your Dose History")

if not st.session_state.dose_log:
    st.info("You have not logged any doses yet. Click the button above to start.")
else:
    # Display the log from STATE
    for entry in st.session_state.dose_log:
        st.write(f"- {entry.strftime('%A, %B %d, %Y at %I:%M:%S %p')}")
