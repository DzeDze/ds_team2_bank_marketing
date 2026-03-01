import pandas as pd

from utils.data_manager import read_raw_data, save_processed_data

OUTPUT_FILE = "processed_bank_full.csv"

def add_balance_bucket_feature(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add a balance bucket feature.

    Non-negative balances are split into three quantiles
    (low, mid, high), while negative balances are labeled
    as 'negative'.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataset containing a 'balance' column.

    Returns
    -------
    pd.DataFrame
        DataFrame with an added 'balance_bucket' column.
    """
    if "balance" not in df.columns:
        raise ValueError("Column 'balance' is required")
    
    df = df.copy()

    # Bucket non-negative balances
    df.loc[df["balance"] >= 0, "balance_bucket"] = pd.qcut(
        df.loc[df["balance"] >= 0, "balance"],
        q=3,
        labels=["low", "mid", "high"],
        duplicates="drop"
    )

    # Convert to object to allow new category assignment
    df["balance_bucket"] = df["balance_bucket"].astype(object)

    # Assign negative bucket
    df.loc[df["balance"] < 0, "balance_bucket"] = "negative"

    return df

def add_age_bucket_feature(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add an age bucket feature.

    Age groups:
        18-25
        25-35
        35-45
        45-55
        55-65
        65+

    Parameters
    ----------
    df : pd.DataFrame
        Input dataset containing an 'age' column.

    Returns
    -------
    pd.DataFrame
        DataFrame with an added 'age_bucket' column.
    """

    if "age" not in df.columns:
        raise ValueError("Column 'age' is required")
    
    df = df.copy()

    df["age_bucket"] = pd.cut(
        df["age"],
        bins=[18, 25, 35, 45, 55, 65, 100],
        labels=[
            "18-25",
            "25-35",
            "35-45",
            "45-55",
            "55-65",
            "65+"
        ]
    )

    return df

def save_data(df: pd.DataFrame) -> None:
    """
    Save the processed dataset to the processed data directory.

    Parameters
    ----------
    df : pd.DataFrame
        Processed dataset to be saved.
    """
    save_processed_data(OUTPUT_FILE, df)

def main() -> None:
    """
    Run the feature engineering pipeline.

    Steps
    -----
    1. Load raw data
    2. Create balance buckets
    3. Create age buckets
    4. Save processed dataset
    """

    data = read_raw_data()

    data = add_balance_bucket_feature(data)
    data = add_age_bucket_feature(data)

    print("Data columns:", data.columns.values)

    save_data(data)

if __name__ == "__main__":
    main()
