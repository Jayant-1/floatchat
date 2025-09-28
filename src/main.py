"""
FloatChat - Conversational AI for ARGO Ocean Data
Smart India Hackathon 2025

Main Streamlit Application Entry Point
"""

import streamlit as st
import sys
import os
from pathlib import Path

# Add the current directory to the Python path
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

from utils.config import PAGE_CONFIG, THEME_CONFIG
from utils.data_generator import DataGenerator
from utils.ui_components import render_header, render_sidebar

# Page configuration
st.set_page_config(
    page_title=PAGE_CONFIG["title"],
    page_icon=PAGE_CONFIG["icon"],
    layout=PAGE_CONFIG["layout"],
    initial_sidebar_state="expanded",
    menu_items=PAGE_CONFIG["menu_items"],
)

# Apply custom CSS
st.markdown(
    f"""
<style>
    {THEME_CONFIG["custom_css"]}
</style>
""",
    unsafe_allow_html=True,
)


def render_top_navigation():
    """Render top navigation bar instead of sidebar."""
    col1, col2, col3, col4, col5 = st.columns(5)

    # Home stays first
    with col1:
        if st.button("🏠 Home", key="nav_home", use_container_width=True):
            st.session_state.current_page = "Home"
            st.rerun()

    # Chat moved to second position
    with col2:
        if st.button("💬 Chat", key="nav_chat", use_container_width=True):
            st.session_state.current_page = "FloatChat AI"
            st.rerun()

    # Map now third
    with col3:
        if st.button("🗺️ Map", key="nav_map", use_container_width=True):
            st.session_state.current_page = "ARGO Floats Map"
            st.rerun()

    # Data fourth
    with col4:
        if st.button("📊 Data", key="nav_data", use_container_width=True):
            st.session_state.current_page = "Data Explorer"
            st.rerun()

    # Admin fifth
    with col5:
        if st.button("⚙️ Admin", key="nav_admin", use_container_width=True):
            st.session_state.current_page = "Admin Dashboard"
            st.rerun()

    st.markdown("---")


def main():
    """Main application function"""

    # Initialize session state
    if "data_generator" not in st.session_state:
        st.session_state.data_generator = DataGenerator()

    if "first_visit" not in st.session_state:
        st.session_state.first_visit = True

    if "current_page" not in st.session_state:
        st.session_state.current_page = "Home"

    # Render header
    render_header()

    # Render top navigation instead of sidebar
    render_top_navigation()

    # Get current page (now managed by session state)
    selected_page = st.session_state.current_page

    # Main content area
    if selected_page == "Home":
        from app_pages.home import render_home_page

        render_home_page()

    elif selected_page == "ARGO Floats Map":
        from app_pages.map_visualizer import render_map_page

        render_map_page()

    elif selected_page == "Data Explorer":
        from app_pages.data_explorer import render_data_explorer_page

        render_data_explorer_page()

    elif selected_page == "FloatChat AI":
        from app_pages.chatbot import render_floatchat

        render_floatchat()

    elif selected_page == "Admin Dashboard":
        from app_pages.admin import render_admin_page

        render_admin_page()


if __name__ == "__main__":
    main()
