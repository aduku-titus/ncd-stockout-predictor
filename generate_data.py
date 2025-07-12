import pandas as pd
import numpy as np
import datetime

# --- Configuration ---
DRUGS = [
    # Tier 1
    "Amlodipine 5mg", "Lisinopril 10mg", "Metformin 500mg", "Atorvastatin 20mg", "Bendroflumethiazide 2.5mg",
    # Tier 2
    "Nifedipine 20mg", "Losartan 50mg", "Atenolol 50mg", "Glibenclamide 5mg", "Soluble Aspirin 75mg",
    # Tier 3
    "Methyldopa 250mg", "Hydralazine 25mg", "Insulin Mixtard", "Insulin Actrapid"
]

START_DATE = datetime.date(2020, 1, 1)
END_DATE = datetime.date(2024, 12, 31)

# --- Main Script ---

def generate_synthetic_data(drugs, start, end):
    """Generates a synthetic dataset for drug stock management."""
    
    date_range = pd.date_range(start, end, freq='MS') # MS for Month Start
    data = []

    print(f"Generating data for {len(drugs)} drugs from {start} to {end}...")

    for drug in drugs:
        # Establish a baseline for this drug
        is_high_volume = "Metformin" in drug or "Amlodipine" in drug
        base_consumption = np.random.randint(500, 2000) if is_high_volume else np.random.randint(100, 500)
        
        # Initial stock is 2-3x the base consumption
        opening_balance = base_consumption * np.random.uniform(2, 3)

        for date in date_range:
            # Simulate monthly consumption with seasonality and growth
            month = date.month
            year_factor = 1 + (date.year - start.year) * 0.05 # 5% annual growth
            seasonal_factor = 1 + np.sin(2 * np.pi * (month - 1) / 12) * 0.1 # 10% seasonal swing
            consumption = int(base_consumption * year_factor * seasonal_factor * np.random.uniform(0.85, 1.15))
            
            # Simulate receiving new stock every 2-3 months
            quantity_received = 0
            if month % np.random.choice([2, 3]) == 0:
                quantity_received = int(base_consumption * np.random.uniform(2.5, 3.5))

            # Simulate losses and adjustments (small percentage of opening balance)
            losses = int(opening_balance * np.random.uniform(0, 0.02))

            # Calculate closing balance before stock-out check
            closing_balance_pre = opening_balance + quantity_received - consumption - losses
            
            # Simulate stock-outs
            days_out_of_stock = 0
            if closing_balance_pre < (0.25 * base_consumption): # If stock is below 1 week's worth
                # Higher chance of stocking out if low
                if np.random.rand() < 0.6: 
                    days_out_of_stock = np.random.randint(1, 15)
            
            # Final closing balance cannot be negative
            closing_balance_final = max(0, closing_balance_pre)
            
            # Append record
            data.append({
                "Date": date,
                "Hospital": "Tatale District Hospital",
                "Drug": drug,
                "Opening_Balance": int(opening_balance),
                "Quantity_Received": quantity_received,
                "Consumption": consumption,
                "Losses_Adjustments": losses,
                "Closing_Balance": int(closing_balance_final),
                "Days_Out_of_Stock": days_out_of_stock
            })

            # The next month's opening balance is this month's closing balance
            opening_balance = closing_balance_final
    
    print("Data generation complete.")
    return pd.DataFrame(data)

if __name__ == "__main__":
    df = generate_synthetic_data(DRUGS, START_DATE, END_DATE)
    
    # Save to CSV
    output_filename = "synthetic_drug_data.csv"
    df.to_csv(output_filename, index=False)
    
    print(f"\nSuccessfully generated and saved data to '{output_filename}'")
    print(f"Total records created: {len(df)}")
    print("Data head:")
    print(df.head())