"""
Build the processed modeling dataset.

Pipeline:
- load cleaned bank-full-clean.csv
- add engineered bucket features
- encode target y
- save to data/processed/processed_bank_full.csv
"""

import pandas as pd
from config import CFG
from utils.data_manager import read_csv_data, save_processed_data
from utils.transforms import add_bucket_features
from utils.preprocessing import ensure_target_numeric

def build_processed_dataset() -> pd.DataFrame:
    """
    Build and persist processed dataset used by all downstream pipelines.

    Returns:
        Processed DataFrame (saved to data/processed/bank-full-cleaned-processed-engineered.csv)
    """
    df = read_csv_data(CFG.PROCESSED_DATA_REL + "/" + CFG.CLEAN_BANK_REL)
    df = add_bucket_features(df)
    df = ensure_target_numeric(df, target_col=CFG.TARGET_COL) # binary encode target

    save_processed_data(CFG.PROCESSED_BANK_REL, df)
    return df

def main() -> None:
    build_processed_dataset()


if __name__ == "__main__":
    main()
