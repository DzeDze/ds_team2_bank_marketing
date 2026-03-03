"""
Central configuration for paths and thresholds.
"""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AppConfig:
    # Project root
    ROOT: Path = Path(__file__).resolve().parents[1]

    # Data directories
    DATA_DIR: Path = ROOT / "data"
    VIZ_DATA_DIR: Path = DATA_DIR / "processed" / "viz"
    MODELS_DIR: Path = ROOT / "artifacts" / "models"

    # Artifacts
    SEGMENTATION_DATA_CSV: Path = VIZ_DATA_DIR / "segmentation_data.csv"
    LR_PIPELINE_JOBLIB: Path = MODELS_DIR / "logistic_regression_pipeline.joblib"
    DT_MODEL_JOBLIB: Path = MODELS_DIR / "decision_tree_pipeline.joblib"

    # Thresholds
    TARGET_LIFT: float = 1.5 # targer lift threshold
    AVOID_LIFT: float = 0.7 # avoid lift threshold

    # Defaults
    DEFAULT_TOP_N: int = 200 # Show top N customers in customer targeting page
    DEFAULT_CUTOFF: float = 0.3 # Probability cutoff (filter), only show customers whose predicted probability is ≥ this threshold.

    # Columns available in processed_bank_full.csv
    PROCESSED_COLUMNS = [
        "age","job","marital","education","default","balance","housing","loan","contact","day","month",
        "duration","campaign","pdays","previous","poutcome","y","balance_bucket","age_bucket",
    ]

    # Columns that the LR model expects at inference time (must match training features)
    LR_MODEL_FEATURES = [
        "age_bucket",
        "job",
        "marital",
        "education",
        "default",
        "housing",
        "loan",
        "balance_bucket",
    ]

    # dropdown values for sandbox
    AGE_BUCKET_OPTIONS = ["18-25", "26-35", "36-45", "46-55", "56-65", "65+"]
    BALANCE_BUCKET_OPTIONS = ["negative", "low", "mid", "high"]

    JOB_OPTIONS = [
        "management", "technician", "entrepreneur", "blue-collar",
        "unknown", "retired", "admin.", "services",
        "self-employed", "unemployed", "housemaid", "student"
    ]

    MARITAL_OPTIONS = ["married", "single", "divorced"]

    EDUCATION_OPTIONS = ["tertiary", "secondary", "unknown", "primary"]

    DEFAULT_OPTIONS = ["no", "yes"]

    HOUSING_OPTIONS = ["yes", "no"]

    LOAN_OPTIONS = ["no", "yes"]

CFG = AppConfig()