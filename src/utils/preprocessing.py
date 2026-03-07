"""
Reusable preprocessing helpers.
"""
import pandas as pd

def clean_bank_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply cleaning steps.
    """
    out = df.copy()

    out["job"] = out["job"].str.replace(".", "", regex=False)

    month_order = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
    out["month"] = pd.Categorical(out["month"], categories=month_order, ordered=True)

    return out

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