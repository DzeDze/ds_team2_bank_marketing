"""
Artifact loading utilities: data + models.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

import joblib
import pandas as pd

@dataclass(frozen=True)
class LoadedArtifacts:
    segmentation_df: Optional[pd.DataFrame]
    lr_pipeline: Optional[Any]
    decision_tree: Optional[Any]

def load_csv(path: Path) -> pd.DataFrame:
    """
    Load a CSV from disk.

    Args:
        path: File path.

    Returns:
        DataFrame

    Raises:
        FileNotFoundError: if missing
        ValueError: if empty
    """
    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path}")
    df = pd.read_csv(path)
    if df.empty:
        raise ValueError(f"CSV is empty: {path}")
    return df

def load_joblib(path: Path) -> Any:
    """
    Load a joblib artifact from disk.

    Args:
        path: File path.

    Returns:
        Loaded object.

    Raises:
        FileNotFoundError: if missing
    """
    if not path.exists():
        raise FileNotFoundError(f"Missing artifact: {path}")
    return joblib.load(path)

def try_load_artifacts(
    segmentation_csv: Path,
    lr_pipeline_joblib: Path,
    decision_tree_joblib: Path,
) -> LoadedArtifacts:
    """
    Try to load all artifacts; return None for those not found.

    This lets the UI partially work if some artifacts aren't present yet.

    Returns:
        LoadedArtifacts with optional components.
    """
    segmentation_df = None
    lr_pipeline = None
    decision_tree = None

    try:
        segmentation_df = load_csv(segmentation_csv)
    except Exception:
        segmentation_df = None

    try:
        lr_pipeline = load_joblib(lr_pipeline_joblib)
    except Exception:
        lr_pipeline = None

    try:
        decision_tree = load_joblib(decision_tree_joblib)
    except Exception:
        decision_tree = None

    return LoadedArtifacts(segmentation_df, lr_pipeline, decision_tree)