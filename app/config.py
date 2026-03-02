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
    MODELS_DIR: Path = ROOT / "models"

    # Artifacts
    SEGMENTATION_DATA_CSV: Path = VIZ_DATA_DIR / "segmentation_data.csv"
    LR_PIPELINE_JOBLIB: Path = MODELS_DIR / "lr_pipeline.joblib"
    DT_MODEL_JOBLIB: Path = MODELS_DIR / "decision_tree.joblib"

    # Thresholds
    TARGET_LIFT: float = 1.5 # targer lift threshold
    AVOID_LIFT: float = 0.7 # avoid lift threshold

    # Defaults
    DEFAULT_TOP_N: int = 200 # Show top N customers in customer targeting page
    DEFAULT_CUTOFF: float = 0.3 # Probability cutoff (filter)


CFG = AppConfig()