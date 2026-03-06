"""
src/pipelines/export_segmentation.py

Generates segmentation artifacts under data/processed/viz/.

Outputs:
- viz/segmentation_data.csv  (two-way segments with lift + class + baseline_conv)
- viz/decision_table.csv     (top targets + top avoids)
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple

import pandas as pd

from config import CFG
from utils.data_manager import read_csv_data, save_processed_data
from utils.preprocessing import ensure_target_numeric

@dataclass(frozen=True)
class SegmentationExportConfig:
    """
    Config for segmentation exports.
    """
    min_n: int = CFG.MIN_SEGMENT_N
    target_lift: float = CFG.TARGET_LIFT
    avoid_lift: float = CFG.AVOID_LIFT
    target_col: str = CFG.TARGET_COL

def calc_baseline_conversion_rate(df: pd.DataFrame, target_col: str = "y") -> float:
    """
    Compute the baseline conversion rate for the full dataset.

    Parameters
    ----------
    df : pd.DataFrame
        Dataset containing the target column.
    target_col : str, default="y"
        Name of the target column. Assumes values are either:
        - binary numeric (0/1), or
        - strings like {"yes","no"}.

    Returns
    -------
    float
        Baseline conversion rate rounded to 4 decimals.
    """
    if target_col not in df.columns:
        raise ValueError(f"Column '{target_col}' is required to compute baseline conversion rate.")

    y = df[target_col]

    # Handle common bank dataset format: "yes"/"no"
    if y.dtype == "object":
        y = y.map({"yes": 1, "no": 0})

    baseline = y.mean()
    return round(float(baseline), 4)

def evaluate_segments_full(
        data: pd.DataFrame, 
        group_vars: List[str], 
        baseline: float,
        min_size=int,
        target_col: str = "y"
) -> pd.DataFrame:
    """Compute segment size, conversion, lift, and % customers on the full dataset.

    Parameters
    ----------
    data : pd.DataFrame
        Full dataset containing the target column.
    group_vars : list[str]
        Columns used to define segments (e.g., ["age_bucket", "loan"]).
    baseline : float
        Baseline conversion rate on the full dataset.
    min_size : int, default=MIN_N
        Minimum number of observations required for a segment to be included.
    target_col : str, default="y"
        Name of the target column.

    Returns
    -------
    pd.DataFrame
        Segment table with: n, conv, lift, pct_customers.
    """

    missing = [c for c in [*group_vars, target_col] if c not in data.columns]
    if missing:
        raise ValueError(f"Missing required column(s): {missing}")

    seg = (
        data.groupby(group_vars, observed=True)
        .agg(
            n=(target_col, "size"),
            conv=(target_col, "mean")
        )
        .reset_index()
    )

    seg["lift"] = seg["conv"] / baseline
    seg["pct_customers"] = seg["n"] / len(data) * 100

    # Minimum-size filter for reliability
    seg = seg.loc[seg["n"] >= min_size].copy()

    return seg.sort_values("lift", ascending=False)
    
def create_two_way_segmentation_table(
        df: pd.DataFrame, 
        two_way_vars: List[Tuple[str, str]], 
        baseline: float, 
        min_size: int,
        target_col: str
) -> pd.DataFrame:
    """
    Create a combined two-way segmentation table for multiple variable pairs.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataset.
    two_way_vars : list[tuple[str, str]]
        List of column pairs to segment by, e.g. [("age_bucket","loan"), ...].
    baseline : float
        Baseline conversion rate used for lift calculation.
    min_size : int
        Minimum segment size threshold.

    Returns
    -------
    pd.DataFrame
        Stacked segmentation results with columns:
        segment_type, segment, n, pct_customers, conv, lift
    """

    if not two_way_vars:
        raise ValueError("two_way_vars is empty. Provide at least one (var_a, var_b) pair.")
    
    tables: list[pd.DataFrame] = []

    for a, b in two_way_vars:
        seg = evaluate_segments_full(df, [a, b], baseline, min_size=min_size)

        seg["segment"] = seg[a].astype(str) + " & " + seg[b].astype(str)
        seg["segment_type"] = f"{a} x {b}"

        tables.append(seg[["segment_type", "segment", "n", "pct_customers", "conv", "lift"]])

    return pd.concat(tables, ignore_index=True)

def add_class_labels(seg_df: pd.DataFrame, target_lift: float, avoid_lift: float) -> pd.DataFrame:
    """
    Add decision class labels for dashboard: Target / Neutral / Avoid.
    """
    out = seg_df.copy()
    out["class"] = "Neutral"
    out.loc[out["lift"] >= target_lift, "class"] = "Target"
    out.loc[out["lift"] <= avoid_lift, "class"] = "Avoid"
    return out

def build_decision_table(seg_df: pd.DataFrame, top_n: int = 12) -> pd.DataFrame:
    """
    Build a compact decision table with top targets and top avoids.
    """
    targets = (
        seg_df[seg_df["class"] == "Target"]
        .sort_values(["lift", "pct_customers"], ascending=[False, False])
        .head(top_n)
        .copy()
    )
    avoids = (
        seg_df[seg_df["class"] == "Avoid"]
        .sort_values(["lift", "pct_customers"], ascending=[True, False])
        .head(top_n)
        .copy()
    )
    return pd.concat([targets, avoids], ignore_index=True)

def main(cfg: SegmentationExportConfig = SegmentationExportConfig()):
    """
    Load engineered dataset, compute two-way segments, and export viz CSVs.
    """
    df = read_csv_data(CFG.PROCESSED_DATA_REL + "/" + CFG.PROCESSED_BANK_REL)
    df = ensure_target_numeric(df, cfg.target_col)

    baseline = calc_baseline_conversion_rate(df, cfg.target_col)

    two_way_tests = [
        ("age_bucket", "loan"),
        ("age_bucket", "housing"),
        ("loan", "housing"),
        ("balance_bucket", "loan"),
        ("balance_bucket", "housing"),
        ("balance_bucket", "age_bucket"),
        ("job", "loan"),
        ("job", "housing"),
        ("marital", "loan"),
        ("marital", "housing"),
        ("education", "job"),
        ("education", "loan"),
        ("age_bucket", "marital"),
        ("age_bucket", "job"),
        ("balance_bucket", "job"),
        ("balance_bucket", "marital"),
    ]

    seg = create_two_way_segmentation_table(
        df,
        two_way_tests,
        baseline,
        min_size=cfg.min_n,
        target_col=cfg.target_col,
    )

    seg = add_class_labels(seg, target_lift=cfg.target_lift, avoid_lift=cfg.avoid_lift)

    # Make Streamlit read-only: include baseline in exported table
    seg["baseline_conv"] = baseline

    decision_tbl = build_decision_table(seg, top_n=10)

    save_processed_data(CFG.SEGMENTATION_VIZ_REL, seg)
    save_processed_data(CFG.DECISION_TABLE_VIZ_REL, decision_tbl)

if __name__ == "__main__":
    main()