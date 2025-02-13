import pandas as pd

def load_fire_data(csv_path):
    """
    Load fire event data from a CSV file.

    Parameters:
        csv_path (str): Path to the CSV file.

    Returns:
        pandas.DataFrame: DataFrame containing fire event data.
    """
    return pd.read_csv(csv_path)
