import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from sidebar import render_sidebar

# -----------------------------
# Load data
# -----------------------------
ROOT = Path(__file__).resolve().parents[2]
RAW_DATA_PATH = ROOT / "data" / "raw" / "bank-full.csv"

df = pd.read_csv(RAW_DATA_PATH, sep = ";")
print(df.head(2))
print("COLUMNS: ", df.columns)

#======================================
# Every plots functions
#======================================
def show_marital_target_matrix(df):

	# --- Prepare data ---
	df['y_binary'] = df['y'].apply(lambda x: 1 if x=='yes' else 0)
	# Likelihood table
	likelihood = df.groupby('marital')['y_binary'].mean().reset_index()
	likelihood.rename(columns={'y_binary': 'likelihood'}, inplace=True)

	# Volume table (share of all subscribers)
	subscriber_counts = df[df['y'] == 'yes'].groupby('marital').size().reset_index(name='subscriber_count')
	total_subscribers = subscriber_counts['subscriber_count'].sum()
	subscriber_counts['volume_share'] = subscriber_counts['subscriber_count'] / total_subscribers

	# Merge likelihood + volume
	merged = pd.merge(likelihood, subscriber_counts, on='marital', how='left')
	merged['volume_share'] = merged['volume_share'].fillna(0)

	# --- Compute thresholds ---
	likelihood_threshold = merged['likelihood'].median()
	volume_threshold = merged['volume_share'].median()

	# --- Assign quadrant labels ---
	def classify_quadrant(row):
		if row['volume_share'] >= volume_threshold and row['likelihood'] >= likelihood_threshold:
			return "Prime Target"
		elif row['volume_share'] >= volume_threshold and row['likelihood'] < likelihood_threshold:
			return "Improvement Opportunity"
		elif row['volume_share'] < volume_threshold and row['likelihood'] >= likelihood_threshold:
			return "Niche / Unstable"
		else:
			return "Low Priority"

	merged['quadrant'] = merged.apply(classify_quadrant, axis=1)

	# --- Base scatter ---
	fig = px.scatter(
		merged,
		x='volume_share',
		y='likelihood',
		color='quadrant',
		size='volume_share',
		hover_data={},  # disable hover
		title="Marital Status Target Matrix: Subscription Likelihood vs Subscriber Volume",
		labels={'volume_share': 'Share of All Subscribers', 'likelihood': 'Subscription Likelihood'},
		size_max=40,
		color_discrete_map={
			"Prime Target": "#1f77b4",
			"Improvement Opportunity": "#ff7f0e",
			"Niche / Unstable": "#2ca02c",
			"Low Priority": "#d62728"
		}
	)

	# Add quadrant reference lines
	fig.add_hline(y=likelihood_threshold, line_dash="dash", line_color="gray")
	fig.add_vline(x=volume_threshold, line_dash="dash", line_color="gray")

	fig.update_layout(width=900, height=650, legend_title_text="Segment Type")

	# --- Quadrant shading ---
	x_min, x_max = merged['volume_share'].min(), merged['volume_share'].max()
	y_min, y_max = merged['likelihood'].min(), merged['likelihood'].max()

	fig.add_shape(type="rect", x0=x_min, x1=volume_threshold, y0=y_min, y1=likelihood_threshold,
			fillcolor="rgba(214, 39, 40, 0.08)", line_width=0)
	fig.add_shape(type="rect", x0=volume_threshold, x1=x_max, y0=y_min, y1=likelihood_threshold,
			fillcolor="rgba(255, 127, 14, 0.08)", line_width=0)
	fig.add_shape(type="rect", x0=x_min, x1=volume_threshold, y0=likelihood_threshold, y1=y_max,
			fillcolor="rgba(44, 160, 44, 0.08)", line_width=0)
	fig.add_shape(type="rect", x0=volume_threshold, x1=x_max, y0=likelihood_threshold, y1=y_max,
			fillcolor="rgba(31, 119, 180, 0.08)", line_width=0)

	# --- Quadrant labels ---
	x_left  = (x_min + volume_threshold) / 2
	x_right = (volume_threshold + x_max) / 2
	y_bottom = (y_min + likelihood_threshold) / 2
	y_top    = (likelihood_threshold + y_max) / 2

	fig.add_annotation(x=x_right, y=y_top, text="Prime Target", showarrow=False, font=dict(size=14))
	fig.add_annotation(x=x_right, y=y_bottom, text="Improvement Opportunity", showarrow=False, font=dict(size=14))
	fig.add_annotation(x=x_left, y=y_top, text="Niche / Unstable", showarrow=False, font=dict(size=14))
	fig.add_annotation(x=x_left, y=y_bottom, text="Low Priority", showarrow=False, font=dict(size=14))

	# --- Improved bubble labels ---
	for _, row in merged.iterrows():

		label_text = (
			f"<b>{row['marital']}</b><br>"
			f"Lik: {row['likelihood']:.2f} | Vol: {row['volume_share']:.2f}"
		)

		# Smart label placement
		if row['volume_share'] < volume_threshold:
			xanchor = "right"
			xshift = -10
		else:
			xanchor = "left"
			xshift = 10

		fig.add_annotation(
			x=row['volume_share'],
			y=row['likelihood'],
			text=label_text,
			showarrow=False,
			font=dict(size=11, color="black"),
			align="left",
			xanchor=xanchor,
			yanchor="middle",
			xshift=xshift,
			bgcolor="rgba(255,255,255,0.75)",
			bordercolor="rgba(0,0,0,0.25)",
			borderwidth=1,
			borderpad=3
		)

	return fig

def show_education_target_matrix(df):
    df['y_binary'] = df['y'].apply(lambda x: 1 if x=='yes' else 0)
    likelihood = df.groupby('education')['y_binary'].mean().reset_index()
    likelihood.rename(columns={'y_binary': 'likelihood'}, inplace=True)

    subscriber_counts = df[df['y'] == 'yes'].groupby('education').size().reset_index(name='subscriber_count')
    total_subscribers = subscriber_counts['subscriber_count'].sum()
    subscriber_counts['volume_share'] = subscriber_counts['subscriber_count'] / total_subscribers

    merged = pd.merge(likelihood, subscriber_counts, on='education', how='left')
    merged['volume_share'] = merged['volume_share'].fillna(0)

	# --- Thresholds ---
    likelihood_threshold = merged['likelihood'].median()
    volume_threshold = merged['volume_share'].median()
    # --- Quadrants ---
    def classify_quadrant(row):
        if row['volume_share'] >= volume_threshold and row['likelihood'] >= likelihood_threshold:
            return "Prime Target"
        elif row['volume_share'] >= volume_threshold and row['likelihood'] < likelihood_threshold:
            return "Improvement Opportunity"
        elif row['volume_share'] < volume_threshold and row['likelihood'] >= likelihood_threshold:
            return "Niche / Unstable"
        else:
            return "Low Priority"
	
    merged['quadrant'] = merged.apply(classify_quadrant, axis=1)

    # --- Base scatter ---
    fig = px.scatter(
        merged,
        x='volume_share',
        y='likelihood',
        color='quadrant',
        size='volume_share',
        hover_data={},  # disable hover
        title="Education Target Matrix: Subscription Likelihood vs Subscriber Volume",
        labels={'volume_share': 'Share of All Subscribers', 'likelihood': 'Subscription Likelihood'},
        size_max=40,
        color_discrete_map={
            "Prime Target": "#1f77b4",
            "Improvement Opportunity": "#ff7f0e",
            "Niche / Unstable": "#2ca02c",
            "Low Priority": "#d62728"
        }
    )
    fig.add_hline(y=likelihood_threshold, line_dash="dash", line_color="gray")
    fig.add_vline(x=volume_threshold, line_dash="dash", line_color="gray")
    fig.update_layout(width=900, height=650, legend_title_text="Segment Type")

    # --- Quadrant shading ---
    x_min, x_max = merged['volume_share'].min(), merged['volume_share'].max()
    y_min, y_max = merged['likelihood'].min(), merged['likelihood'].max()

    fig.add_shape(type="rect", x0=x_min, x1=volume_threshold, y0=y_min, y1=likelihood_threshold,
              fillcolor="rgba(214, 39, 40, 0.08)", line_width=0)
    fig.add_shape(type="rect", x0=volume_threshold, x1=x_max, y0=y_min, y1=likelihood_threshold,
              fillcolor="rgba(255, 127, 14, 0.08)", line_width=0)
    fig.add_shape(type="rect", x0=x_min, x1=volume_threshold, y0=likelihood_threshold, y1=y_max,
              fillcolor="rgba(44, 160, 44, 0.08)", line_width=0)
    fig.add_shape(type="rect", x0=volume_threshold, x1=x_max, y0=likelihood_threshold, y1=y_max,
              fillcolor="rgba(31, 119, 180, 0.08)", line_width=0)

    # --- Quadrant labels ---
    x_left  = (x_min + volume_threshold) / 2
    x_right = (volume_threshold + x_max) / 2
    y_bottom = (y_min + likelihood_threshold) / 2
    y_top    = (likelihood_threshold + y_max) / 2

    fig.add_annotation(x=x_right, y=y_top, text="Prime Target", showarrow=False, font=dict(size=14))
    fig.add_annotation(x=x_right, y=y_bottom, text="Improvement Opportunity", showarrow=False, font=dict(size=14))
    fig.add_annotation(x=x_left, y=y_top, text="Niche / Unstable", showarrow=False, font=dict(size=14))
    fig.add_annotation(x=x_left, y=y_bottom, text="Low Priority", showarrow=False, font=dict(size=14))

    # --- Improved bubble labels ---
    for _, row in merged.iterrows():

    # Bold education name + short metrics
        label_text = (
            f"<b>{row['education']}</b><br>"
            f"Lik: {row['likelihood']:.2f} | Vol: {row['volume_share']:.2f}"
        )

    # Smart label placement: right side for left quadrants, left side for right quadrants
        if row['volume_share'] < volume_threshold:
            xanchor = "right"
            xshift = -10
        else:
            xanchor = "left"
            xshift = 10

        fig.add_annotation(
            x=row['volume_share'],
            y=row['likelihood'],
            text=label_text,
            showarrow=False,
            font=dict(size=11, color="black"),
            align="left",
            xanchor=xanchor,
            yanchor="middle",
            xshift=xshift,
            bgcolor="rgba(255,255,255,0.7)",  # readable background
            bordercolor="rgba(0,0,0,0.2)",
            borderwidth=1,
            borderpad=3
            )

    return fig

def show_age_job_heatmap(df):

    import matplotlib.pyplot as plt
    import seaborn as sns
    import pandas as pd

    # Age groups
    bins = [18, 25, 35, 45, 55, 65, 100]
    labels = ['18–25', '26–35', '36–45', '46–55', '56–65', '65+']
    df['age_group'] = pd.cut(df['age'], bins=bins, labels=labels, right=False)

    # Binary target
    df['y_binary'] = df['y'].apply(lambda x: 1 if x == 'yes' else 0)

    # Likelihood table
    likelihood = df.pivot_table(
        values='y_binary',
        index='job',
        columns='age_group',
        aggfunc='mean'
    )

    # Sample size table
    sample_size = df.pivot_table(
        values='y_binary',
        index='job',
        columns='age_group',
        aggfunc='count'
    )

    # --- Plot dual heatmaps ---
    fig, axes = plt.subplots(1, 2, figsize=(22, 10))

    # Likelihood heatmap
    sns.heatmap(
        likelihood,
        annot=True,
        fmt=".2f",
        cmap="Blues",
        linewidths=.5,
        ax=axes[0]
    )
    axes[0].set_title("Subscription Likelihood by Job × Age Group")
    axes[0].set_xlabel("Age Group")
    axes[0].set_ylabel("Job Category")

    # Sample size heatmap
    sns.heatmap(
        sample_size,
        annot=True,
        fmt="d",
        cmap="Greens",
        linewidths=.5,
        ax=axes[1]
    )
    axes[1].set_title("Sample Size by Job × Age Group")
    axes[1].set_xlabel("Age Group")
    axes[1].set_ylabel("Job Category")

    plt.tight_layout()

    return fig   # ✅ return the figure, not plt.show()



def show_age_job_target_matrix(df):

    import pandas as pd
    import plotly.express as px

    # -------------------------
    # Prepare age groups
    # -------------------------
    bins = [18, 25, 35, 45, 55, 65, 100]
    labels = ['18–25', '26–35', '36–45', '46–55', '56–65', '65+']
    df['age_group'] = pd.cut(df['age'], bins=bins, labels=labels, right=False)

    # Binary target
    df['y_binary'] = df['y'].apply(lambda x: 1 if x == 'yes' else 0)

    # Likelihood table
    likelihood = df.pivot_table(
        values='y_binary',
        index='job',
        columns='age_group',
        aggfunc='mean'
    )

    # Sample size table
    sample_size = df.pivot_table(
        values='y',
        index='job',
        columns='age_group',
        aggfunc='count',
        fill_value=0
    )

    # Melt both tables into long format
    likelihood_long = likelihood.reset_index().melt(
        id_vars='job',
        var_name='age_group',
        value_name='likelihood'
    )

    sample_long = sample_size.reset_index().melt(
        id_vars='job',
        var_name='age_group',
        value_name='sample_size'
    )

    # Merge likelihood + sample size
    merged = pd.merge(likelihood_long, sample_long, on=['job', 'age_group'])

    # Remove rows with missing likelihood
    merged = merged.dropna(subset=['likelihood'])

    # -------------------------
    # Compute thresholds
    # -------------------------
    likelihood_threshold = merged['likelihood'].median()
    sample_threshold = merged['sample_size'].median()

    # Quadrant classification
    def classify_quadrant(row):
        if row['sample_size'] >= sample_threshold and row['likelihood'] >= likelihood_threshold:
            return "Prime Target"
        elif row['sample_size'] >= sample_threshold and row['likelihood'] < likelihood_threshold:
            return "Improvement Opportunity"
        elif row['sample_size'] < sample_threshold and row['likelihood'] >= likelihood_threshold:
            return "Niche / Unstable"
        else:
            return "Low Priority"

    merged['quadrant'] = merged.apply(classify_quadrant, axis=1)

    # -------------------------
    # Interactive scatter plot
    # -------------------------
    fig = px.scatter(
        merged,
        x='sample_size',
        y='likelihood',
        color='quadrant',
        size='sample_size',
        hover_name='job',
        hover_data={
            'age_group': True,
            'sample_size': True,
            'likelihood': ':.2f',
            'quadrant': True
        },
        title="Interactive Target Matrix: Subscription Likelihood vs Sample Size (Job × Age Group)",
        labels={
            'sample_size': 'Sample Size (Segment Size)',
            'likelihood': 'Subscription Likelihood'
        },
        size_max=40,
        color_discrete_map={
            "Prime Target": "#1f77b4",
            "Improvement Opportunity": "#ff7f0e",
            "Niche / Unstable": "#2ca02c",
            "Low Priority": "#d62728"
        }
    )

    # Reference lines
    fig.add_hline(y=likelihood_threshold, line_dash="dash", line_color="gray")
    fig.add_vline(x=sample_threshold, line_dash="dash", line_color="gray")

    fig.update_layout(
        width=1000,
        height=700,
        legend_title_text="Segment Type"
    )

    # -------------------------
    # Quadrant shading
    # -------------------------
    x_min, x_max = merged['sample_size'].min(), merged['sample_size'].max()
    y_min, y_max = merged['likelihood'].min(), merged['likelihood'].max()

    x_left = (x_min + sample_threshold) / 2
    x_right = (sample_threshold + x_max) / 2
    y_bottom = (y_min + likelihood_threshold) / 2
    y_top = (likelihood_threshold + y_max) / 2

    fig.add_shape(type="rect",
                  x0=x_min, x1=sample_threshold,
                  y0=y_min, y1=likelihood_threshold,
                  fillcolor="rgba(214, 39, 40, 0.08)", line_width=0)

    fig.add_shape(type="rect",
                  x0=sample_threshold, x1=x_max,
                  y0=y_min, y1=likelihood_threshold,
                  fillcolor="rgba(255, 127, 14, 0.08)", line_width=0)

    fig.add_shape(type="rect",
                  x0=x_min, x1=sample_threshold,
                  y0=likelihood_threshold, y1=y_max,
                  fillcolor="rgba(44, 160, 44, 0.08)", line_width=0)

    fig.add_shape(type="rect",
                  x0=sample_threshold, x1=x_max,
                  y0=likelihood_threshold, y1=y_max,
                  fillcolor="rgba(31, 119, 180, 0.08)", line_width=0)

    # -------------------------
    # Quadrant labels
    # -------------------------
    fig.add_annotation(x=x_right, y=y_top, text="Prime Target", showarrow=False, font=dict(size=13))
    fig.add_annotation(x=x_right, y=y_bottom, text="Improvement Opportunity", showarrow=False, font=dict(size=13))
    fig.add_annotation(x=x_left, y=y_top, text="Niche / Unstable", showarrow=False, font=dict(size=13))
    fig.add_annotation(x=x_left, y=y_bottom, text="Low Priority", showarrow=False, font=dict(size=13))

    # -------------------------
    # Quadrant explanation box
    # -------------------------
    fig.add_annotation(
        x=1.32, y=-0.15, xref="paper", yref="paper",
        text=(
            "Large sample + high likelihood → <b>Prime Targets</b><br>"
            "Large sample + low likelihood → <b>Improvement Opportunities</b><br>"
            "Small sample + high likelihood → <b>Niche / Unstable</b><br>"
            "Small sample + low likelihood → <b>Low Priority</b>"
        ),
        showarrow=False,
        align="left",
        font=dict(size=8, color="black"),
        bordercolor="lightgrey",
        borderwidth=1,
        borderpad=6,
        bgcolor="white",
        opacity=0.9
    )

    return fig

def show_age_group_barplots(df):

    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns

    # ----------------------------------------
    # Create age bins
    # ----------------------------------------
    bins = [18, 25, 35, 45, 55, 65, 100]
    labels = ['18–25', '26–35', '36–45', '46–55', '56–65', '65+']
    df['age_group'] = pd.cut(df['age'], bins=bins, labels=labels, right=False)

    # ----------------------------------------
    # Prepare data
    # ----------------------------------------
    df['subscribed'] = df['y'].apply(lambda x: 1 if x == 'yes' else 0)

    subscriber_volume = (
        df[df['y'] == 'yes']['age_group']
        .value_counts(normalize=True)
        .sort_index()
    )

    # ----------------------------------------
    # Side-by-side plots
    # ----------------------------------------
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    # Transparent background
    fig.patch.set_alpha(0.0)
    for ax in axes:
        ax.set_facecolor("none")

    # ----------------------------------------
    # Plot 1: Subscription Rate by Age Group
    # ----------------------------------------
    ax1 = axes[0]
    sns.barplot(
        data=df,
        x='age_group',
        y='subscribed',
        ci=None,
        ax=ax1,
        color="#2F6F73"   # primary color
    )

    for p in ax1.patches:
        ax1.annotate(
            f"{p.get_height():.2%}",
            (p.get_x() + p.get_width() / 2., p.get_height()),
            ha='center',
            va='bottom',
            color="white"
        )

    ax1.set_title("Likelihood of Subscription by Age Group", color="white")
    ax1.set_xlabel("Age Group", color="white")
    ax1.set_ylabel("Subscription Rate", color="white")

    # White tick labels
    ax1.tick_params(axis='x', colors='white')
    ax1.tick_params(axis='y', colors='white')

    # ----------------------------------------
    # Plot 2: Share of All Subscribers by Age Group
    # ----------------------------------------
    ax2 = axes[1]
    sns.barplot(
        x=subscriber_volume.index,
        y=subscriber_volume.values,
        color="#5E8F95",
        ax=ax2
    )

    ax2.set_title("Share of Total Subscribers by Age Group", color="white")
    ax2.set_xlabel("Age Group", color="white")
    ax2.set_ylabel("Share of Subscribers", color="white")
    ax2.set_ylim(0, subscriber_volume.max() + 0.05)

    for i, v in enumerate(subscriber_volume.values):
        ax2.text(i, v + 0.005, f"{v:.1%}", ha='center', color="white")

    # White tick labels
    ax2.tick_params(axis='x', colors='white')
    ax2.tick_params(axis='y', colors='white')

    # ----------------------------------------
    # Clean style: remove spines
    # ----------------------------------------
    for ax in axes:
        sns.despine(ax=ax, top=True, right=True)
        ax.spines['bottom'].set_color('white')
        ax.spines['left'].set_color('white')

    plt.tight_layout()

    return fig


def build_segment_hierarchy(df):

    import pandas as pd
    import numpy as np

    df = df.copy()

    # AGE GROUPS
    bins = [18, 25, 35, 45, 55, 65, 100]
    labels = ['18–25', '26–35', '36–45', '46–55', '56–65', '65+']
    df['age_group'] = pd.cut(df['age'], bins=bins, labels=labels, right=False)

    df['y_binary'] = df['y'].apply(lambda x: 1 if x == 'yes' else 0)


    # LEAF LEVEL ONLY
    leaf = df.groupby(
        ['age_group', 'job', 'education', 'marital'],
        dropna=False
    ).agg(
        volume=('y_binary', 'sum'),
        sample_size=('y_binary', 'count')
    ).reset_index()

    # Filter unstable segments
    leaf = leaf[leaf['sample_size'] >= 50].copy()
    leaf['likelihood'] = leaf['volume'] / leaf['sample_size']

    # Convert to string for Plotly
    for col in ["age_group", "job", "education", "marital"]:
        leaf[col] = leaf[col].astype(str)

    return leaf




def show_treemap(hierarchy):

    import numpy as np
    import plotly.express as px

    df = hierarchy.copy()

    # customdata = [volume, likelihood]
    df["volume_int"] = df["volume"].astype(int)
    customdata = np.stack(
        [df["volume_int"], df["likelihood"]],
        axis=-1
    )

    # Custom color scale based on your team color #2F6F73
    custom_scale = [
        [0.0, "#D9E7E8"],   # very light tint
        [0.5, "#5A8F92"],   # medium tint
        [1.0, "#2F6F73"]    # primary color
    ]

    fig = px.treemap(
        df,
        path=["age_group", "job", "education", "marital"],
        values="sample_size",
        color="likelihood",
        color_continuous_scale=custom_scale,
        title="Treemap: Population Structure by Demographic Layers"
    )

    fig.data[0].customdata = customdata

    fig.update_traces(
        hovertemplate=(
            "%{label}<br>"
            "sample_size: %{value}<br>"
            "volume: %{customdata[0]:d}<br>"
            "likelihood: %{customdata[1]:.3f}"
            "<extra></extra>"
        )
    )

    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))

    return fig



# -----------------------------
# Streamlit UI
# -----------------------------
# The page title and caption
render_sidebar()
st.title("📊 Demographic Insights of Our Customer Base")
st.caption(
	"🔍 A focused analysis of age, education, marital status, and employment that shape customer behavior and reveal opportunities for targeted marketing."
)
# show a devider
st.divider()

# =========================================================
# 👥 AGE ANALYSIS SECTION⭐ 
# =========================================================
st.header("👥 Age Insights")
st.markdown("⭐ Age are grouped into 6 buckets: 18–25, 26–35, 36–45, 46–55, 56–65, and 65+.")

st.pyplot(show_age_group_barplots(df))
st.markdown(
    """
⚪ Since Age by itself does not provide a reliable basis for targeting, given there are only two combinations:
- Large Sample Size with Low Likelihood  
- Small Sample Size with High Likelihood  

⭐ Therefore, we need to layer Age with other demographics (e.g., job) to identify more actionable segments.
"""
)

# =========================================================
# 👥 AGE X Employment ANALYSIS SECTION
# =========================================================
st.divider()
st.header("👥 Age X 💼 Employment Insights")

st.subheader("📈 How Age and Job Shape Subscription Likelihood")
st.markdown("🔍 Older retired customers, younger students and mid-older unemployed customers show higher likelihood to subscribe term deposits.")
st.markdown("🔍 Working age groups (26-55) such as blue-collar, services, admin and technician show lower subscription likelihood")



fig = show_age_job_heatmap(df)
st.pyplot(fig)
plt.close(fig)




st.divider()
# -------------------------
# 🎯 AGE TARGET MATRIX
# -------------------------
st.header("🎯 Who to Target - based on Age and Job")
st.markdown(
	"""
	This matrix highlights how each age x job group performs across two dimensions:**subscription likelihood** and **subscriber volume**.  
	It helps identify which groups are prime targets, improvement opportunities, or niche segments.
	"""
)

st.plotly_chart(show_age_job_target_matrix(df), use_container_width=True)
st.divider()

# =========================================================
# 🎓 EDUCATION INSIGHTS
# =========================================================

st.header("🎓 based on Education Level")
st.markdown(
	"""
	- 🎓 Higher education levels tend to correlate with slightly higher subscription likelihood.  
	"""
)
st.plotly_chart(show_education_target_matrix(df), use_container_width=True)
st.divider()
# =========================================================
# 💍 MARITAL STATUS INSIGHTS
# =========================================================

st.header("💍 based on Marital Status")
st.markdown(
	"""
	- 💑 Married individuals form the largest subscriber volume but have lower subscription likelihood compared to single individuals.  
	- 📉 But single individuals show higher subscription likelihood  
	"""
)
st.plotly_chart(show_marital_target_matrix(df), use_container_width=True)

# =========================================================
# 🏁 SUMMARY
# =========================================================

st.header("🏁 Summary")
st.markdown(
	"""
	Demographic patterns reveal clear opportunities for targeted marketing.  
	While younger and older customers show strong interest, the largest customer segments underperform in conversion, suggesting that tailored messaging and channel optimization could unlock significant gains.
	"""
)


#fig2 = show_all_treemap(df)
hierarchy = build_segment_hierarchy(df)
st.plotly_chart(show_treemap(hierarchy), use_container_width=True) #subject to move to main page if necessary




st.divider()
