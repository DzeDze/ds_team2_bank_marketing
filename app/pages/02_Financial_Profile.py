import pandas as pd
import streamlit as st
import plotly.express as px
from sidebar import render_sidebar

st.set_page_config(page_title="Customer Financial Profile", layout="wide")
render_sidebar()
st.title("Customer Financial Profile and Conversion Drivers")

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("data/raw/bank-full.csv", sep=";")
    df["converted"] = df["y"].map({"yes": 1, "no": 0})
    return df

df = load_data()


# =========================================================
# ANALYSIS 1: Does a higher customer account balance increase the likelihood of subscription?
# =========================================================

from plotly.subplots import make_subplots
import plotly.graph_objects as go

# Create balance segments
df["balance_segment"] = pd.qcut(
    df["balance"],
    q=4,
    labels=["Lower Balance", "Lower-Mid Balance", "Upper-Mid Balance", "Higher Balance"],
    duplicates="drop"
)

summary = (
    df.groupby("balance_segment", observed=True)
    .agg(
        n_customers=("converted", "size"),
        n_converted=("converted", "sum"),
        conversion_rate=("converted", "mean"),
        avg_balance=("balance", "mean")
    )
    .reset_index()
)

fig = make_subplots(specs=[[{"secondary_y": True}]])

# Conversion rate bars
fig.add_trace(
    go.Bar(
        x=summary["balance_segment"],
        y=summary["conversion_rate"],
        marker_color="#1F4E52",
        hoverinfo="skip"
    ),
    secondary_y=False
)

# Average balance line
fig.add_trace(
    go.Scatter(
        x=summary["balance_segment"],
        y=summary["avg_balance"],
        mode="lines+markers",
        line=dict(color="#5E8F95", width=5),
        marker=dict(size=9),
        customdata=summary[["n_customers","n_converted","avg_balance"]].to_numpy(),
        hovertemplate=
        "Customers in this segment: %{customdata[0]:,}<br>"
        "Customers who subscribed: %{customdata[1]:,}<br>"
        "Average account balance: $%{customdata[2]:,.0f}"
        "<extra></extra>"
    ),
    secondary_y=True
)

fig.update_layout(
    title="Average Account Balance vs Campaign Conversion Rate",
    xaxis_title="Customer Balance Segment",
    showlegend=False,
    plot_bgcolor="white"
)

# Conversion rate axis
fig.update_yaxes(
    title_text="Customer Conversion Rate",
    tickformat=".0%",
    tickmode="linear",
    dtick=0.02,
    showgrid=True,
    gridcolor="#E5E7EB",
    secondary_y=False
)

# Balance axis
fig.update_yaxes(
    title_text="Average Account Balance ($)",
    tickprefix="$",
    showgrid=False,
    secondary_y=True
)

fig.update_xaxes(showgrid=False)

st.plotly_chart(fig, use_container_width=True)


# =========================================================
# ANALYSIS 2: Does a customer’s existing debt profile affect the likelihood of subscribing?
# =========================================================

st.header("Existing Loan Products and Conversion Impact")

def existing_products(row):
    if row["default"] == "yes":
        return "Credit Default"
    if row["housing"] == "yes" and row["loan"] == "yes":
        return "Housing + Personal Loan"
    if row["housing"] == "yes":
        return "Housing Loan"
    if row["loan"] == "yes":
        return "Personal Loan"
    return "No Loan Products"

df["existing_products"] = df.apply(existing_products, axis=1)

products_summary = (
    df.groupby("existing_products")
    .agg(
        n_customers=("converted","size"),
        n_converted=("converted","sum"),
        conversion_rate=("converted","mean")
    )
    .reset_index()
    .sort_values("conversion_rate")
)

fig2 = px.bar(
    products_summary,
    x="conversion_rate",
    y="existing_products",
    orientation="h",
    text=products_summary["conversion_rate"].map(lambda v: f"{v:.0%}"),
    title="Customer Existing Financial Products vs Conversion Rate"
)

fig2.update_layout(
    xaxis_tickformat=".0%",
    xaxis_title="Customer Conversion Rate",
    yaxis_title="Customer Existing Financial Products"
)

fig2.update_traces(
    marker_color="#2F6F73",
    customdata=products_summary[["n_customers","n_converted"]].to_numpy(),
    hovertemplate=
        "Customers in this group: %{customdata[0]:,}<br>"
        "Customers who subscribed: %{customdata[1]:,}"
        "<extra></extra>"
)

st.plotly_chart(fig2, use_container_width=True)


# =========================================================
# ANALYSIS 3: What financial segments are the highest-value targets for the next campaign?
# =========================================================

st.header("Highest-Value Financial Segments for Targeting")

segment_summary = (
    df.groupby(["balance_segment", "existing_products"], observed=True)
    .agg(
        n_customers=("converted", "size"),
        n_converted=("converted", "sum"),
        conversion_rate=("converted", "mean")
    )
    .reset_index()
)

palette = {
    "Credit Default": "#1F4E52",
    "Housing + Personal Loan": "#2F6F73",
    "Housing Loan": "#5E8F95",
    "Personal Loan": "#8FB3C1",
    "No Loan Products": "#C6D9E2"
}

fig3 = px.bar(
    segment_summary,
    x="balance_segment",
    y="conversion_rate",
    color="existing_products",
    barmode="group",
    color_discrete_map=palette,
    title="Customer Balance Segment and Existing Financial Products vs Conversion Rate",
)

fig3.update_layout(
    yaxis_tickformat=".0%",
    xaxis_title="Customer Balance Segment",
    yaxis_title="Customer Conversion Rate",
    legend_title_text="Customer Existing Financial Products"
)

fig3.update_traces(
    customdata=segment_summary[["n_customers", "n_converted"]].to_numpy(),
    hovertemplate=
        "Customers in this segment: %{customdata[0]:,}<br>"
        "Customers who subscribed: %{customdata[1]:,}"
        "<extra></extra>"
)

st.plotly_chart(fig3, use_container_width=True)

# =========================================================
# 🏁 SUMMARY
# =========================================================

st.header("Summary")
st.markdown(
	"""
	- Financial stability strongly correlates with conversion. Customers with higher account balances are more likely to subscribe, especially when they do not hold loans.
- Conversely, customers with housing or personal loans, and particularly those with credit in default, show much lower subscription rates. Debt status acts as a negative predictor of campaign success.
- Housing loans are far more common than personal loans, indicating many customers have long-term financial commitments. Targeting financially stable, debt-free, high-balance customers could therefore improve overall campaign efficiency.

	"""
)