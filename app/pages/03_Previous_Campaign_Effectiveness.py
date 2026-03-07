import pandas as pd
import streamlit as st
import plotly.express as px
from sidebar import render_sidebar

st.set_page_config(page_title="Previous Campaign Effectiveness", layout="wide")
render_sidebar()
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


# =========================================================
# ANALYSIS 7: Monthly Trends in Conversion Rate
# =========================================================

st.header("Monthly Trends in Conversion Rate")

eda_df = df.copy()
eda_df['only_yes'] = (eda_df['y'] == 'yes').astype(int)
month_success = eda_df.groupby('month')['only_yes'].mean().mul(100).reset_index()
overall_avg = eda_df['only_yes'].mean() * 100

month_success['color'] = month_success['only_yes'].apply(
    lambda x: '#2F6F73' if x >= overall_avg else '#8FB3C1'
)

fig = px.bar(
    month_success,
    x='month',
    y='only_yes',
    title='Conversion Rate by Month',
    labels={'only_yes': 'Conversion Rate (%)', 'month': 'Month'},
    color='color',
    color_discrete_map='identity'
)

fig.add_hline(
    y=overall_avg,
    line_dash='dash',
    line_color='white',
    line_width=1,
    annotation_text=f'Average: {overall_avg:.2f}%',
    annotation_position='top right'
)

st.plotly_chart(fig, use_container_width=True)

# =========================================================
# ANALYSIS 8: Call Duration as a Predictor of Conversion
# =========================================================

st.header("Call Duration as a Predictor of Conversion")

bins = [0, 1, 2, 3, 4, 10, eda_df['duration'].max()+1]
labels = ['<1','1-2','2-3','3-4','5-10','>10']
eda_df['duration_bin'] = pd.cut(eda_df['duration']/60, bins=bins, labels=labels, right=False)

duration_success = eda_df.groupby('duration_bin')['only_yes'].mean().mul(100).reset_index()
duration_success['color'] = duration_success['only_yes'].apply(
    lambda x: '#2F6F73' if x >= overall_avg else '#8FB3C1'
)

fig = px.bar(
    duration_success,
    x='duration_bin',
    y='only_yes',
    title='Conversion Rate by Call Duration',
    labels={'only_yes': 'Conversion Rate (%)', 'duration_bin': 'Call Duration (in minutes)'},
    color='color',
    color_discrete_map='identity',
)

fig.add_hline(
    y=overall_avg,
    line_dash='dash',
    line_color='white',
    line_width=1,
    annotation_text=f'Average: {overall_avg:.2f}%',
    annotation_position='top right',
)

st.plotly_chart(fig, use_container_width=True)

# =========================================================
# ANALYSIS 9: Impact of Contact Frequency on Conversion Probability
# =========================================================

st.header("Impact of Contact Frequency on Conversion Probability")

contact_success = eda_df.groupby('campaign')['only_yes'].mean().mul(100).reset_index()

fig = px.line(
    contact_success,
    x='campaign',
    y='only_yes',
    title='Conversion Rate by Contact Count',
    labels={'only_yes': 'Conversion Rate (%)', 'campaign': 'Number of Contacts in Campaign'},
)
fig.update_traces(line_color='#1F4E52', line=dict(width=5))

# Add colored markers for above/below average
for color, label in [("#36B464", 'Above Average'), ("#DD4D4D", 'Below Average')]:
    mask = contact_success['only_yes'] >= overall_avg if color == "#36B464" else contact_success['only_yes'] < overall_avg
    subset = contact_success[mask]
    fig.add_scatter(
        x=subset['campaign'],
        y=subset['only_yes'],
        mode='markers',
        marker=dict(color=color, size=10),
        name=label
    )

fig.add_hline(
    y=overall_avg,
    line_dash='dash',
    line_color='white',
    line_width=1,
    annotation_text=f'Average: {overall_avg:.2f}%',
    annotation_position='top right',
)

st.plotly_chart(fig, use_container_width=True)

# =========================================================
# ANALYSIS 10: Conversion Performance by Contact Channel
# =========================================================

st.header("Conversion Performance by Contact Channel")

contact_type_success = eda_df.groupby('contact')['only_yes'].mean().mul(100).reset_index()

fig = px.bar(
    contact_type_success,
    x='contact',
    y='only_yes',
    title='Conversion Rate by Contact Type',
    labels={'only_yes': 'Conversion Rate (%)', 'contact': 'Contact Type'},
    color_discrete_sequence=['#2F6F73'],
)

fig.add_hline(
    y=overall_avg,
    line_dash='dash',
    line_color='white',
    line_width=1,
    annotation_text=f'Average: {overall_avg:.2f}%',
    annotation_position='top right',
)

st.plotly_chart(fig, use_container_width=True)

# =========================================================
# 🏁 SUMMARY
# =========================================================

st.header("Summary")
st.markdown(
	"""
	Past interactions remain one of the strongest predictors of future success. Customers who previously subscribed are highly likely to convert again, making re-engagement particularly efficient.

Those who previously failed to subscribe show reduced responsiveness, repeated targeting may result in diminishing returns. Customers contacted recently show higher likelihood to subscribe, emphasizing the value of recency-based segmentation.




Contact strategy also matters:

- Fewer contact attempts with meaningful conversations perform best, over-contacting hurts conversion rates.
- Call duration positively correlates with success, calls lasting at least five minutes tend to yield better results.
- The cellular channel performs slightly better than telephone, though both are effective.
- Seasonal timing matters: March shows the strongest conversion rates, followed by September, October, and December.


	"""
)