import pandas as pd
from feature_engineering import create_features

def test_create_features_columns():
    """
    Tests if the create_features function adds the correct new columns.
    """
    # Arrange: Create a small, simple DataFrame for the test
    data = {
        'Date': pd.to_datetime(['2024-01-01', '2024-02-01', '2024-03-01']),
        'Drug': ['Metformin', 'Metformin', 'Metformin'],
        'Consumption': [100, 110, 120]
    }
    test_df = pd.DataFrame(data)
    
    # Act: Run the function we want to test
    result_df = create_features(test_df)
    
    # Assert: Check if the output is what we expect
    expected_columns = ['month', 'year', 'quarter', 'consumption_lag_1', 'consumption_roll_mean_3']
    
    for col in expected_columns:
        assert col in result_df.columns

def test_lag_feature_calculation():
    """
    Tests if the lag feature is calculated correctly.
    """
    # Arrange
    data = {
        'Date': pd.to_datetime(['2024-01-01', '2024-02-01']),
        'Drug': ['Metformin', 'Metformin'],
        'Consumption': [100, 110]
    }
    test_df = pd.DataFrame(data)
    
    # Act
    result_df = create_features(test_df)
    
    # Assert
    # The first row's lag should be NaN and dropped, so the result should have 1 row
    assert len(result_df) == 1
    # The lag value in the first remaining row should be the consumption from the previous month
    assert result_df['consumption_lag_1'].iloc[0] == 100