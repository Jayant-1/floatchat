"""
Reusable UI components for FloatChat Streamlit application
"""

import streamlit as st
from utils.config import NAVIGATION, THEME_CONFIG
from datetime import datetime

def render_header():
    """Render the main header with branding"""
    st.markdown("""
    <div class="main-header">
        <h1>🌊 FloatChat</h1>
        <h3>Conversational AI for ARGO Ocean Data</h3>
        <p><em>Smart India Hackathon 2025</em></p>
    </div>
    """, unsafe_allow_html=True)

def render_sidebar():
    """Render empty sidebar and return selected page"""
    # Keep sidebar completely empty
    with st.sidebar:
        st.empty()  # Ensure sidebar is empty
    
    # Default to Home page - no navigation buttons
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Home"
    
    return st.session_state.current_page

def render_metric_cards(metrics_data):
    """Render metric cards in a grid layout"""
    cols = st.columns(len(metrics_data))
    
    for i, (title, value, delta, help_text) in enumerate(metrics_data):
        with cols[i]:
            st.metric(
                label=title,
                value=value,
                delta=delta,
                help=help_text
            )

def render_feature_card(title, description, icon, color_gradient="135deg, #667eea 0%, #764ba2 100%"):
    """Render a feature highlight card"""
    st.markdown(f"""
    <div style="
        background: linear-gradient({color_gradient});
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    ">
        <h2 style="margin: 0; font-size: 2em;">{icon}</h2>
        <h3 style="margin: 0.5rem 0;">{title}</h3>
        <p style="margin: 0; opacity: 0.9;">{description}</p>
    </div>
    """, unsafe_allow_html=True)

def render_chat_message(message, is_user=False):
    """Render a chat message with appropriate styling"""
    if is_user:
        st.markdown(f"""
        <div class="chat-message user-message">
            <strong>You:</strong> {message}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-message bot-message">
            <strong>🤖 FloatChat:</strong> {message}
        </div>
        """, unsafe_allow_html=True)

def render_data_table(df, title="Data Table", max_height=400):
    """Render a styled data table"""
    st.subheader(title)
    st.dataframe(
        df,
        use_container_width=True,
        height=max_height
    )

def render_info_box(title, content, box_type="info"):
    """Render an information box"""
    if box_type == "info":
        st.info(f"**{title}**\n\n{content}")
    elif box_type == "success":
        st.success(f"**{title}**\n\n{content}")
    elif box_type == "warning":
        st.warning(f"**{title}**\n\n{content}")
    elif box_type == "error":
        st.error(f"**{title}**\n\n{content}")

def render_download_button(data, filename, label="Download Data", file_format="csv"):
    """Render a download button for data"""
    if file_format == "csv":
        csv_data = data.to_csv(index=False)
        st.download_button(
            label=label,
            data=csv_data,
            file_name=filename,
            mime="text/csv"
        )
    elif file_format == "json":
        json_data = data.to_json(orient='records', indent=2)
        st.download_button(
            label=label,
            data=json_data,
            file_name=filename,
            mime="application/json"
        )

def render_loading_spinner(text="Loading..."):
    """Render a loading spinner"""
    with st.spinner(text):
        import time
        time.sleep(1)  # Simulate loading

def render_progress_bar(progress_value, text="Processing..."):
    """Render a progress bar"""
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i in range(progress_value + 1):
        progress_bar.progress(i)
        status_text.text(f'{text} {i}%')
    
    return progress_bar

def render_expandable_section(title, content, expanded=False):
    """Render an expandable section"""
    with st.expander(title, expanded=expanded):
        st.markdown(content)

def render_tabs(tab_names, tab_contents):
    """Render tabbed content"""
    tabs = st.tabs(tab_names)
    
    for i, (tab, content) in enumerate(zip(tabs, tab_contents)):
        with tab:
            content()

def render_status_indicator(status, label="Status"):
    """Render a status indicator"""
    color_map = {
        "Active": "🟢",
        "Inactive": "🔴", 
        "Maintenance": "🟡",
        "Unknown": "⚪"
    }
    
    indicator = color_map.get(status, "⚪")
    st.markdown(f"**{label}:** {indicator} {status}")

def render_filter_sidebar():
    """Render filter controls in sidebar"""
    st.sidebar.markdown("### 🔍 Filters")
    
    # Date range filter
    date_range = st.sidebar.date_input(
        "Date Range",
        value=(datetime(2024, 1, 1), datetime.now()),
        help="Select date range for data filtering"
    )
    
    # Region filter
    regions = st.sidebar.multiselect(
        "Ocean Regions",
        ["Arabian Sea", "Bay of Bengal", "Indian Ocean", "Pacific Ocean", "Atlantic Ocean"],
        default=["Arabian Sea", "Bay of Bengal"],
        help="Select ocean regions to include"
    )
    
    # Parameter filter
    parameters = st.sidebar.multiselect(
        "Parameters",
        ["Temperature", "Salinity", "Depth", "Location"],
        default=["Temperature", "Salinity"],
        help="Select parameters to analyze"
    )
    
    # Depth range filter
    depth_range = st.sidebar.slider(
        "Depth Range (m)",
        min_value=0,
        max_value=2000,
        value=(0, 500),
        step=50,
        help="Select depth range for analysis"
    )
    
    return {
        "date_range": date_range,
        "regions": regions,
        "parameters": parameters,
        "depth_range": depth_range
    }

def render_chat_sidebar():
    """Render chat interface in sidebar with same functionality as chat page"""
    import time
    import random
    from utils.config import CHATBOT_CONFIG
    
    def should_show_navigation_buttons(response_content):
        """Determine if navigation buttons should be shown based on response content"""
        data_keywords = [
            "temperature", "salinity", "depth", "location", "data", "analysis", "visualization", 
            "profile", "regional", "trends", "patterns", "floats", "arabian sea", 
            "bay of bengal", "indian ocean", "compare", "explore", "show", "map", "latitude", "longitude"
        ]
        content_lower = response_content.lower()
        return any(keyword in content_lower for keyword in data_keywords)

    def display_sidebar_message(message, show_timestamps=True):
        """Display a chat message with styling in sidebar"""
        
        is_user = message["role"] == "user"
        content = message["content"]
        timestamp = message["timestamp"]
        
        # Create message container with smaller styling for sidebar
        if is_user:
            st.markdown(f"""
            <div style="
                background-color: #e3f2fd;
                padding: 0.5rem;
                border-radius: 8px 8px 2px 8px;
                margin: 0.25rem 0;
                border-left: 3px solid #1976d2;
                font-size: 0.85rem;
            ">
                <strong>You:</strong> {content}
                {f'<br><small style="color: #666;">{timestamp.strftime("%H:%M")}</small>' if show_timestamps else ''}
            </div>
            """, unsafe_allow_html=True)
        else:
            # Bot message with more features
            st.markdown(f"""
            <div style="
                background-color: #f5f5f5;
                padding: 0.5rem;
                border-radius: 8px 8px 8px 2px;
                margin: 0.25rem 0;
                border-left: 3px solid #4caf50;
                font-size: 0.85rem;
            ">
                <strong>🤖 FloatChat:</strong> {content}
                {f'<br><small style="color: #666;">{timestamp.strftime("%H:%M")}</small>' if show_timestamps else ''}
            </div>
            """, unsafe_allow_html=True)
            
            # Add navigation buttons for data-related responses
            if should_show_navigation_buttons(content):
                # Add CSS to make buttons shorter and stick together on left for sidebar
                st.markdown("""
                <style>
                .sidebar-nav-buttons-container {
                    display: flex !important;
                    gap: 0px !important;
                    justify-content: flex-start !important;
                    margin: 0rem 0 !important;
                }
                .sidebar-nav-buttons-container .stButton > button {
                    height: 1.8rem !important;
                    padding: 0.2rem 0.5rem !important;
                    font-size: 0.75rem !important;
                    margin: 0 !important;
                    width: auto !important;
                    min-width: auto !important;
                    margin-right: 1px !important;
                }
                .sidebar-nav-buttons-container .stButton {
                    margin-right: 0 !important;
                    margin-left: 0 !important;
                }
                </style>
                """, unsafe_allow_html=True)
                
                # Create container div and use very tight columns for sidebar
                st.markdown('<div class="sidebar-nav-buttons-container">', unsafe_allow_html=True)
                col1, col2 = st.columns([1, 1], gap="small")
                
                with col1:
                    if st.button("🗺️ Map", key=f"sidebar_map_{timestamp}", type="secondary"):
                        st.session_state.current_page = "ARGO Floats Map"
                        st.rerun()
                with col2:
                    if st.button("📊 Data", key=f"sidebar_data_{timestamp}", type="secondary"):
                        st.session_state.current_page = "Data Explorer"
                        st.rerun()
                
                st.markdown('</div>', unsafe_allow_html=True)

    def process_sidebar_user_message(user_input):
        """Process user message and generate bot response for sidebar chat"""
        from app_pages.chatbot import generate_bot_response
        
        # Add user message to history
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_input,
            "timestamp": datetime.now()
        })
        
        # Generate bot response
        bot_response = generate_bot_response(user_input)
        
        # Add bot response to history
        st.session_state.chat_history.append({
            "role": "assistant", 
            "content": bot_response,
            "timestamp": datetime.now()
        })
        
        # Limit chat history size
        if len(st.session_state.chat_history) > CHATBOT_CONFIG["max_chat_history"]:
            st.session_state.chat_history = st.session_state.chat_history[-CHATBOT_CONFIG["max_chat_history"]:]

    # Set sidebar to expanded by default
    st.sidebar.markdown("### 💬 FloatChat AI")
    
    # Add custom CSS for blue send button in sidebar
    st.sidebar.markdown("""
    <style>
    /* Custom blue styling for sidebar send buttons */
    .stSidebar .stForm button[kind="secondaryFormSubmit"] {
        background-color: #1f77b4 !important;
        border-color: #1f77b4 !important;
        color: white !important;
    }
    .stSidebar .stForm button[kind="secondaryFormSubmit"]:hover {
        background-color: #1565c0 !important;
        border-color: #1565c0 !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize chat history if not exists
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = [
            {"role": "assistant", "content": CHATBOT_CONFIG["welcome_message"], "timestamp": datetime.now()}
        ]
    
    # Display chat history in sidebar
    chat_container = st.sidebar.container()
    with chat_container:
        # Limit displayed messages to last 5 to avoid sidebar overflow
        recent_messages = st.session_state.chat_history[-5:]
        for message in recent_messages:
            display_sidebar_message(message, show_timestamps=True)
    
    # Chat input form in sidebar
    with st.sidebar.form(key="sidebar_chat_form", clear_on_submit=True):
        user_input = st.text_input(
            "Message", 
            placeholder="Ask about ARGO data...",
            key="sidebar_user_input_form",
            label_visibility="collapsed"
        )
        
        # Send button with blue styling (same as main chat)
        submitted = st.form_submit_button("➤ Send Message", type="secondary")
        
        if submitted and user_input:
            process_sidebar_user_message(user_input)
            st.rerun()
