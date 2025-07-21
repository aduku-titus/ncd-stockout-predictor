import pandas as pd

def create_features(input_filepath="ncd_stock_data_analysis_ready.csv", 
                    output_filepath="ncd_stock_data_featured.csv"):
    """
    Loads the clean data, creates time-based features, and saves the result.
    """
    print("Loading clean data...")
    df = pd.read_csv(input_filepath)
    
    # Ensure 'Date' is a datetime object
    df['Date'] = pd.to_datetime(df['Date'])
    
    print("Creating time-series features...")
    # --- Feature Engineering ---
    # Create features from the 'Date' column that a model can learn from.
    df['month'] = df['Date'].dt.month
    df['year'] = df['Date'].dt.year
    df['quarter'] = df['Date'].dt.quarter
    
    # Lag features: What was the consumption last month?
    # This is a very powerful feature for time-series problems.
    df = df.sort_values(by=['Drug', 'Date'])
    df['consumption_lag_1'] = df.groupby('Drug')['Consumption'].shift(1)
    
    # Rolling features: What was the average consumption over the last 3 months?
    df['consumption_roll_mean_3'] = df.groupby('Drug')['Consumption'].transform(
        lambda x: x.rolling(3, 1).mean()
    )

    # Drop rows with NaN values created by lag/rolling features
    df.dropna(inplace=True)
    
    print("Feature engineering complete.")
    
    # Save the new, featured data
    df.to_csv(output_filepath, index=False)
    print(f"Successfully saved featured data to '{output_filepath}'")
    
    return df

if __name__ == "__main__":
    create_features()