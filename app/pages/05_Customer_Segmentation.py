"""
app/pages/dashboard.py

Dashboard page:
- Owns Streamlit layout and controls.
- Calls component modules that return Plotly figures / data.
- Each team member add their own `app/components/<module>.py`
- import + place team member charts here.
"""

import streamlit as st
from sidebar import render_sidebar

try:
    from app.components.segmentation_chart import (
        SegmentationConfig,
        build_decision_table,
        fig_decision_table,
        fig_segments_bar,
        load_artifacts,
    )
except ModuleNotFoundError:
    from components.segmentation_chart import (  # type: ignore
        SegmentationConfig,
        build_decision_table,
        fig_decision_table,
        fig_segments_bar,
        load_artifacts,
    )

def _safe_plotly(fig_factory, *args, **kwargs) -> None:
    """
    Render a Plotly figure safely.

    If a chart errors, the page keeps rendering.
    """
    try:
        fig = fig_factory(*args, **kwargs)
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.warning("A chart failed to render (module may be in progress).")
        st.exception(e)

def render_dashboard() -> None:
    """Render the main dashboard page."""
    st.set_page_config(page_title="Customer Segmentation", layout="wide")
    st.title("Customer Segmentation")

    # Sidebar controls (page-level; components remain pure)
    st.sidebar.header("Controls")
    visible_n = st.sidebar.selectbox(
        "Number of visible segments (per class)",
        options=list(range(5, 21)),
        index=12,  # default = 10
    )

    # Load segmentation artifacts
    config = SegmentationConfig()
    try:
        seg_df, baseline, targets, avoids = load_artifacts(config)
    except Exception as e:
        st.error("Failed to load segmentation inputs.")
        st.exception(e)
        st.stop()

    # st.caption(f"Baseline conversion rate = {baseline:.3f}. Lift = segment conversion ÷ baseline conversion.")
    # st.plotly_chart(fig, use_container_width=True)
    # Layout: two charts on top, table below
    col_left, col_right = st.columns(2)

    # with col_left:
    st.subheader("Target Segments")
    _safe_plotly(
            fig_segments_bar,
            targets,
            baseline=baseline,
            title="Top Target Segments (ranked by lift)",
            top_n=visible_n,
        )   

    # with col_right:
    st.subheader("Avoid Segments")
    _safe_plotly(
            fig_segments_bar,
            avoids,
            baseline=baseline,
            title="Segments to Avoid (ranked by lift)",
            top_n=visible_n,
        )

    st.markdown("---")
    st.subheader("Decision Table")
    dec_df = build_decision_table(targets, avoids, top_n=visible_n)
    _safe_plotly(fig_decision_table, dec_df, baseline=baseline)

    with st.expander("Show underlying segmentation data"):
        st.dataframe(seg_df, use_container_width=True)

    # Placeholder: future teammate modules
    st.markdown("---")
render_sidebar()
# Streamlit multipage runs this file directly
render_dashboard()