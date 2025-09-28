from streamlit_option_menu import option_menu
import streamlit as st

# --- Set page to wide layout ---
st.set_page_config(
    page_title="FloatChat App",
    page_icon="🚀",
    layout="wide",  # make page wide
    initial_sidebar_state="expanded"
)

def render_sidebar_navigation():
    """Vertical navigation menu in the sidebar."""

    with st.sidebar:
        selected = option_menu(
            menu_title=None , 
            options=["Home", "FloatChat AI", "ARGO Floats Map", "Data Explorer", "Admin Dashboard"],
            icons=["house", "chat-dots", "map", "bar-chart", "gear"],
            menu_icon="cast",
            default_index=0,
            orientation="vertical",
            key="sidebar_nav_menu"
        )
    # Store selection in session state
    st.session_state.current_page = selected


# --- Usage in main app ---
render_sidebar_navigation()

selected_page = st.session_state.get("current_page", "Home")

if selected_page == "Home":
    from app_pages.home import render_home_page
    render_home_page()
elif selected_page == "FloatChat AI":
    from app_pages.chatbot import render_floatchat
    render_floatchat()
elif selected_page == "ARGO Floats Map":
    from app_pages.map_visualizer import render_map_page
    render_map_page()
elif selected_page == "Data Explorer":
    from app_pages.data_explorer import render_data_explorer_page
    render_data_explorer_page()
elif selected_page == "Admin Dashboard":
    from app_pages.admin import render_admin_page
    render_admin_page()
