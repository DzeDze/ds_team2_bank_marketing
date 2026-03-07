# app/sidebar.py
import streamlit as st

def render_sidebar():
    with st.sidebar:
        st.markdown("## ⭐ Priority Pages")
        st.page_link("pages/05_Customer_Segmentation.py", label="Customer Segmentation", icon="🧩")
        st.page_link("pages/06_High_Impact_Customer_Profiles.py", label="High Impact Customer Profiles", icon="⭐")
        st.page_link("pages/07_Customer_Targeting.py", label="Customer Targeting", icon="🎯")
        st.markdown("---")