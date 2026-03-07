"""
src/config.py

Central configuration for:
- file locations
- thresholds
- feature contract
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class Config:
    PROJECT_ROOT: Path = Path(__file__).resolve().parents[1]

    PROCESSED_DATA_REL: str = "processed"
    CLEAN_BANK_REL: str = "bank-full-clean.csv"
    # Processed dataset (created by src/features/engineering.py)
    PROCESSED_BANK_REL: str = "bank-full-cleaned-processed-engineered.csv"

    # Viz exports (created by pipelines/export_segmentation.py)
    SEGMENTATION_VIZ_REL: str = "viz/segmentation_data.csv"
    DECISION_TABLE_VIZ_REL: str = "viz/decision_table.csv"

    # Model artifacts
    ARTIFACTS_DIR: Path = PROJECT_ROOT / "artifacts"
    MODELS_DIR: Path = ARTIFACTS_DIR / "models"
    DT_PIPELINE_PATH: Path = MODELS_DIR / "decision_tree_pipeline.joblib"
    LR_PIPELINE_PATH: Path = MODELS_DIR / "logistic_regression_pipeline.joblib"

    # Business thresholds
    TARGET_LIFT: float = 1.5 # targer lift threshold
    AVOID_LIFT: float = 0.7 # avoid lift threshold
    MIN_SEGMENT_N: int = 200 # Minimum number of observations required for a segment to be included.

    # Modeling
    RANDOM_STATE: int = 42
    TEST_SIZE: float = 0.3

    # Feature contract for both DT + LR
    MODEL_FEATURES: tuple[str, ...] = (
        "age_bucket",
        "job",
        "marital",
        "education",
        "default",
        "housing",
        "loan",
        "balance_bucket",
    )

    TARGET_COL: str = "y"


CFG = Config()