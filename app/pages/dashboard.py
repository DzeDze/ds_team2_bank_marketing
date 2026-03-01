from __future__ import annotations

import os
from typing import Tuple

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ----------------------------
# Config / Constants
# ----------------------------
DATA_FILE = "segmentation_data.csv"
PROCESSED_DATA_FILE = "processed_bank_full.csv"

SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, "..", "..", "data"))
VIZ_DATA_DIR = os.path.join(DATA_DIR, "processed", "viz")
PROCESSED_DATA_DIR  = os.path.join(DATA_DIR, "processed")

TARGET_LIFT = 1.50   # target threshold
AVOID_LIFT = 0.70    # avoid threshold

# ----------------------------
# Data loading
# ----------------------------
@st.cache_data(show_spinner=False)
def load_segmentation_results(csv_path: str) -> pd.DataFrame:
    """
    Load segmentation results saved by the segmentation pipeline.

    Parameters
    ----------
    csv_path : str
        Full path to the segmentation CSV (expected under data/processed/viz/).

    Returns
    -------
    pd.DataFrame
        Segmentation results table containing at minimum:
        ['segment_type', 'segment', 'n', 'pct_customers', 'conv', 'lift'].
    """
    df = pd.read_csv(csv_path, sep=",")
    required = {"segment_type", "segment", "n", "pct_customers", "conv", "lift"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Segmentation CSV missing required columns: {sorted(missing)}")
    return df

def load_data_for_baseline(csv_path: str) -> pd.DataFrame:
    """
    Load data for baseline calc.

    Parameters
    ----------
    csv_path : str
        Full path to the processed CSV (expected under data/processed/).

    Returns
    -------
    pd.DataFrame
        Segmentation results table containing at minimum:
        ['segment_type', 'segment', 'n', 'pct_customers', 'conv', 'lift'].
    """
    
    print("Reading CSV data...")
    df = pd.read_csv(csv_path, sep=",")
    print(f"Successfully read {csv_path}")
    print(f"{len(df)} rows, {len(df.columns)} columns")
    return df

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

# ----------------------------
# Business logic
# ----------------------------
def filter_target_segments(df: pd.DataFrame, lift_threshold: float = TARGET_LIFT) -> pd.DataFrame:
    """
    Filter segments with lift above target threshold and sort by priority.

    Returns
    -------
    pd.DataFrame
        Target segments sorted by (lift desc, pct_customers desc).
    """
    return (
        df.loc[df["lift"] >= lift_threshold]
        .sort_values(["lift", "pct_customers"], ascending=[False, False])
        .reset_index(drop=True)
    )

def filter_avoid_segments(df: pd.DataFrame, lift_threshold: float = AVOID_LIFT) -> pd.DataFrame:
    """
    Filter segments with lift below avoid threshold and sort by priority.

    Returns
    -------
    pd.DataFrame
        Avoid segments sorted by (lift asc, pct_customers desc).
    """
    return (
        df.loc[df["lift"] <= lift_threshold]
        .sort_values(["lift", "pct_customers"], ascending=[True, False])
        .reset_index(drop=True)
    )

def build_decision_table(targets: pd.DataFrame, avoids: pd.DataFrame, top_n: int) -> pd.DataFrame:
    """
    Build a combined decision table of top target and avoid segments.

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
    targets_display = targets.head(top_n).copy()
    targets_display["class"] = "Target"

    avoids_display = avoids.head(top_n).copy()
    avoids_display["class"] = "Avoid"

    return pd.concat([targets_display, avoids_display], ignore_index=True)

# ----------------------------
# Visuals
# ----------------------------
def _add_baseline_annotation(fig: go.Figure, baseline: float, y: float = 1.12) -> None:
    """Add a baseline annotation above a Plotly figure."""
    fig.add_annotation(
        text=(
            f"Baseline conversion rate = {baseline:.3f}  |  "
            "Lift = segment conversion ÷ baseline conversion"
        ),
        x=0,
        y=y,
        xref="paper",
        yref="paper",
        showarrow=False,
        align="left",
    )

def plot_segments_bar(
    seg_df: pd.DataFrame,
    baseline: float,
    title: str,
    top_n: int,
    sort_ascending: bool,
) -> go.Figure:
    """
    Create a horizontal bar chart for top segments by lift.

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
    sort_ascending : bool
        Whether to sort by lift ascending (True for Avoid, False for Target).

    Returns
    -------
    go.Figure
        Plotly bar chart.
    """
    top = seg_df.head(top_n).copy()
    top["label"] = top["segment_type"].astype(str) + " | " + top["segment"].astype(str)

    top = top.sort_values("lift", ascending=sort_ascending)

    fig = px.bar(
        top,
        x="lift",
        y="label",
        orientation="h",
        title=title,
    )
    _add_baseline_annotation(fig, baseline)
    fig.add_vline(x=1.0, line_dash="dot")
    fig.update_layout(xaxis_title="Lift vs baseline", yaxis_title="", margin=dict(t=90))
    return fig

def plot_decision_table(decision_table: pd.DataFrame, baseline: float) -> go.Figure:
    """
    Render the decision table as a Plotly Table.

    Parameters
    ----------
    decision_table : pd.DataFrame
        Combined decision table containing both Target and Avoid rows.
    baseline : float
        Baseline conversion rate used in the lift definition.

    Returns
    -------
    go.Figure
        Plotly Table figure.
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
                        decision_table["segment_type"],
                        decision_table["segment"],
                        decision_table["class"],
                        decision_table["pct_customers"].round(2),
                        decision_table["conv"].round(3),
                        decision_table["lift"].round(2),
                    ],
                    align="left",
                ),
            )
        ]
    )

    fig.update_layout(
        title="Decision Table: Target and Avoid Segments",
        margin=dict(t=120),
    )

    fig.add_annotation(
        text=(
            f"Baseline conversion rate = {baseline:.3f}  |  "
            "% customers = segment size ÷ total customers  |  "
            "Lift = segment conversion ÷ baseline conversion"
        ),
        x=0,
        y=1.12,
        xref="paper",
        yref="paper",
        showarrow=False,
        align="left",
    )

    return fig

def visualize_target_segments(targets: pd.DataFrame, baseline: float) -> go.Figure:
    top_targets_vis = targets.head(12).copy()
    top_targets_vis["label"] = top_targets_vis["segment_type"] + " | " + top_targets_vis["segment"]

    fig = px.bar(
        top_targets_vis.sort_values("lift"),
        x="lift",
        y="label",
        orientation="h",
        title="Top Target Segments (ranked by lift)",
    )

    # Baseline annotation (appears once above table)
    fig.add_annotation(
        text=(
            f"Baseline conversion rate = {baseline:.3f}  |  "
            "Lift = segment conversion ÷ baseline conversion"
        ),
        x=0,
        y=1.12,
        xref="paper",
        yref="paper",
        showarrow=False,
        align="left"
    )
    fig.add_vline(x=1.0, line_dash="dot")
    fig.update_layout(xaxis_title="Lift vs baseline", yaxis_title="")
    return fig

def visualize_avoid_segments(avoids: pd.DataFrame, baseline: float) -> go.Figure:
    top_avoids_vis = avoids.head(12).copy()
    top_avoids_vis["label"] = top_avoids_vis["segment_type"] + " | " + top_avoids_vis["segment"]

    fig = px.bar(
        top_avoids_vis.sort_values("lift"),
        x="lift",
        y="label",
        orientation="h",
        title="Segments to Avoid (ranked by lift)",
    )
    # Baseline annotation (appears once above table)
    fig.add_annotation(
        text=(
            f"Baseline conversion rate = {baseline:.3f}  |  "
            "Lift = segment conversion ÷ baseline conversion"
        ),
        x=0,
        y=1.12,
        xref="paper",
        yref="paper",
        showarrow=False,
        align="left"
    )
    fig.add_vline(x=1.0, line_dash="dot")
    fig.update_layout(xaxis_title="Lift vs baseline", yaxis_title="")

# ----------------------------
# Streamlit app
# ----------------------------
def main() -> None:
    """Run the Streamlit dashboard."""
    st.set_page_config(page_title="Segmentation Dashboard", layout="wide")
    st.title("Segmentation Dashboard")

    csv_path = os.path.join(VIZ_DATA_DIR, DATA_FILE)
    df = load_segmentation_results(csv_path)

    # Controls
    st.sidebar.header("Controls")
    visible_n = st.sidebar.selectbox(
        "Number of visible segments (per class)",
        options=list(range(5, 21)),
        index=5,  # default = 10
        help="Controls how many Target segments and how many Avoid segments are shown.",
    )
    path = os.path.join(PROCESSED_DATA_DIR, PROCESSED_DATA_FILE)
    baseline_df = load_data_for_baseline(path)
    baseline = calc_baseline_conversion_rate(baseline_df)

    targets = filter_target_segments(df, TARGET_LIFT)
    avoids = filter_avoid_segments(df, AVOID_LIFT)

    # Top row charts
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Target Segments")
        st.plotly_chart(
            plot_segments_bar(
                targets,
                baseline=baseline,
                title="Top Target Segments (ranked by lift)",
                top_n=visible_n,
                sort_ascending=True,  # for horizontal bar readability (low->high)
            ),
            use_container_width=True,
        )

    with col_right:
        st.subheader("Avoid Segments")
        st.plotly_chart(
            plot_segments_bar(
                avoids,
                baseline=baseline,
                title="Segments to Avoid (ranked by lift)",
                top_n=visible_n,
                sort_ascending=True,  # low->high
            ),
            use_container_width=True,
        )

    # Decision table
    st.markdown("---")
    st.subheader("Decision Table")
    decision_tbl = build_decision_table(targets, avoids, top_n=visible_n)

    st.plotly_chart(
        plot_decision_table(decision_tbl, baseline=baseline),
        use_container_width=True,
    )

    # Optional: also show raw dataframe (handy for debugging)
    with st.expander("Show underlying data"):
        st.dataframe(df, use_container_width=True)


if __name__ == "__main__":
    main()