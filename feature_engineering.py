# 3_feature_engineering.py (Refactored for Testability)
import pandas as pd

def create_features(df):
    """
    Takes a clean DataFrame and creates time-based features.
    
    Args:
        df (pd.DataFrame): The clean input DataFrame.
        
    Returns:
        pd.DataFrame: The DataFrame with new feature columns.
    """
    # Ensure 'Date' is a datetime object
    df['Date'] = pd.to_datetime(df['Date'])
    
    # --- Feature Engineering ---
    df['month'] = df['Date'].dt.month
    df['year'] = df['Date'].dt.year
    df['quarter'] = df['Date'].dt.quarter
    
    df = df.sort_values(by=['Drug', 'Date'])
    df['consumption_lag_1'] = df.groupby('Drug')['Consumption'].shift(1)
    
    df['consumption_roll_mean_3'] = df.groupby('Drug')['Consumption'].transform(
        lambda x: x.rolling(3, 1).mean()
    )

    df.dropna(inplace=True)
    return df

# This main block allows the script to still be run directly
if __name__ == "__main__":
    print("Loading clean data...")
    clean_df = pd.read_csv("ncd_stock_data_analysis_ready.csv")
    
    print("Creating features...")
    featured_df = create_features(clean_df.copy()) # Pass a copy to the function
    
    output_filename = "ncd_stock_data_featured.csv"
    featured_df.to_csv(output_filename, index=False)
    print(f"Successfully saved featured data to '{output_filename}'")
    