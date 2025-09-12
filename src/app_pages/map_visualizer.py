"""
ARGO Floats Map Visualizer page
"""

import streamlit as st
import folium
from streamlit_folium import st_folium
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from utils.ui_components import render_data_table, render_info_box, render_status_indicator, render_chat_sidebar

def render_map_page():
    """Render the ARGO floats map visualizer page"""
    
    # Render chat interface in sidebar
    render_chat_sidebar()
    
    # Add page-specific CSS to prevent overflow
    st.markdown("""
    <style>
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        max-width: 100%;
    }
    .stSidebar .sidebar-content {
        max-height: calc(100vh - 100px);
        overflow-y: auto;
    }
    .element-container {
        margin-bottom: 1rem;
    }
    .metric-container {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #1f77b4;
        margin-bottom: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("## 🗺️ ARGO Floats Global Map")
    st.markdown("Explore the worldwide network of ARGO floats with interactive mapping and detailed profiles.")
    
    # Generate float data
    if 'float_locations' not in st.session_state:
        st.session_state.float_locations = st.session_state.data_generator.generate_float_locations(50)
    
    float_data = st.session_state.float_locations
    
    # Horizontal filters at the top
    st.markdown("### 🔍 Map Filters")
    
    # Create three columns for horizontal filter layout
    filter_col1, filter_col2, filter_col3 = st.columns(3)
    
    with filter_col1:
        # Region filter
        selected_regions = st.multiselect(
            "Select Regions",
            options=float_data['region'].unique(),
            default=float_data['region'].unique()[:3],
            help="Filter floats by ocean region"
        )
    
    with filter_col2:
        # Status filter
        selected_status = st.multiselect(
            "Float Status",
            options=float_data['status'].unique(),
            default=float_data['status'].unique(),
            help="Filter by operational status"
        )
    
    with filter_col3:
        # Float type filter
        selected_types = st.multiselect(
            "Float Types",
            options=float_data['float_type'].unique(),
            default=float_data['float_type'].unique(),
            help="Filter by float type/model"
        )
    
    # Add spacing after filters
    st.markdown("---")
    
    # Apply filters
    filtered_data = float_data[
        (float_data['region'].isin(selected_regions)) &
        (float_data['status'].isin(selected_status)) &
        (float_data['float_type'].isin(selected_types))
    ]
    
    # Main content area - single column since statistics removed
    st.markdown("### 🌍 Interactive Map")
    
    # Add custom CSS for map container
    st.markdown("""
    <style>
    .map-container {
        border: 2px solid #e0e0e0;
        border-radius: 12px;
        padding: 10px;
        background: white;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        overflow: hidden;
    }
    .folium-map {
        border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Create folium map
    center_lat = filtered_data['latitude'].mean()
    center_lon = filtered_data['longitude'].mean()
    
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=3,
        tiles='OpenStreetMap'
    )
        
    # Add float markers
    for idx, float_info in filtered_data.iterrows():
        # Color based on status
        color_map = {'Active': 'green', 'Inactive': 'red', 'Maintenance': 'orange'}
        color = color_map.get(float_info['status'], 'blue')
        
        # Create compact popup content
        popup_content = f"""
        <div style="font-family: Arial; width: 180px; font-size: 12px;">
            <h4 style="margin: 0 0 8px 0; color: #1f77b4;">{float_info['float_id']}</h4>
            <p style="margin: 2px 0;"><b>Status:</b> {float_info['status']}</p>
            <p style="margin: 2px 0;"><b>Region:</b> {float_info['region']}</p>
            <p style="margin: 2px 0;"><b>Cycle:</b> {float_info['cycle_number']}</p>
            <p style="margin: 2px 0;"><b>Max Depth:</b> {float_info['max_depth']}m</p>
        </div>
        """
        
        folium.CircleMarker(
            location=[float_info['latitude'], float_info['longitude']],
            radius=6,
            popup=folium.Popup(popup_content, max_width=200),
            color='black',
            weight=1,
            fillColor=color,
            fillOpacity=0.7,
            tooltip=f"Float {float_info['float_id']}"
        ).add_to(m)
        
        # Add improved legend with proper styling
        legend_html = '''
        <div style="position: fixed; 
                    bottom: 50px; left: 50px; width: 140px; height: 110px; 
                    background-color: rgba(255,255,255,0.95); 
                    border: 2px solid #1f77b4; 
                    border-radius: 8px;
                    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
                    z-index: 9999; 
                    font-size: 12px; 
                    padding: 12px;
                    font-family: Arial, sans-serif;">
        <p style="margin: 0 0 8px 0; font-weight: bold; color: #1f77b4; font-size: 13px;">Float Status</p>
        <p style="margin: 3px 0; display: flex; align-items: center;">
            <span style="display: inline-block; width: 12px; height: 12px; background-color: green; border-radius: 50%; margin-right: 8px;"></span>
            <span style="font-size: 11px;">Active</span>
        </p>
        <p style="margin: 3px 0; display: flex; align-items: center;">
            <span style="display: inline-block; width: 12px; height: 12px; background-color: red; border-radius: 50%; margin-right: 8px;"></span>
            <span style="font-size: 11px;">Inactive</span>
        </p>
        <p style="margin: 3px 0; display: flex; align-items: center;">
            <span style="display: inline-block; width: 12px; height: 12px; background-color: orange; border-radius: 50%; margin-right: 8px;"></span>
            <span style="font-size: 11px;">Maintenance</span>
        </p>
        </div>
        '''
        m.get_root().add_child(folium.Element(legend_html))
        
    # Display map with container styling
    with st.container():
        map_data = st_folium(m, width=700, height=500, returned_objects=["last_clicked"])
    
    # Handle map clicks
    selected_float = None
    if map_data['last_clicked'] is not None:
        clicked_lat = map_data['last_clicked']['lat']
        clicked_lng = map_data['last_clicked']['lng']
        
        # Find nearest float
        distances = ((filtered_data['latitude'] - clicked_lat)**2 + 
                    (filtered_data['longitude'] - clicked_lng)**2)
        nearest_idx = distances.idxmin()
        selected_float = filtered_data.loc[nearest_idx]
    
    # Selected float details and profile
    if selected_float is not None:
        st.markdown("---")
        st.markdown(f"### 📍 Selected Float: {selected_float['float_id']}")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### Float Information")
            st.write(f"**Location:** {selected_float['latitude']:.4f}°, {selected_float['longitude']:.4f}°")
            st.write(f"**Region:** {selected_float['region']}")
            st.write(f"**Type:** {selected_float['float_type']}")
            render_status_indicator(selected_float['status'])
            st.write(f"**Institution:** {selected_float['institution']}")
            st.write(f"**Cycle:** {selected_float['cycle_number']}")
            
        with col2:
            st.markdown("#### Technical Details")
            st.write(f"**Deployment:** {selected_float['deployment_date']}")
            st.write(f"**Last Profile:** {selected_float['last_profile']}")
            st.write(f"**Max Depth:** {selected_float['max_depth']} m")
            st.write(f"**Battery:** {selected_float['battery_level']}%")
            
        with col3:
            st.markdown("#### Data Ranges")
            st.write(f"**Temperature:** {selected_float['temperature_range']}")
            st.write(f"**Salinity:** {selected_float['salinity_range']}")
        
        # Generate and display profile data
        profile_data = st.session_state.data_generator.generate_profile_data(
            selected_float['float_id'], 
            selected_float['max_depth']
        )
        
        st.markdown("#### Oceanographic Profile")
        
        # Create subplots for profile visualization (only Temperature and Salinity)
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Temperature (°C)', 'Salinity (PSU)'),
            shared_yaxes=True
        )
        
        # Temperature profile
        fig.add_trace(
            go.Scatter(x=profile_data['temperature'], y=-profile_data['depth'],
                      mode='lines', name='Temperature', line=dict(color='red')),
            row=1, col=1
        )
        
        # Salinity profile
        fig.add_trace(
            go.Scatter(x=profile_data['salinity'], y=-profile_data['depth'],
                      mode='lines', name='Salinity', line=dict(color='blue')),
            row=1, col=2
        )
        
        fig.update_layout(
            height=400,
            title_text=f"Oceanographic Profile - {selected_float['float_id']}",
            showlegend=False
        )
        fig.update_yaxes(title_text="Depth (m)", row=1, col=1)
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Trajectory data
        st.markdown("#### Recent Trajectory")
        trajectory_data = st.session_state.data_generator.generate_trajectory_data(selected_float['float_id'])
        
        # Plot trajectory
        fig_traj = px.line_mapbox(
            trajectory_data,
            lat="latitude",
            lon="longitude",
            title=f"30-Day Trajectory for {selected_float['float_id']}",
            mapbox_style="open-street-map",
            height=300
        )
        fig_traj.update_layout(mapbox_center={"lat": selected_float['latitude'], "lon": selected_float['longitude']})
        fig_traj.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
        
        st.plotly_chart(fig_traj, use_container_width=True)
        
        # Data download options
        st.markdown("#### Download Data")
        col1, col2 = st.columns(2)
        
        with col1:
            csv_data = profile_data.to_csv(index=False)
            st.download_button(
                label="Download Profile Data (CSV)",
                data=csv_data,
                file_name=f"{selected_float['float_id']}_profile.csv",
                mime="text/csv"
            )
        
        with col2:
            traj_csv = trajectory_data.to_csv(index=False)
            st.download_button(
                label="Download Trajectory Data (CSV)",
                data=traj_csv,
                file_name=f"{selected_float['float_id']}_trajectory.csv",
                mime="text/csv"
            )
    
    else:
        render_info_box(
            "Select a Float",
            "Click on any float marker on the map to view detailed profile data and trajectory information.",
            "info"
        )
    
    # Data table
    st.markdown("---")
    st.markdown("### 📋 Float Details Table")
    
    # Display filtered data table
    display_columns = ['float_id', 'region', 'latitude', 'longitude', 'status', 
                      'float_type', 'cycle_number', 'battery_level', 'last_profile']
    render_data_table(filtered_data[display_columns], "Filtered ARGO Floats")
    
    # Export options
    st.markdown("#### Export Options")
    col1, col2 = st.columns(2)
    
    with col1:
        csv_export = filtered_data.to_csv(index=False)
        st.download_button(
            label="Download Filtered Data (CSV)",
            data=csv_export,
            file_name="argo_floats_filtered.csv",
            mime="text/csv"
        )
    
    with col2:
        if st.button("🔄 Refresh Data"):
            del st.session_state.float_locations
            st.rerun()
