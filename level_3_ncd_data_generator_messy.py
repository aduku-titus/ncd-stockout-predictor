import pandas as pd
import numpy as np
import datetime

# ===================================================================
# --- 1. CONFIGURATION ---
# All high-level settings are here. Easy to change without touching the logic.
# ===================================================================
DRUGS = [
    # Tier 1
    "Amlodipine 5mg", "Lisinopril 10mg", "Metformin 500mg", "Atorvastatin 20mg", 
    "Bendroflumethiazide 2.5mg", "Nifedipine 20mg", "Losartan 50mg", "Atenolol 50mg", 
    "Glibenclamide 5mg", "Soluble Aspirin 75mg", "Methyldopa 250mg", "Hydralazine 25mg"
]
START_DATE = datetime.date(2020, 1, 1)
END_DATE = datetime.date(2024, 12, 31)
OUTPUT_FILENAME = "ncd_stock_data_dynamic_messy.csv" # <-- Updated Filename


# ===================================================================
# --- 2. FUNCTION DEFINITIONS ---
# This section defines our "tools" but doesn't run them yet.
# ===================================================================

def generate_messy_stock_data(drug_list, start, end):
    """
    Generates a realistic, messy dataset for NCD stock management, including
    common data errors like missing values, outliers, and incorrect data types.
    """
    print(f"Generating MESSY data for {len(drug_list)} drugs from {start} to {end}...")
    
    date_range = pd.date_range(start, end, freq='MS')
    all_records = []

    for drug in drug_list:
        base_consumption = np.random.randint(500, 3000)
        opening_balance = base_consumption * 3
        
        for date in date_range:
            # --- Generate a "clean" record for this month first ---
            consumption = int(base_consumption * np.random.uniform(0.85, 1.15))
            quantity_received = int(base_consumption * 3) if date.month % 3 == 0 else 0
            losses = int(opening_balance * np.random.uniform(0, 0.02))
            
            # =============================================================
            # --- NEW: INTRODUCE BUGS (Chaos Engineering) ---
            # =============================================================

            # 1. Missing Value Bug: 10% chance for Consumption to be missing
            if np.random.rand() < 0.10: # np.random.rand() is a float between 0.0 and 1.0
                consumption = np.nan # np.nan is the standard for missing numbers

            # 2. Outlier Bug: 2% chance for Consumption to be 10x the normal
            #    We use 'elif' so a value can't be both missing AND an outlier.
            elif np.random.rand() < 0.02: 
                consumption = consumption * 10
            
            # 3. Negative Value Bug: 1% chance for Consumption to be negative
            elif np.random.rand() < 0.01:
                consumption = -50
            
            # --- Calculate Balances (handle potential missing consumption) ---
            
            # NEW: Add defensive code to handle the missing values we created.
            if pd.isna(consumption):
                # If consumption is unknown, we can't calculate closing balance accurately.
                # A simple business rule: assume no change from what we have.
                closing_balance_final = opening_balance + quantity_received - losses
            else:
                # If consumption is a valid number, use the normal formula.
                closing_balance_final = opening_balance + quantity_received - consumption - losses

            # Ensure stock never goes below zero
            if closing_balance_final < 0:
                closing_balance_final = 0

            # --- Assemble the final record, including the data type bug ---
            record = {
                "Date": date,
                "Drug": drug,
                # 4. Incorrect Data Type Bug: Intentionally save as a string
                "Opening_Balance": str(int(opening_balance)), 
                "Quantity_Received": quantity_received,
                "Consumption": consumption,
                "Losses_Adjustments": losses,
                "Closing_Balance": int(closing_balance_final),
                "Days_Out_of_Stock": 0 
            }
            all_records.append(record)
            
            # This logic remains the same: link months together
            opening_balance = closing_balance_final
            
    print("...messy data generation complete.")
    return pd.DataFrame(all_records)


# ===================================================================
# --- 3. MAIN EXECUTION BLOCK ---
# ===================================================================

if __name__ == "__main__":
    
    # Call the newly renamed function
    messy_df = generate_messy_stock_data(DRUGS, START_DATE, END_DATE)
    
    # Save the result to our new messy filename
    messy_df.to_csv(OUTPUT_FILENAME, index=False)
    
    print(f"\nSuccessfully generated and saved MESSY data to '{OUTPUT_FILENAME}'")
    print(f"Total records created: {len(messy_df)}")
    
    # Show a sample to verify
    print("\nSample of the messy data (notice the NaN):")
    # Display more rows to increase the chance of seeing a bug in the sample
    print(messy_df.sample(10))