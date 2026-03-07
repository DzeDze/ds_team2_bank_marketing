"""
src/pipelines/run_all.py

One command to regenerate everything:)
1) download_data        -> data/raw/bank-full.csv
2) data_cleaning        -> data/processed/bank-full-clean.csv
3) build_processed      -> data/processed/processed_bank_full.csv
4) export_segmentation  -> data/processed/viz/segmentation_data.csv (+ decision_table.csv)
5) train_models         -> artifacts/models/*.joblib
6) ... (regenerate teammates's stuffs)
"""
import pandas as pd
# from src.config import CFG
# from src.utils.data_manager import read_csv_data, save_processed_data

from pipelines.download_data import main as download_data_main
from pipelines.data_cleaning import build_clean_dataset
from pipelines.process_data import build_processed_dataset
from pipelines.export_segmentation import main as export_segmentation_main
from pipelines.train_models import main as train_models_main

def run_teammate_exports(df: pd.DataFrame) -> None:
    """
    Register teammate exports here.

    Convention:
      builder(df) returns a DataFrame to be saved under data/processed/viz/.
    """
    # Add teammate exports here (when they deliver).
    # Keep this as the ONLY integration point to reduce merge conflicts.
    pass

def main() -> None:
    """
    Run all pipelines.
    """
    print("1) Downloading + validating raw dataset...")
    download_data_main()

    print("2) Building cleaned dataset...")
    _ = build_clean_dataset()

    print("3) Building processed dataset...")
    _ = build_processed_dataset()

    print("4) Exporting segmentation artifacts...")
    export_segmentation_main()

    print("5) Training + saving model pipelines...")
    train_models_main()

    # 3) Optional teammate exports
    # df = read_csv_data(CFG.PROCESSED_BANK_REL)
    # run_teammate_exports(df)

    print("Done. Artifacts are ready for Streamlit.")

if __name__ == "__main__":
    main()