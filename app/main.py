import streamlit as st
from sidebar import render_sidebar

st.set_page_config(
    page_title="Bank Marketing Campaign Analysis",
    page_icon="📊",
    layout="wide",
)
render_sidebar()
# ---------- STYLE ----------
st.markdown(
    """
<style>

/* ----- CARD ----- */
.nav-card {
    border-radius: 14px;
    padding: 22px 20px 20px 20px;
    background: #ffffff;
    border-left: 6px solid #2F6F73;
    border-top: 1px solid rgba(0,0,0,0.05);
    border-right: 1px solid rgba(0,0,0,0.05);
    border-bottom: 1px solid rgba(0,0,0,0.05);
    min-height: 210px;
    transition: all 0.18s ease;
    box-shadow: 0 3px 10px rgba(0,0,0,0.04);
}

.nav-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 10px 24px rgba(0,0,0,0.08);
    border-left: 6px solid #3b8f94;
}

/* ----- CARD TITLE ----- */
.nav-title {
    font-size: 1.15rem;
    font-weight: 700;
    margin-bottom: 0.35rem;
    color: #2F6F73;
}

/* ----- CARD TEXT ----- */
.nav-text {
    color: #4b5563;
    font-size: 0.95rem;
    line-height: 1.45;
    margin-bottom: 1rem;
}

/* ----- SECTION TITLE ----- */
.section-title {
    font-size: 1.25rem;
    font-weight: 700;
    margin: 0.5rem 0 1.2rem 0;
    color: #2F6F73;
}

/* remove link styling */
.card-link {
    text-decoration: none;
}

</style>
""",
    unsafe_allow_html=True,
)

# ---------- HEADER ----------
st.title("📊 Bank Marketing Campaign Analysis")
st.caption("Data-driven insights to improve targeting for term deposit marketing campaigns")

st.divider()

# ---------- TOP INFO CARDS ----------
col1, col2, col3 = st.columns(3, gap="large")

with col1:
    st.markdown(
        """
<div class="nav-card">
<div class="nav-title">🎯 What is this analysis?</div>
<div class="nav-text">
Identify high-potential customers, detect low-yield segments,
and support more targeted term-deposit campaigns.
</div>
</div>
""",
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
<div class="nav-card">
<div class="nav-title">👥 Who benefits?</div>
<div class="nav-text">
Marketing, CRM, campaign operations, analytics,
and leadership teams looking to improve targeting precision.
</div>
</div>
""",
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        """
<div class="nav-card">
<div class="nav-title">💡 Key insights</div>
<div class="nav-text">
Financial strength, loan status, and previous campaign outcomes
are strong indicators of subscription likelihood.
</div>
</div>
""",
        unsafe_allow_html=True,
    )

st.divider()

# ---------- NAVIGATION ----------
st.markdown('<div class="section-title">Explore the analysis</div>', unsafe_allow_html=True)

row1 = st.columns(3, gap="large")
row2 = st.columns(3, gap="large")

def nav_card(col, title, text, page):
    with col:
        with st.container(border=True):
            st.markdown(f"### {title}")
            st.write(text)
            st.page_link(page, label="Open page →")

nav_card(
    row1[0],
    "👤 Demographic Profile",
    "Explore age, job, and demographic patterns.",
    "pages/01_Demographic_Profile.py",
)

nav_card(
    row1[1],
    "💰 Financial Profile",
    "Analyze balance, loans, and financial characteristics.",
    "pages/02_Financial_Profile.py",
)

nav_card(
    row1[2],
    "📈 Previous Campaign Effectiveness",
    "Understand how past campaigns influence outcomes.",
    "pages/03_Previous_Campaign_Effectiveness.py",
)

nav_card(
    row2[0],
    "🧩 Customer Segmentation",
    "Target and avoid segments with lift analysis.",
    "pages/05_Customer_Segmentation.py",
)

nav_card(
    row2[1],
    "⭐ High Impact Customer Profiles",
    "Identify actionable high-conversion profiles.",
    "pages/06_High_Impact_Customer_Profiles.py",
)

nav_card(
    row2[2],
    "🎯 Customer Targeting",
    "Upload CSV, score customers, download ranked list.",
    "pages/07_Customer_Targeting.py",
)

st.divider()

cta1, cta2 = st.columns([1, 1], gap="large")

with cta1:
    st.page_link(
        "pages/05_Customer_Segmentation.py",
        label="🚀 Start with Customer Segmentation",
    )

with cta2:
    st.page_link(
        "pages/07_Customer_Targeting.py",
        label="📥 Upload Customer List",
    )
