import pandas as pd

def extract_day_time(df):
    """
    Extracts day of the week and hour from the 'Consult_date' column.
    
    Args:
        df (pandas.DataFrame): DataFrame containing the 'Consult_date' column.
    
    Returns:
        pandas.DataFrame: DataFrame with added 'Day' and 'Hour' columns.
    """
    df['Consult_date'] = pd.to_datetime(df['Consult_date'])
    df['Day'] = df['Consult_date'].dt.day_name()
    df['Hour'] = df['Consult_date'].dt.hour
    return df

def prepare_time_series_data(df):
    """
    Prepares data for time-series analysis by aggregating consultation counts by date.
    
    Args:
        df (pandas.DataFrame): DataFrame with 'Consult_date' column.
    
    Returns:
        pandas.DataFrame: Aggregated DataFrame with 'Consult_date' and 'Counts'.
    """
    df['Consult_date'] = pd.to_datetime(df['Consult_date']).dt.date
    aggregated_data = df.groupby('Consult_date').size().reset_index(name='Counts')
    return aggregated_data

