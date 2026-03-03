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
# -----------------------------
# age_group
# -----------------------------
bins = [18, 25, 35, 45, 55, 65, 100]
labels = ['18–25', '26–35', '36–45', '46–55', '56–65', '65+']

df['age_group'] = pd.cut(df['age'], bins=bins, labels=labels, right=False)

subscriber_volume = (
    df[df['y'] == 'yes']['age_group']
    .value_counts(normalize=True)
    .sort_index()
)

def show_subscribers_by_age_group():
    plt.figure(figsize=(10,6))
    sns.barplot(
        x=subscriber_volume.index,
        y=subscriber_volume.values,
        color='steelblue'
    )

    plt.title("Share of All Subscribers by Age Group")
    plt.xlabel("Age Group")
    plt.ylabel("Share of Subscribers")
    plt.ylim(0, subscriber_volume.max() + 0.05)

    # Add percentage labels
    for i, v in enumerate(subscriber_volume.values):
        plt.text(i, v + 0.005, f"{v:.1%}", ha='center')
    
    return plt.gcf()

def show_subscribers_by_age_group_plotly():
    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=subscriber_volume.index.astype(str),
            y=subscriber_volume.values,
            marker_color="steelblue",
            text=[f"{v:.1%}" for v in subscriber_volume.values],
            textposition="outside",
        )
    )

    fig.update_layout(
        title="Share of All Subscribers by Age Group",
        xaxis_title="Age Group",
        yaxis_title="Share of Subscribers",
        yaxis=dict(range=[0, float(subscriber_volume.max()) + 0.05]),
    )

    return fig

# -----------------------------
# Streamlit UI
# -----------------------------
st.title("Example Page: Kerensa")
st.caption(
    "This is an Example Page for **Kerensa**. "
    "Use it as a template: load data -> compute something -> visualize."
)


# show a devider
st.divider()

# show show_subscribers_by_age_group plot
st.subheader("Example: Subscribers by Age Group")
fig = show_subscribers_by_age_group()
st.pyplot(fig)
plt.close(fig)

# show a devider
st.divider()

st.subheader("Subscribers by Age Group (Plotly Version)")
fig_plotly = show_subscribers_by_age_group_plotly()
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