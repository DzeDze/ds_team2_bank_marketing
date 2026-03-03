"""
Artifact loading utilities: data + models.
"""

from pathlib import Path
from typing import Any

import joblib
import pandas as pd

import streamlit as st

def _load_csv(path: Path) -> pd.DataFrame:
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

def _load_joblib(path: Path) -> Any:
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

@st.cache_data(show_spinner=False)
def load_segmentation_df(segmentation_csv: Path) -> pd.DataFrame:
    """Load segmentation results CSV."""
    return _load_csv(segmentation_csv)


@st.cache_resource(show_spinner=False)
def load_dt_pipeline(dt_pipeline_joblib: Path) -> Any:
    """Load Decision Tree pipeline (joblib)."""
    return _load_joblib(dt_pipeline_joblib)


@st.cache_resource(show_spinner=False)
def load_lr_pipeline(lr_pipeline_joblib: Path) -> Any:
    """Load Logistic Regression pipeline (joblib)."""
    return _load_joblib(lr_pipeline_joblib)