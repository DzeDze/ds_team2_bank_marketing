import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path
import streamlit as st
import plotly.graph_objects as go

# -----------------------------
# Load data
# -----------------------------
ROOT = Path(__file__).resolve().parents[2]
RAW_DATA_PATH = ROOT / "data" / "raw" / "bank-full.csv"

df = pd.read_csv(RAW_DATA_PATH, sep = ";")
print(df.head(2))
print("COLUMNS: ", df.columns)

# 2) Convert target to numeric
df["subscribed"] = df["y"].map({"yes": 1, "no": 0})

# 3) Create balance quartiles
df["balance_bin"] = pd.qcut(df["balance"], q=4, duplicates="drop")

# 4) Calculate subscription rate per quartile
conversion_by_bin = df.groupby("balance_bin")["subscribed"].mean()

def show_sub_rate_by_bal_quartile():
    # 5) Plot bar chart
    plt.figure(figsize=(8, 5))
    conversion_by_bin.plot(kind="bar")

    plt.title("Subscription Rate by Balance Quartile")
    plt.xlabel("Balance Quartile")
    plt.ylabel("Subscription Rate")
    plt.grid(axis="y", alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    return plt.gcf()

def show_sub_rate_by_bal_quartile_plotly():
    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=conversion_by_bin.index.astype(str),
            y=conversion_by_bin.values,
            marker_color="steelblue",
            text=[f"{v:.1%}" for v in conversion_by_bin.values],
            textposition="outside",
        )
    )

    fig.update_layout(
        title="Subscription Rate by Balance Quartile",
        xaxis_title="Balance Quartile",
        yaxis_title="Subscription Rate",
        xaxis_tickangle=45,
    )

    return fig

# -----------------------------
# Streamlit UI
# -----------------------------
st.title("Example Page: CookieJars")
st.caption(
    "This is an Example Page for **CookieJars**. "
    "Use it as a template: load data -> compute something -> visualize."
)


# show a devider
st.divider()

# show show_subscribers_by_age_group plot
st.subheader("Example: Subscription Rate by Balance Quartile")
fig = show_sub_rate_by_bal_quartile()
st.pyplot(fig)
plt.close(fig)

# show a devider
st.divider()

st.subheader("Subscription Rate by Balance Quartile (Plotly Version)")
fig_plotly = show_sub_rate_by_bal_quartile_plotly()
st.plotly_chart(fig_plotly, use_container_width=True)

# show a devider
st.divider()

example = 1
st.subheader("Example: how to render markdown")
st.markdown(
    f"""
### Lorem Ipsum Section

Lorem ipsum dolor sit amet, consectetur adipiscing elit.  
Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.

- Lorem ipsum dolor sit amet  
- Consectetur adipiscing elit  
- Sed do eiusmod tempor incididunt  

Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.  
Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.

---

Example variable value: `{example}`
"""
)