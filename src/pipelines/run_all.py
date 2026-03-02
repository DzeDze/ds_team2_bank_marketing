"""
src/pipelines/run_all.py

One command to regenerate everything:)
1) engineered dataset
2) segmentation viz exports
3) model artifacts
4) ... (regenerate teammates's stuffs)
"""
import pandas as pd
# from src.config import CFG
# from src.utils.data_manager import read_csv_data, save_processed_data

from src.pipelines.export_segmentation import main as export_segmentation_main
from src.pipelines.train_models import main as train_models_main

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
    # 1) Segmentation exports
    export_segmentation_main()

    # 2) Model artifacts
    train_models_main()

    # 3) Optional teammate exports
    # df = read_csv_data(CFG.PROCESSED_BANK_REL)
    # run_teammate_exports(df)


if __name__ == "__main__":
    main()