"""
Home page for FloatChat application
"""

import streamlit as st
from utils.ui_components import render_feature_card, render_metric_cards, render_info_box

def render_home_page():
    """Render the home/overview page"""
    
    # Project introduction
    st.markdown("""
    ## 🌊 Welcome to FloatChat
    
    **Advanced ARGO Ocean Data Analysis Platform** - A streamlined platform that provides powerful 
    tools for exploring and analyzing oceanographic data from the global ARGO float network.
    
    ### 🎯 Project Overview
    
    FloatChat focuses on four core oceanographic parameters: **Temperature**, **Salinity**, **Depth**, 
    and **Location**. Our platform provides interactive mapping, advanced filtering, and AI-powered 
    insights to make ARGO float data accessible for researchers, policymakers, and ocean enthusiasts.
    """)
    
    # Key metrics
    st.markdown("### 📊 Platform Statistics")
    metrics_data = [
        ("Active ARGO Floats", "3,847", "", "Total number of operational ARGO floats"),
        ("Core Parameters", "4", "", "Essential oceanographic measurements"),
        ("Ocean Regions", "7", "", "Major ocean regions monitored"),
        ("Analysis Tools", "3", "", "Interactive analysis interfaces")
    ]
    render_metric_cards(metrics_data)
    
    # Feature highlights
    st.markdown("### 🚀 Key Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        render_feature_card(
            "Interactive Mapping",
            "Explore ARGO floats across global oceans with streamlined popups and real-time positioning",
            "🗺️",
            "135deg, #1f77b4 0%, #00cc96 100%"
        )
        
        render_feature_card(
            "Advanced Data Filters",
            "Filter and analyze oceanographic data using geographic, parameter, and temporal controls",
            "🔎",
            "135deg, #ff7f0e 0%, #d62728 100%"
        )
    
    with col2:
        render_feature_card(
            "Core Parameter Analysis",
            "Focus on Temperature, Salinity, Depth, and Location for comprehensive ocean insights",
            "📈",
            "135deg, #2ca02c 0%, #bcbd22 100%"
        )
        
        render_feature_card(
            "AI-Powered Chat",
            "Get intelligent responses about ocean data patterns and specific float information",
            "💬",
            "135deg, #9467bd 0%, #8c564b 100%"
        )
    
    # Impact and applications
    st.markdown("### 🌍 Impact & Applications")
    
    tab1, tab2, tab3 = st.tabs(["🔬 Research", "🏛️ Policy", "📚 Education"])
    
    with tab1:
        st.markdown("""
        #### Climate Research Applications
        
        - **Temperature Analysis**: Track ocean temperature variations and thermal profiles across depths
        - **Salinity Monitoring**: Study ocean circulation patterns through salinity gradients  
        - **Depth Profiling**: Analyze vertical water column structure and stratification
        - **Location-Based Studies**: Compare regional oceanographic patterns and trends
        
        > *"FloatChat's focused approach on core parameters has streamlined our research 
        > workflow, allowing us to concentrate on essential oceanographic variables."*
        > 
        > — Dr. Marine Scientist, INCOIS
        """)
    
    with tab2:
        st.markdown("""
        #### Policy & Decision Making
        
        - **Marine Environment Assessment**: Use temperature and salinity data for ecosystem evaluation
        - **Fisheries Management**: Optimize fishing zones based on core oceanographic conditions
        - **Coastal Planning**: Inform infrastructure development with depth and location data
        - **Regional Monitoring**: Track ocean health through essential parameter analysis
        
        > *"The streamlined interface focusing on key parameters makes it easier for 
        > policy makers to understand and act on oceanographic data."*
        > 
        > — Policy Analyst, Ministry of Earth Sciences
        """)
    
    with tab3:
        st.markdown("""
        #### Educational Impact
        
        - **Core Parameter Learning**: Focus on essential oceanographic variables for better understanding
        - **Interactive Mapping**: Engage students with location-based ocean data exploration
        - **Data Analysis Skills**: Teach filtering and visualization through hands-on experience
        - **Regional Comparisons**: Compare temperature, salinity, and depth patterns across locations
        
        > *"Students can now focus on the most important oceanographic parameters, 
        > building a solid foundation in marine science fundamentals."*
        > 
        > — Professor, IIT Mumbai Ocean Engineering
        """)
    
    # Recent updates and news
    st.markdown("### 📰 Recent Updates")
    
    with st.expander("🆕 Latest Updates", expanded=True):
        st.markdown("""
        - **September 2025**: Streamlined application to focus on 4 core parameters (Temperature, Salinity, Depth, Location)
        - **September 2025**: Removed natural language queries for simplified data exploration experience
        - **September 2025**: Enhanced map interface with compact float popups and removed statistics panel
        - **September 2025**: Updated data explorer with advanced filters and quick analysis tools
        - **September 2025**: Improved chatbot responses focused on core oceanographic parameters
        """)
    
    # Call to action
    st.markdown("### 🎯 Ready to Explore?")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🗺️ Explore Map", use_container_width=True):
            st.session_state.current_page = "ARGO Floats Map"
            st.rerun()
    
    with col2:
        if st.button("📊 Query Data", use_container_width=True):
            st.session_state.current_page = "Data Explorer"
            st.rerun()
    
    with col3:
        if st.button("🤖 Chat with AI", use_container_width=True):
            st.session_state.current_page = "FloatChat AI"
            st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p><strong>FloatChat</strong> - Developed for Smart India Hackathon 2025</p>
        <p>🌊 Making Ocean Data Accessible to Everyone 🌊</p>
    </div>
    """, unsafe_allow_html=True)
