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

eda_df = df.copy()
eda_df['only_yes'] = (eda_df['y'] == 'yes').astype(int)
month_success = eda_df.groupby('month')['only_yes'].mean().mul(100).reset_index()
overall_avg = eda_df['only_yes'].mean() * 100

def show_sub_rate_by_month():
    plt.figure(figsize=(10,5))
    month_success['color'] = month_success['only_yes'].apply(lambda x: 'green' if x >= overall_avg else 'red')
    sns.barplot(x='month', y='only_yes', data=month_success, palette=month_success['color'].tolist())
    plt.axhline(overall_avg, color='darkblue', linestyle='--', linewidth=1, label=f'Average: {overall_avg:.2f}%')
    plt.title('Subscription Rate by Month')
    plt.ylabel('Subscription Rate (%)')
    plt.xlabel('Month')
    plt.legend()
    
    return plt.gcf()

def show_sub_rate_by_month_plotly():
    colors = [
        "green" if x >= overall_avg else "red"
        for x in month_success["only_yes"]
    ]

    fig = go.Figure()

    # Bar chart
    fig.add_trace(
        go.Bar(
            x=month_success["month"],
            y=month_success["only_yes"],
            marker_color=colors,
            name="Subscription Rate",
            text=[f"{v:.2f}%" for v in month_success["only_yes"]],
            textposition="outside",
        )
    )

    # Average line
    fig.add_hline(
        y=overall_avg,
        line_dash="dash",
        line_color="darkblue",
        annotation_text=f"Average: {overall_avg:.2f}%",
        annotation_position="top left"
    )

    fig.update_layout(
        title="Subscription Rate by Month",
        xaxis_title="Month",
        yaxis_title="Subscription Rate (%)",
        showlegend=True,
    )

    return fig

# -----------------------------
# Streamlit UI
# -----------------------------
st.title("Example Page: Kateryna")
st.caption(
    "This is an Example Page for **Kateryna**. "
    "Use it as a template: load data -> compute something -> visualize."
)


# show a devider
st.divider()

# show show_subscribers_by_age_group plot
st.subheader("Example: Subscription Rate by Month")
fig = show_sub_rate_by_month()
st.pyplot(fig)
plt.close(fig)

# show a devider
st.divider()

st.subheader("Subscription Rate by Month (Plotly Version)")
fig_plotly = show_sub_rate_by_month_plotly()
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