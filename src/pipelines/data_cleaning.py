"""
Build and persist the cleaned bank marketing dataset.

Pipeline:
- load raw bank-full.csv via data_manager.read_raw_data()
- apply cleaning steps
- save to data/processed/bank-full-clean.csv
"""

import pandas as pd

from config import CFG
from utils.data_manager import read_raw_data, save_processed_data
from utils.preprocessing import clean_bank_data

def build_clean_dataset() -> pd.DataFrame:
    """
    Build and persist cleaned dataset used by downstream pipelines.

    Returns
    -------
    pd.DataFrame
        Cleaned DataFrame (saved to data/processed/bank-full-clean.csv)
    """
    df = read_raw_data()
    df = clean_bank_data(df)
    save_processed_data(CFG.CLEAN_BANK_REL, df)
    return df

def main() -> None:
    build_clean_dataset()

if __name__ == "__main__":
    main()