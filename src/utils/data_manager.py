import pandas as pd
import os

RAW_DATA_FILE = "bank-full.csv"
SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
RAW_DATA_DIR  = os.path.normpath(os.path.join(SCRIPT_DIR, "..", "..", "data", "raw"))
OUTPUT_DIR  = os.path.normpath(os.path.join(SCRIPT_DIR, "..", "..", "data", "processed"))
# OUTPUT_PATH = os.path.join(OUTPUT_DIR, TARGET_FILE)

def read_raw_data() -> pd.DataFrame:
    """
    Load the raw bank marketing dataset.

    Returns
    -------
    pd.DataFrame
        Raw dataset loaded from `data/raw/bank-full.csv`.
    """
    print("Reading raw data..")
    path = os.path.join(RAW_DATA_DIR, RAW_DATA_FILE)
    df = pd.read_csv(path, sep=";")
    print(f"Successfully read {RAW_DATA_FILE}")
    print(f"{len(df)} rows, {len(df.columns)} columns")
    return df

def save_processed_data(relative_path: str, data:pd.DataFrame) -> None:
    """
    Save a processed dataset under the `data/processed/` directory.

    Parameters
    ----------
    relative_path : str
        Relative output path inside `data/processed/`.

        Examples
        --------
        save_processed_data("clean/train.csv", df)
        -> data/processed/clean/train.csv

        save_processed_data("viz/summary.csv", df)
        -> data/processed/viz/summary.csv

    data : pd.DataFrame
        DataFrame to save.

    Notes
    -----
    - Missing directories are created automatically.
    - Data is saved as CSV without the index.
    """
    print("Saving processed data...")

    save_path = os.path.normpath(
        os.path.join(OUTPUT_DIR, relative_path)
    )

    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    data.to_csv(save_path, index=False)

    print(f"Saved: {save_path}")