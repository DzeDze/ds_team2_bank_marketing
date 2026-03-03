"""
Reusable preprocessing helpers.
"""
import pandas as pd

def ensure_target_numeric(df: pd.DataFrame, target_col: str = "y") -> pd.DataFrame:
    """
    Ensure target is numeric 0/1.
    """
    if target_col not in df.columns:
        raise ValueError(f"Missing target column: {target_col}")

    out = df.copy()

    if out[target_col].dtype == "object":
        out[target_col] = out[target_col].map({"yes": 1, "no": 0})
        
    out[target_col] = out[target_col].astype(int)
    return out