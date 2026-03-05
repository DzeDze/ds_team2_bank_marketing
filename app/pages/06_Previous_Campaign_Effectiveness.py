import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Previous Campaign Effectiveness", layout="wide")

st.title("Customer Response Patterns from Previous Campaigns")

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("data/raw/bank-full.csv", sep=";")
    df["converted"] = df["y"].map({"yes": 1, "no": 0})
    return df

df = load_data()


# =========================================================
# ANALYSIS 4: How does the outcome of the previous marketing campaign influence conversion in the current campaign?
# =========================================================

st.header("How Past Campaign Outcomes Influence Customer Conversion")

df["previous_campaign_result"] = df["poutcome"].replace({
    "success": "Previous Campaign Success",
    "failure": "Previous Campaign Failure",
    "unknown": "No Previous Campaign Contact",
    "other": "Outcome Unrecorded"
})

summary_outcome = (
    df.groupby("previous_campaign_result")["converted"]
    .agg(
        n_customers="size",
        n_converted="sum",
        conversion_rate="mean"
    )
    .reset_index()
)

fig1 = px.bar(
    summary_outcome,
    x="conversion_rate",
    y="previous_campaign_result",
    orientation="h",
    text=summary_outcome["conversion_rate"].map(lambda v: f"{v:.0%}"),
    title="Previous Campaign Result vs Conversion Rate"
)

fig1.update_layout(
    xaxis_tickformat=".0%",
    yaxis_title="Previous Campaign Result",
    xaxis_title="Customer Conversion Rate",
)

fig1.update_traces(
    marker_color="#2F6F73",
    customdata=summary_outcome[["n_customers", "n_converted"]].to_numpy(),
    hovertemplate=
        "Customers in this group: %{customdata[0]:,}<br>"
        "Customers who subscribed: %{customdata[1]:,}"
        "<extra></extra>"
)

st.plotly_chart(fig1, use_container_width=True)


# =========================================================
# ANALYSIS 5: Does time since the last marketing contact affect conversion rates?
# =========================================================

st.header("Customer Contact Timing and Conversion Performance")

def contact_recency(days):
    if days == -1:
        return "Never Contacted"
    if days <= 30:
        return "0–30 Days"
    if days <= 90:
        return "31–90 Days"
    return "90+ Days"

df["last_contact_timing"] = df["pdays"].apply(contact_recency)

order = ["0–30 Days", "31–90 Days", "90+ Days", "Never Contacted"]

summary_recency = (
    df.groupby("last_contact_timing")["converted"]
    .agg(
        n_customers="size",
        n_converted="sum",
        conversion_rate="mean"
    )
    .reindex(order)
    .reset_index()
)

fig2 = px.line(
    summary_recency,
    x="last_contact_timing",
    y="conversion_rate",
    markers=True,
    title="Conversion Rate by Time Since Last Customer Contact"
)

fig2.update_layout(
    yaxis_tickformat=".0%",
    xaxis_title="Time Since Last Contact",
    yaxis_title="Customer Conversion Rate"
)

fig2.update_traces(
    line=dict(width=5, color="#1F4E52"),
    marker=dict(size=9, color="#1F4E52"),
    customdata=summary_recency[["n_customers", "n_converted"]].to_numpy(),
    hovertemplate=
        "Customers in this group: %{customdata[0]:,}<br>"
        "Customers who subscribed: %{customdata[1]:,}"
        "<extra></extra>"
)

st.plotly_chart(fig2, use_container_width=True)


# =========================================================
# ANALYSIS 6: Are customers previously contacted in past campaigns more likely to convert than first-time contacts?
# =========================================================

st.header("Conversion Performance: Existing vs First-Time Customers")

df["customer_type"] = df["pdays"].apply(
    lambda x: "New Customer" if x == -1 else "Existing Customer"
)

summary_customer = (
    df.groupby("customer_type")["converted"]
    .agg(
        n_customers="size",
        n_converted="sum",
        conversion_rate="mean"
    )
    .reset_index()
)

fig3 = px.bar(
    summary_customer,
    x="conversion_rate",
    y="customer_type",
    orientation="h",
    text=summary_customer["conversion_rate"].map(lambda v: f"{v:.0%}"),
    title="Existing vs New Customers Conversion Rate"
)

fig3.update_layout(
    xaxis_tickformat=".0%",
    yaxis_title="Customer Type",
    xaxis_title="Customer Conversion Rate"
)

fig3.update_traces(
    marker_color="#2F6F73",
    customdata=summary_customer[["n_customers", "n_converted"]].to_numpy(),
    hovertemplate=
        "Customers in this group: %{customdata[0]:,}<br>"
        "Customers who subscribed: %{customdata[1]:,}"
        "<extra></extra>"
)

st.plotly_chart(fig3, use_container_width=True)