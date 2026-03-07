"""
Customer Targeting dashboard page.

- CSV upload
- Batch scoring with predict_proba
- Deciles + charts + ranked table
- Download scored CSV
- Single-customer sandbox
"""

from __future__ import annotations

import streamlit as st
import pandas as pd

from config import CFG
from app_utils.artifacts import load_lr_pipeline
from app_utils.validation import validate_columns
from app_utils.scoring import score_customers, expected_conversions
from sidebar import render_sidebar
# from viz.charts import fig_probability_histogram, fig_decile_bar

st.set_page_config(page_title="Customer Targeting", layout="wide")
render_sidebar()
st.title("🎯 Customer Targeting Tool")


# -----------------------------
# Load Model
# -----------------------------
@st.cache_resource(show_spinner=False)
def _load_pipeline():
    return load_lr_pipeline(CFG.LR_PIPELINE_JOBLIB)


pipeline = _load_pipeline()
if pipeline is None:
    st.error(
        f"LR pipeline not found at {CFG.LR_PIPELINE_JOBLIB}. "
        "Train + export it via src pipeline and ensure app/config.py path is correct."
    )
    st.stop()

required_cols = list(CFG.LR_MODEL_FEATURES)


# -----------------------------
# Tab Rendering Functions
# -----------------------------
def render_batch_tab():
    st.subheader("1) Upload CSV")
    uploaded = st.file_uploader("Upload a CSV file", type=["csv"])

    if uploaded is None:
        st.info("Upload a CSV to begin scoring. You can still use the sandbox tab.")
        return

    df = pd.read_csv(uploaded)
    st.write("Preview:")
    st.dataframe(df.head(20), use_container_width=True)

    st.subheader("2) Validate schema")

    vr = validate_columns(df, required_cols)
    if not vr.ok:
        st.error("Missing required columns:")
        st.write(vr.missing)
        return

    st.success("Schema looks good.")
    if vr.extra:
        st.caption(f"Extra columns will be ignored: {vr.extra[:20]}")

    st.subheader("3) Score & rank")

    # id_col = st.selectbox(
    #     "Optional ID column (for easier export)",
    #     options=["(none)"] + list(df.columns),
    #     index=0,
    # )
    # id_col_val = None if id_col == "(none)" else id_col

    top_n = st.number_input(
        "Show top N customers",
        min_value=10,
        max_value=5000,
        value=CFG.DEFAULT_TOP_N,
        step=10,
    )

    cutoff = st.slider(
        # Probability cutoff (filter), only show customers whose predicted probability is ≥ this threshold.
        "Probability cutoff (filter)",
        min_value=0.0,
        max_value=1.0,
        value=CFG.DEFAULT_CUTOFF,
        step=0.01,
    )

    try:
        X = df[required_cols].copy()

        outputs = score_customers(
            pipeline=pipeline,
            df=X,
            id_col=None,
        )

        scored = outputs.scored_df
        prob_col = outputs.prob_col
        # decile_col = outputs.decile_col

        # KPIs
        colA, colB, colC = st.columns(3)
        colA.metric("Customers uploaded", f"{len(scored):,}")
        colB.metric("Expected conversions (Σ prob)", f"{expected_conversions(scored, prob_col):.1f}")
        colC.metric(f"Customers with prob ≥ {cutoff:.2f}", f"{(scored[prob_col] >= cutoff).sum():,}")

        # # Charts
        # c1, c2 = st.columns(2)
        # with c1:
        #     st.plotly_chart(
        #         fig_decile_bar(scored, decile_col=decile_col, prob_col=prob_col),
        #         use_container_width=True,
        #     )
        # with c2:
        #     st.plotly_chart(
        #         fig_probability_histogram(scored, prob_col=prob_col),
        #         use_container_width=True,
        #     )

        # Ranked list
        st.subheader("Ranked target list")
        filtered = scored[scored[prob_col] >= cutoff].head(int(top_n))
        st.dataframe(filtered, use_container_width=True)

        # Download
        st.subheader("Download")
        csv_bytes = scored.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download scored CSV",
            data=csv_bytes,
            file_name="scored_customers.csv",
            mime="text/csv",
        )

    except Exception as e:
        st.error(f"Scoring failed: {e}")

def likelihood_band(prob: float) -> tuple[str, str]:
    """
    Map predicted probability to a simple band + action.

    Bands are intentionally simple for demos; adjust thresholds as needed.
    """
    if prob < 0.10:
        return "Low likelihood", "Deprioritize for high-cost channels; include only in low-cost/nurture."
    if prob < 0.20:
        return "Moderate likelihood", "Good test audience; use targeted messaging and measure lift."
    return "High likelihood", "Prioritize outreach; allocate higher-touch channels and personalization."

def render_sandbox_tab():
    st.subheader("Single-customer sandbox")
    st.caption("Useful for demos. For real activation, use CSV upload.")

    inputs: dict[str, str] = {}
    cols = st.columns(3)

    for i, col_name in enumerate(required_cols):
        with cols[i % 3]:

            if col_name == "age_bucket":
                inputs[col_name] = st.selectbox(col_name, CFG.AGE_BUCKET_OPTIONS)

            elif col_name == "balance_bucket":
                inputs[col_name] = st.selectbox(col_name, CFG.BALANCE_BUCKET_OPTIONS)

            elif col_name == "job":
                inputs[col_name] = st.selectbox(col_name, CFG.JOB_OPTIONS)

            elif col_name == "marital":
                inputs[col_name] = st.selectbox(col_name, CFG.MARITAL_OPTIONS)

            elif col_name == "education":
                inputs[col_name] = st.selectbox(col_name, CFG.EDUCATION_OPTIONS)

            elif col_name == "default":
                inputs[col_name] = st.selectbox(col_name, CFG.DEFAULT_OPTIONS)

            elif col_name == "housing":
                inputs[col_name] = st.selectbox(col_name, CFG.HOUSING_OPTIONS)

            elif col_name == "loan":
                inputs[col_name] = st.selectbox(col_name, CFG.LOAN_OPTIONS)

            else:
                inputs[col_name] = st.text_input(col_name, value="")

    one = pd.DataFrame([inputs])

    if st.button("Score this customer"):
        try:
            #  Rrediction
            prob = float(pipeline.predict_proba(one)[:, 1][0])
            band, action = likelihood_band(prob)

            col1, col2 = st.columns([1, 2])
            with col1:
                st.metric("Predicted conversion chance", f"{prob*100:.1f}%")
            with col2:
                st.metric("Likelihood band", band)

            st.markdown(f"**Suggested action:** {action}")
            st.caption("Note: This is a model estimate based on historical patterns, not a guarantee for an individual.")
        except Exception as e:
            st.error(f"Could not score single row: {e}")


# -----------------------------
# Tabs
# -----------------------------
tab1, tab2 = st.tabs(["Batch scoring (CSV upload)", "Single-customer sandbox"])

with tab1:
    render_batch_tab()

with tab2:
    render_sandbox_tab()