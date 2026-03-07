"""
app/components/segmentation_chart.py

Segmentation visualization component:
- Loads segmentation results and processed baseline dataset.
- Computes baseline conversion rate.
- Filters Target/Avoid segments.
- Builds Plotly figures.

Design principle:
- This module returns Figures/DataFrames.
- The page (`app/pages/dashboard.py`) owns layout and user controls.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Tuple, Optional

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ----------------------------
# Defaults / constants
# ----------------------------
DEFAULT_SEGMENTATION_DATA_FILE = "segmentation_data.csv"
DEFAULT_PROCESSED_DATA_FILE = "processed_bank_full.csv"

DEFAULT_TARGET_LIFT = 1.5 # targer lift threshold
DEFAULT_AVOID_LIFT = 0.7 # avoid lift threshold
DEFAULT_TARGET_COL = "y"

def _project_root() -> Path:
    """
    Resolve project root based on this file location.

    Expected repository structure:
      <root>/
        app/components/segmentation_chart.py
        data/processed/viz/segmentation_data.csv
        data/processed/processed_bank_full.csv
    """
    # segmentation_chart.py -> components -> app -> root
    return Path(__file__).resolve().parents[2]

def segmentation_csv_path(filename: str = DEFAULT_SEGMENTATION_DATA_FILE) -> Path:
    """Return the default path to the segmentation results CSV."""
    return _project_root() / "data" / "processed" / "viz" / filename

def processed_csv_path(filename: str = DEFAULT_PROCESSED_DATA_FILE) -> Path:
    """Return the default path to the processed dataset used for baseline conversion."""
    return _project_root() / "data" / "processed" / filename

@st.cache_data(show_spinner=False)
def load_segmentation_results(csv_path: str) -> pd.DataFrame:
    """
    Load segmentation results CSV (cached).

    Required columns:
      - segment_type
      - segment
      - n
      - pct_customers
      - conv
      - lift
    """
    df = pd.read_csv(csv_path)
    required = {"segment_type", "segment", "n", "pct_customers", "conv", "lift"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Segmentation CSV missing required columns: {sorted(missing)}")
    return df

@st.cache_data(show_spinner=False)
def load_processed_data(csv_path: str) -> pd.DataFrame:
    """Load processed dataset CSV (cached)."""
    return pd.read_csv(csv_path)

def calc_baseline_conversion_rate(df: pd.DataFrame, target_col: str = DEFAULT_TARGET_COL) -> float:
    """
    Compute baseline conversion rate from a full dataset.

    Supports:
      - numeric targets in {0, 1}
      - string targets in {"yes", "no"}

    Returns:
      Baseline conversion rate rounded to 4 decimals.
    """
    if target_col not in df.columns:
        raise ValueError(f"Column '{target_col}' is required to compute baseline conversion rate.")

    y = df[target_col]
    if y.dtype == "object":
        y = y.map({"yes": 1, "no": 0})

    baseline = float(y.mean())
    return round(baseline, 4)

def infer_baseline_from_segmentation(seg_df: pd.DataFrame) -> Optional[float]:
    """
    If segmentation export included baseline_conv, use it.
    """
    if "baseline_conv" not in seg_df.columns:
        return None
    try:
        return float(seg_df["baseline_conv"].iloc[0])
    except Exception:
        return None

def filter_target_segments(df: pd.DataFrame, lift_threshold: float) -> pd.DataFrame:
    """
    Filter segments that meet the target threshold.

    Returns:
      DataFrame sorted by lift desc, then pct_customers desc.
    """
    return (
        df.loc[df["lift"] >= lift_threshold]
        .sort_values(["lift", "pct_customers"], ascending=[False, False])
        .reset_index(drop=True)
    )

def filter_avoid_segments(df: pd.DataFrame, lift_threshold: float) -> pd.DataFrame:
    """
    Filter segments considered "avoid" (below threshold).

    Returns:
      DataFrame sorted by lift asc, then pct_customers desc.
    """
    return (
        df.loc[df["lift"] <= lift_threshold]
        .sort_values(["lift", "pct_customers"], ascending=[True, False])
        .reset_index(drop=True)
    )

def build_decision_table(targets: pd.DataFrame, avoids: pd.DataFrame, top_n: int) -> pd.DataFrame:
    """
    Combine top-N Target and top-N Avoid segments into a single decision table.

    Output includes a 'class' column with values 'Target' or 'Avoid'.

    Parameters
        ----------
        targets : pd.DataFrame
            Target segments table.
        avoids : pd.DataFrame
            Avoid segments table.
        top_n : int
            Number of segments to include per class (Target/Avoid).

        Returns
        -------
        pd.DataFrame
            Decision table with a 'class' column and top N rows for each class.
        
    """
    t = targets.head(top_n).copy()
    t["class"] = "Target"

    a = avoids.head(top_n).copy()
    a["class"] = "Avoid"

    return pd.concat([t, a], ignore_index=True)

def _add_baseline_annotation(fig: go.Figure, baseline: float, y: float = 1.12) -> None:
    """Add a baseline conversion + lift definition annotation to a figure."""
    fig.add_annotation(
        text=f"Baseline conversion rate = {baseline:.3f}  |  Lift = segment conversion ÷ baseline conversion",
        x=0,
        y=y,
        xref="paper",
        yref="paper",
        showarrow=False,
        align="left",
    )

def fig_segments_bar(
    seg_df: pd.DataFrame,
    baseline: float,
    title: str,
    top_n: int,
) -> go.Figure:
    """
    Build a horizontal bar chart showing segment lift.

    Notes:
      - The caller decides which `seg_df` to pass (targets or avoids).
      - The chart is sorted by lift ascending for readability in horizontal bars.

    Parameters
    ----------
        seg_df : pd.DataFrame
            Segments (already filtered to Target or Avoid).
        baseline : float
            Baseline conversion rate for annotation.
        title : str
            Chart title.
        top_n : int
            Number of segments to display.
    """
    top = seg_df.head(top_n).copy()
    top["label"] = top["segment_type"].astype(str) + " | " + top["segment"].astype(str)
    top = top.sort_values("lift", ascending=True)

    fig = px.bar(top, x="lift", y="label", orientation="h", title=title)
    fig.add_vline(x=1.0, line_dash="dot")
    _add_baseline_annotation(fig, baseline)
    fig.update_traces(marker_color="#2F6F73")
    fig.update_layout(xaxis_title="Lift vs baseline", yaxis_title="", margin=dict(t=90))
    return fig

def fig_decision_table(decision_df: pd.DataFrame, baseline: float) -> go.Figure:
    """
    Build a Plotly Table figure for the decision table.
    """
    fig = go.Figure(
        data=[
            go.Table(
                header=dict(
                    values=[
                        "Segment type",
                        "Segment values",
                        "Class",
                        "% customers",
                        "Segment conv.",
                        "Lift",
                    ],
                    align="left",
                ),
                cells=dict(
                    values=[
                        decision_df["segment_type"],
                        decision_df["segment"],
                        decision_df["class"],
                        decision_df["pct_customers"].round(2),
                        decision_df["conv"].round(3),
                        decision_df["lift"].round(2),
                    ],
                    align="left",
                ),
            )
        ]
    )

    fig.update_layout(title="Decision Table: Target and Avoid Segments", margin=dict(t=120))
    fig.add_annotation(
        text=(
            f"Baseline conversion rate = {baseline:.3f}  |  "
            "% customers = segment size ÷ total customers"
        ),
        x=0,
        y=1.12,
        xref="paper",
        yref="paper",
        showarrow=False,
        align="left",
    )
    return fig

@dataclass(frozen=True)
class SegmentationConfig:
    """
    Config for segmentation visualization.
    """
    target_lift: float = DEFAULT_TARGET_LIFT
    avoid_lift: float = DEFAULT_AVOID_LIFT
    target_col: str = DEFAULT_TARGET_COL
    segmentation_filename: str = DEFAULT_SEGMENTATION_DATA_FILE
    processed_filename: str = DEFAULT_PROCESSED_DATA_FILE  

def load_artifacts(
    config: SegmentationConfig,
) -> Tuple[pd.DataFrame, float, pd.DataFrame, pd.DataFrame]:
    """
    Load all required artifacts for the segmentation dashboard.

    Returns:
      seg_df: full segmentation results
      baseline: baseline conversion rate
      targets: filtered target segments
      avoids: filtered avoid segments
    """
    seg_path = segmentation_csv_path(config.segmentation_filename)
    if not seg_path.exists():
        raise FileNotFoundError(f"Missing segmentation results CSV: {seg_path}")
    
    seg_df = load_segmentation_results(str(seg_path))
    baseline = infer_baseline_from_segmentation(seg_df)
    
    if baseline is None:
        proc_path = processed_csv_path(config.processed_filename)
        if not proc_path.exists():
            raise FileNotFoundError(
                f"Missing processed dataset CSV for baseline fallback: {proc_path}. "
                "Either export baseline_conv in segmentation_data.csv or add processed file."
            )
        proc_df = load_processed_data(str(proc_path))
        baseline = calc_baseline_conversion_rate(proc_df, target_col=config.target_col)

    targets = filter_target_segments(seg_df, config.target_lift)
    avoids = filter_avoid_segments(seg_df, config.avoid_lift)

    return seg_df, baseline, targets, avoids  
