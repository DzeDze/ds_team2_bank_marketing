"""
Batch scoring utilities for the customer ranking model (Logistic Regression pipeline).

Assumes a fitted sklearn estimator/pipeline with predict_proba.
"""

from dataclasses import dataclass
from typing import Optional

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class ScoringOutputs:
    scored_df: pd.DataFrame
    prob_col: str
    decile_col: str


def add_deciles(
    df: pd.DataFrame,
    prob_col: str,
    decile_col: str = "decile",
) -> pd.DataFrame:
    """
    Assign deciles based on predicted probability.

    Decile 10 = highest probability group (top 10%), Decile 1 = lowest.

    Notes:
    - For very small batches (n < 2), deciles are not meaningful; returns NA decile.
    - Uses qcut when possible; falls back to rank-based assignment when ties prevent qcut.
    - Uses pandas nullable integer dtype ("Int64") to safely represent missing deciles.
    """
    out = df.copy()
    n = len(out)

    # Deciles are undefined for a single row
    if n < 2:
        out[decile_col] = pd.Series([pd.NA] * n, dtype="Int64")
        return out

    try:
        # labels False -> 0..k-1 (low->high). Add 1 -> 1..k
        out[decile_col] = pd.qcut(out[prob_col], 10, labels=False, duplicates="drop") + 1
    except Exception:
        # Rank-based fallback (1..10)
        ranks = out[prob_col].rank(method="average", pct=True)
        out[decile_col] = np.ceil(ranks * 10)

    # Ensure numeric, allow NA
    out[decile_col] = pd.to_numeric(out[decile_col], errors="coerce")

    # Make 10 = best (invert within available bins)
    if out[decile_col].notna().any():
        max_bin = int(out[decile_col].max())
        out[decile_col] = (max_bin + 1 - out[decile_col]).round(0)

    # Use nullable int to avoid "Cannot convert NA to int"
    out[decile_col] = out[decile_col].astype("Int64")
    return out


def score_customers(
    pipeline,
    df: pd.DataFrame,
    id_col: Optional[str] = None,
    prob_col: str = "prob_subscribe",
    decile_col: str = "decile",
) -> ScoringOutputs:
    """
    Score customers with a fitted pipeline using predict_proba.

    Args:
        pipeline: fitted sklearn estimator or Pipeline supporting predict_proba
        df: input DataFrame containing feature columns
        id_col: optional identifier to keep (e.g., customer_id)
        prob_col: output probability column name
        decile_col: output decile column name

    Returns:
        ScoringOutputs with scored_df including probability + decile.
    """
    X = df.copy()

    # predict_proba -> take positive class
    proba = pipeline.predict_proba(X)[:, 1]
    scored = df.copy()
    scored[prob_col] = proba

    scored = add_deciles(scored, prob_col=prob_col, decile_col=decile_col)
    scored = scored.sort_values(prob_col, ascending=False).reset_index(drop=True)

    # Move ID col to front if provided
    if id_col and id_col in scored.columns:
        cols = [id_col] + [c for c in scored.columns if c != id_col]
        scored = scored[cols]

    return ScoringOutputs(scored_df=scored, prob_col=prob_col, decile_col=decile_col)


def expected_conversions(scored_df: pd.DataFrame, prob_col: str) -> float:
    """
    Expected conversions = sum of predicted probabilities.

    Args:
        scored_df: scored DataFrame
        prob_col: probability column

    Returns:
        Expected conversions (float)
    """
    return float(scored_df[prob_col].sum())