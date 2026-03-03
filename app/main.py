"""
app/main.py

Streamlit entrypoint (Home page).
"""

import streamlit as st

st.set_page_config(
    page_title="Segmentation + High-Impact Customer Targeting + Customer Ranking",
    page_icon="📈",
    layout="wide",
)

st.title("📈 Marketing Targeting Dashboard")
st.caption(
    "Segmentation strategy -> top actionable profiles  -> customer ranking & activation lists."
)

st.markdown(
    """
Use the pages in the left sidebar:

- **Segment Strategy**: target/avoid segments + decision map + decision table  
- **High-Impact Customer Targeting**: top actionable profiles  
- **Customer Targeting**: upload a CSV -> score & download ranked target list
"""
)

# def main() -> None:
#     """Render the app home/landing page."""
#     st.set_page_config(page_title="Analytics Dashboard", layout="wide")

#     st.title("Analytics Dashboard")
#     st.write("Use the sidebar to open **Dashboard**.")

#     st.markdown("### Pages")
#     st.markdown("- **Dashboard**: segmentation + other analytics modules")

#     st.markdown("### Notes")
#     st.markdown(
#         "- This app uses Streamlit multipage: files under `app/pages/` appear in the sidebar.\n"
#         "- Each team member can add their own module under `app/components/`"
#     )


# if __name__ == "__main__":
#     main()