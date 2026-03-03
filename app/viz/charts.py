"""
Plotly chart helpers used across pages.
"""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def fig_probability_histogram(df: pd.DataFrame, prob_col: str) -> go.Figure:
    """
    Histogram of predicted probabilities.
    """
    fig = px.histogram(df, x=prob_col, nbins=30)
    fig.update_layout(
        title="Predicted Probability Distribution",
        xaxis_title="P(subscribe)",
        yaxis_title="Count",
        margin=dict(l=10, r=10, t=50, b=10),
    )
    return fig


def fig_decile_bar(df: pd.DataFrame, decile_col: str, prob_col: str) -> go.Figure:
    """
    Bar chart: average probability by decile (Decile 10 is highest group).
    """
    agg = (
        df.groupby(decile_col, as_index=False)[prob_col]
        .mean()
        .sort_values(decile_col, ascending=False)
    )
    fig = px.bar(agg, x=decile_col, y=prob_col)
    fig.update_layout(
        title="Average Predicted Probability by Decile (10 = highest)",
        xaxis_title="Decile",
        yaxis_title=f"Avg {prob_col}",
        margin=dict(l=10, r=10, t=50, b=10),
    )
    return fig


def fig_decision_map(
    seg_df: pd.DataFrame,
    x_col: str = "pct_customers",
    y_col: str = "lift",
    size_col: str = "n_customers",
    color_col: str = "decision",
    hover_name: str = "segment",
) -> go.Figure:
    """
    Bubble chart decision map (size vs lift trade-off).

    Expects seg_df to contain columns like:
      segment, lift, n_customers, pct_customers, decision
    """
    fig = px.scatter(
        seg_df,
        x=x_col,
        y=y_col,
        size=size_col,
        color=color_col,
        hover_name=hover_name,
    )
    fig.update_layout(
        title="Decision Map (Size vs Lift)",
        xaxis_title="Share of Customers",
        yaxis_title="Lift vs Baseline",
        margin=dict(l=10, r=10, t=50, b=10),
    )
    return fig