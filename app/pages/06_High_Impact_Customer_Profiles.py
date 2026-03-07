"""
app/pages/02_High_Impact_Customer_Profiles.py

This page shows:
- KPIs and tables come from the full segmentation results (Target / Neutral / Avoid)
- Optional technical details can be shown under an "Advanced" expander

Data source:
- data/viz/segmentation_data.csv (exported by src/pipelines/export_segmentation.py)
Expected columns:
  segment_type, segment, n, pct_customers, conv, lift, class, baseline_conv
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

import numpy as np
import pandas as pd
import streamlit as st

from config import CFG
from app_utils.artifacts import load_segmentation_df
from sidebar import render_sidebar

st.set_page_config(page_title="High-Impact Customer Profiles", layout="wide")
render_sidebar()

# -------------------------
# Validation
# -------------------------

REQUIRED_COLS = {
    "segment_type",
    "segment",
    "n",
    "pct_customers",
    "conv",
    "lift",
    "class",
    "baseline_conv",
}


def _require_cols(df: pd.DataFrame) -> None:
    missing = REQUIRED_COLS - set(df.columns)
    if missing:
        raise ValueError(f"segmentation_data.csv missing columns: {sorted(missing)}")


def _coerce_types(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["n"] = pd.to_numeric(out["n"], errors="coerce").fillna(0).astype(int)
    out["pct_customers"] = pd.to_numeric(out["pct_customers"], errors="coerce")
    out["conv"] = pd.to_numeric(out["conv"], errors="coerce")
    out["lift"] = pd.to_numeric(out["lift"], errors="coerce")
    out["baseline_conv"] = pd.to_numeric(out["baseline_conv"], errors="coerce")
    out["class"] = out["class"].astype(str)
    out["segment_type"] = out["segment_type"].astype(str)
    out["segment"] = out["segment"].astype(str)
    return out


def _baseline_conv(df: pd.DataFrame) -> float:
    # baseline_conv is repeated per row; take the first non-null
    b = df["baseline_conv"].dropna()
    if b.empty:
        # fallback: weighted average conv across all rows (not ideal if rows overlap)
        denom = df["n"].sum()
        return float((df["n"] * df["conv"]).sum() / denom) if denom else 0.0
    return float(b.iloc[0])


def _weighted_conv(df: pd.DataFrame) -> float:
    denom = df["n"].sum()
    return float((df["n"] * df["conv"]).sum() / denom) if denom else 0.0


@dataclass(frozen=True)
class TierSummary:
    n: int
    pct_customers: float
    avg_conv: float
    avg_lift: float


def _summarize_by_class(df: pd.DataFrame) -> Dict[str, TierSummary]:
    summaries: Dict[str, TierSummary] = {}
    for cls, g in df.groupby("class", dropna=False):
        n = int(g["n"].sum())
        pct = np.nan

        avg_conv = _weighted_conv(g)
        avg_lift = float((g["n"] * g["lift"]).sum() / g["n"].sum()) if g["n"].sum() else np.nan

        summaries[str(cls)] = TierSummary(
            n=n,
            pct_customers=pct,
            avg_conv=avg_conv,
            avg_lift=avg_lift,
        )
    return summaries


def _top_segments(df: pd.DataFrame, cls: str, k: int = 10, min_n: int = 200) -> pd.DataFrame:
    g = df[df["class"] == cls].copy()
    g = g[g["n"] >= min_n]
    g = g.sort_values(["lift", "conv", "n"], ascending=[False, False, False]).head(k)
    return g[
        ["segment_type", "segment", "n", "pct_customers", "conv", "lift", "baseline_conv", "class"]
    ].reset_index(drop=True)

def _fmt_pct_from_ratio(x: float) -> str:
    """
    Format a proportion (e.g. 0.117) as percent string.
    """
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return "—"
    return f"{x*100:.1f}%"


def _fmt_pct_from_percent(x: float) -> str:
    """
    Format a value already in percent units (e.g. 1.65 means 1.65%).
    """
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return "—"
    return f"{x:.1f}%"

def _fmt_x(x: float) -> str:
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return "—"
    return f"{x:.2f}x"


# -------------------------
# Load data
# -------------------------

st.title("High-Impact Customer Profiles")
st.caption(
    "We segment customers into **Target / Neutral / Avoid** profile tiers using two-way customer attributes. "
    "Use this to prioritize marketing investment and reduce waste."
)

try:
    seg_df = load_segmentation_df(CFG.SEGMENTATION_DATA_CSV)
except Exception as e:
    st.error(f"Could not load segmentation data at {CFG.SEGMENTATION_DATA_CSV}\n\nError: {e}")
    st.stop()

try:
    _require_cols(seg_df)
    seg_df = _coerce_types(seg_df)
except Exception as e:
    st.error(f"Segmentation data validation failed.\n\n{e}")
    st.stop()

baseline = _baseline_conv(seg_df)
summaries = _summarize_by_class(seg_df)

# Side controls
st.sidebar.header("Filters")
min_n = st.sidebar.slider("Minimum segment size", min_value=50, max_value=5000, value=200, step=50)
top_k = st.sidebar.slider("Show top segments per tier", min_value=3, max_value=20, value=6, step=1)

# -------------------------
# KPI row
# -------------------------

# Determine "best target" among eligible target segments
target_df = seg_df[seg_df["class"] == "Target"].copy()
target_df = target_df[target_df["n"] >= min_n]
best_target = None
if not target_df.empty:
    best_target = target_df.sort_values(["lift", "conv", "n"], ascending=[False, False, False]).iloc[0]

k1, k2, k3, k4 = st.columns(4)
k1.metric("Baseline conversion (overall)", _fmt_pct_from_ratio(baseline))

if best_target is not None:
    k2.metric("Best Target segment conversion", _fmt_pct_from_ratio(float(best_target["conv"])))
    k3.metric("Best Target lift vs baseline", _fmt_x(float(best_target["lift"])))
    k4.metric("Best Target audience size", f"{int(best_target['n']):,}")
else:
    k2.metric("Best Target segment conversion", "—")
    k3.metric("Best Target lift vs baseline", "—")
    k4.metric("Best Target audience size", "—")

st.divider()

# -------------------------
# Portfolio overview
# -------------------------

st.subheader("Portfolio Overview")
st.caption("A snapshot of where performance concentrates across Target / Neutral / Avoid tiers.")

overview_rows = []
for cls in ["Target", "Neutral", "Avoid"]:
    if cls in summaries:
        s = summaries[cls]
        overview_rows.append(
            {
                "Tier": cls,
                "Customers (sum of segments)": s.n,
                "Avg conversion": s.avg_conv,
                "Avg lift": s.avg_lift,
            }
        )

overview = pd.DataFrame(overview_rows)
if not overview.empty:
    show = overview.copy()
    show["Avg conversion"] = show["Avg conversion"].apply(_fmt_pct_from_ratio)
    show["Avg lift"] = show["Avg lift"].apply(_fmt_x)
    st.dataframe(show, use_container_width=True)
else:
    st.info("No summary rows available. Check your segmentation export.")

st.divider()

# -------------------------
# Tier drill-down tabs
# -------------------------

st.subheader("Top segments by tier")
st.caption("These are the most actionable segments within each tier, ranked by lift and conversion.")

tabs = st.tabs(["Target (invest)", "Neutral (test)", "Avoid (reduce)"])

tier_descriptions = {
    "Target": "Prioritize budget and outreach here (highest lift vs baseline).",
    "Neutral": "Use controlled experiments and smaller spends to validate potential.",
    "Avoid": "Reduce spend / deprioritize; these segments underperform baseline.",
}

for tab, cls in zip(tabs, ["Target", "Neutral", "Avoid"]):
    with tab:
        st.markdown(f"**{tier_descriptions.get(cls, '')}**")

        top = _top_segments(seg_df, cls=cls, k=top_k, min_n=min_n)

        if top.empty:
            st.warning("No segments match the current filter. Try lowering the minimum segment size.")
            continue

        top_show = top.copy()
        top_show["pct_customers"] = top_show["pct_customers"].apply(_fmt_pct_from_percent)
        top_show["conv"] = top_show["conv"].apply(_fmt_pct_from_ratio)
        top_show["lift"] = top_show["lift"].apply(_fmt_x)
        top_show["baseline_conv"] = top_show["baseline_conv"].apply(_fmt_pct_from_ratio)

        st.dataframe(
            top_show.rename(
                columns={
                    "segment_type": "Segment Type",
                    "segment": "Segment",
                    "n": "Customers",
                    "pct_customers": "% Customers",
                    "conv": "Conversion",
                    "lift": "Lift vs baseline",
                    "baseline_conv": "Baseline",
                    "class": "Tier",
                }
            ),
            use_container_width=True,
        )

        st.download_button(
            label=f"Download {cls} segments (CSV)",
            data=top.to_csv(index=False).encode("utf-8"),
            file_name=f"{cls.lower()}_segments.csv",
            mime="text/csv",
        )

st.divider()

# -------------------------
# Recommendations
# -------------------------

st.subheader("Recommended Marketing Actions")
st.markdown(
    f"""
**How to use this segmentation:**
1. **Invest in Target segments** first: focus outreach, budget, and personalization where lift is strongest.
2. **Use Neutral as an experimentation pool**: test new messaging/offers and measure incremental impact.
3. **Deprioritize Avoid**: reduce low-return spend and reallocate effort to higher-performing tiers.

**Baseline conversion used:** {_fmt_pct_from_ratio(baseline)}  
"""
)

# -------------------------
# Optional section
# -------------------------

with st.expander("Advanced (optional): data + assumptions"):
    st.markdown("**Data source:** `segmentation_data.csv` exported by `src/pipelines/export_segmentation.py`.")
    st.write("Raw rows (sample):")
    st.dataframe(seg_df.head(50), use_container_width=True)
