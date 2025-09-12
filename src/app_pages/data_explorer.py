"""
Data Explorer & Query Interface page
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from utils.ui_components import render_data_table, render_info_box, render_chat_sidebar
from utils.config import DATA_CONFIG

def render_data_explorer_page():
    """Render the data explorer and query interface page"""
    
    # Render chat interface in sidebar
    render_chat_sidebar()
    
    st.markdown("## 📊 Data Explorer & Analysis Interface")
    st.markdown("Explore and analyze ARGO ocean data using advanced filters and quick analysis tools.")
    
    # Advanced Filter Interface
    st.markdown("### 🔧 Advanced Data Filters")
    
    # Create filter columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### Geographic Filters")
        
        # Region selection
        selected_regions = st.multiselect(
            "Ocean Regions",
            DATA_CONFIG["ocean_regions"],
            default=["Arabian Sea", "Bay of Bengal"]
        )
        
        # Coordinate ranges
        lat_range = st.slider(
            "Latitude Range",
            min_value=-90.0,
            max_value=90.0,
            value=(-10.0, 30.0),
            step=0.1
        )
        
        lon_range = st.slider(
            "Longitude Range", 
            min_value=-180.0,
            max_value=180.0,
            value=(40.0, 100.0),
            step=0.1
        )
    
    with col2:
        st.markdown("#### Parameter Filters")
        
        # Parameter selection
        selected_parameters = st.multiselect(
            "Parameters to Analyze",
            DATA_CONFIG["parameters"],
            default=["Temperature", "Salinity"]
        )
        
        # Depth range
        depth_range = st.select_slider(
            "Depth Range (m)",
            options=DATA_CONFIG["depth_ranges"],
            value=(0, 500)
        )
        
        # Date range
        date_range = st.date_input(
            "Date Range",
            value=(pd.to_datetime("2024-01-01"), pd.to_datetime("2025-09-11")),
            help="Select date range for data analysis"
        )
    
    with col3:
        st.markdown("#### Analysis Options")
        
        analysis_type = st.selectbox(
            "Analysis Type",
            ["Profile Analysis", "Time Series", "Regional Comparison", "Correlation Analysis", "Anomaly Detection"]
        )
        
        aggregation_method = st.selectbox(
            "Aggregation Method",
            ["Mean", "Median", "Max", "Min", "Standard Deviation"]
        )
        
        visualization_type = st.selectbox(
            "Visualization Type",
            ["Line Plot", "Heatmap", "Box Plot", "Scatter Plot", "Contour Plot"]
        )
    
    # Execute advanced query
    if st.button("📈 Generate Analysis", type="secondary"):
        execute_advanced_query(
            selected_regions, lat_range, lon_range, selected_parameters,
            depth_range, date_range, analysis_type, aggregation_method, visualization_type
        )
    
    st.markdown("---")
    
    # Quick Analysis Shortcuts
    st.markdown("### ⚡ Quick Analysis")
    
    quick_options = st.columns(4)
    
    with quick_options[0]:
        if st.button("🌡️ Temperature Overview", use_container_width=True):
            show_temperature_overview()
    
    with quick_options[1]:
        if st.button("🧂 Salinity Analysis", use_container_width=True):
            show_salinity_analysis()
    
    with quick_options[2]:
        if st.button("� Depth Profiles", use_container_width=True):
            show_depth_analysis()
    
    with quick_options[3]:
        if st.button("🌊 Regional Comparison", use_container_width=True):
            show_regional_comparison()

def execute_advanced_query(regions, lat_range, lon_range, parameters, depth_range, date_range, analysis_type, aggregation, viz_type):
    """Execute advanced query with filters"""
    
    st.markdown("### 📊 Advanced Analysis Results")
    
    with st.spinner("Generating analysis..."):
        import time
        time.sleep(1)
        
        # Generate sample data based on parameters
        if analysis_type == "Regional Comparison":
            show_regional_comparison_analysis(regions, parameters)
        elif analysis_type == "Time Series":
            show_time_series_analysis(parameters[0] if parameters else "Temperature")
        elif analysis_type == "Profile Analysis":
            show_profile_analysis(parameters)
        elif analysis_type == "Correlation Analysis":
            show_correlation_analysis(parameters)
        else:
            show_anomaly_detection(parameters[0] if parameters else "Temperature")

def show_temperature_overview():
    """Show temperature overview analysis"""
    st.markdown("### 🌡️ Temperature Overview")
    
    # Generate temperature data
    regions = ["Arabian Sea", "Bay of Bengal", "Indian Ocean"]
    temp_data = []
    
    for region in regions:
        temps = np.random.normal(25, 3, 100)
        for temp in temps:
            temp_data.append({"region": region, "temperature": temp})
    
    df = pd.DataFrame(temp_data)
    
    # Create visualization
    fig = px.box(df, x="region", y="temperature", title="Temperature Distribution by Region")
    st.plotly_chart(fig, use_container_width=True)
    
    # Summary statistics
    summary = df.groupby('region')['temperature'].agg(['mean', 'std', 'min', 'max']).round(2)
    render_data_table(summary.reset_index(), "Temperature Statistics by Region")

def show_salinity_analysis():
    """Show salinity analysis"""
    st.markdown("### 🧂 Salinity Analysis")
    
    # Generate depth vs salinity data
    depths = np.arange(0, 1000, 50)
    salinity = 35 + np.random.normal(0, 0.5, len(depths))
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=salinity, y=-depths, mode='lines+markers', name='Salinity Profile'))
    fig.update_layout(
        title="Salinity vs Depth Profile",
        xaxis_title="Salinity (PSU)",
        yaxis_title="Depth (m)",
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)

def show_depth_analysis():
    """Show depth profile analysis"""
    st.markdown("### � Depth Profile Analysis")
    
    # Generate temperature vs depth data for different regions
    depths = np.arange(0, 1000, 25)
    
    fig = go.Figure()
    
    # Arabian Sea profile
    temp_arabian = 28 * np.exp(-depths / 800) + 4 + np.random.normal(0, 0.5, len(depths))
    fig.add_trace(go.Scatter(x=temp_arabian, y=-depths, mode='lines', name='Arabian Sea', line=dict(color='red')))
    
    # Bay of Bengal profile  
    temp_bengal = 29 * np.exp(-depths / 750) + 3.5 + np.random.normal(0, 0.5, len(depths))
    fig.add_trace(go.Scatter(x=temp_bengal, y=-depths, mode='lines', name='Bay of Bengal', line=dict(color='blue')))
    
    fig.update_layout(
        title="Temperature vs Depth by Region",
        xaxis_title="Temperature (°C)",
        yaxis_title="Depth (m)",
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)

def show_regional_comparison():
    """Show regional comparison analysis"""
    st.markdown("### 🌊 Regional Comparison")
    
    # Generate comparison data
    comparison_data = st.session_state.data_generator.generate_comparison_data(
        ["Arabian Sea", "Bay of Bengal", "Indian Ocean"], "Temperature"
    )
    
    fig = px.violin(comparison_data, x="region", y="value", title="Temperature Distribution by Region")
    st.plotly_chart(fig, use_container_width=True)
    
    render_data_table(comparison_data.head(20), "Sample Comparison Data")

def show_regional_comparison_analysis(regions, parameters):
    """Show detailed regional comparison"""
    comparison_data = st.session_state.data_generator.generate_comparison_data(regions, parameters[0] if parameters else "Temperature")
    
    fig = px.box(comparison_data, x="region", y="value", title=f"{parameters[0] if parameters else 'Parameter'} Comparison Across Regions")
    st.plotly_chart(fig, use_container_width=True)
    
    render_data_table(comparison_data.head(50), f"{parameters[0] if parameters else 'Parameter'} Comparison Data")

def show_time_series_analysis(parameter):
    """Show time series analysis"""
    time_series_data = st.session_state.data_generator.generate_time_series_data(parameter, "Arabian Sea", 12)
    
    fig = px.line(time_series_data, x='date', y='value', title=f"{parameter} Time Series - Arabian Sea")
    st.plotly_chart(fig, use_container_width=True)

def show_profile_analysis(parameters):
    """Show profile analysis"""
    profile_data = st.session_state.data_generator.generate_profile_data("Sample_Float", 1000)
    
    fig = make_subplots(rows=1, cols=len(parameters), subplot_titles=parameters)
    
    for i, param in enumerate(parameters):
        if param.lower() in profile_data.columns:
            fig.add_trace(
                go.Scatter(x=profile_data[param.lower()], y=-profile_data['depth'], mode='lines', name=param),
                row=1, col=i+1
            )
    
    fig.update_layout(height=400, title="Multi-Parameter Profile Analysis")
    st.plotly_chart(fig, use_container_width=True)

def show_correlation_analysis(parameters):
    """Show correlation analysis"""
    if len(parameters) >= 2:
        # Generate correlation data
        n = 100
        data = {}
        for param in parameters:
            data[param] = np.random.randn(n)
        
        df = pd.DataFrame(data)
        corr_matrix = df.corr()
        
        fig = px.imshow(corr_matrix, title="Parameter Correlation Matrix", aspect="auto")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Please select at least 2 parameters for correlation analysis.")

def show_anomaly_detection(parameter):
    """Show anomaly detection analysis"""
    dates = pd.date_range('2024-01-01', periods=100, freq='D')
    values = np.random.randn(100) * 2 + 25
    
    # Add some anomalies
    anomalies = np.random.choice(100, 5, replace=False)
    values[anomalies] += np.random.choice([-1, 1], 5) * np.random.uniform(5, 10, 5)
    
    df = pd.DataFrame({'date': dates, 'value': values})
    df['is_anomaly'] = False
    for idx in anomalies:
        df.at[idx, 'is_anomaly'] = True
    
    fig = px.scatter(df, x='date', y='value', color='is_anomaly', 
                     title=f"{parameter} Anomaly Detection",
                     color_discrete_map={True: 'red', False: 'blue'})
    st.plotly_chart(fig, use_container_width=True)
    
    st.info(f"Detected {len(anomalies)} anomalies in {parameter} data.")
