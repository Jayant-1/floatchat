"""
ARGO Floats Map Visualizer with Interactive Popups and Float Details Table
"""

import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
import numpy as np
from utils.ui_components import render_status_indicator, render_info_box, render_data_table
from data_generator import DataGenerator  # make sure your generator is imported

# --- Ocean bounding boxes ---
OCEAN_REGIONS = {
    "Indian Ocean": (-40, 30, 20, 120),
    "Atlantic": (-60, 60, -70, 20),
    "Pacific": (-60, 60, 120, -70)  # wraparound handled
}

def generate_ocean_points(n=50):
    """Generate floats only in ocean regions."""
    data = []
    regions = list(OCEAN_REGIONS.keys())
    for i in range(n):
        region = np.random.choice(regions)
        lat_min, lat_max, lon_min, lon_max = OCEAN_REGIONS[region]
        lat = np.random.uniform(lat_min, lat_max)
        if lon_max < lon_min:  # handle wrap
            if np.random.rand() > 0.5:
                lon = np.random.uniform(lon_min, 180)
            else:
                lon = np.random.uniform(-180, lon_max)
        else:
            lon = np.random.uniform(lon_min, lon_max)
        data.append({
            "float_id": f"F{1000+i}",
            "latitude": lat,
            "longitude": lon,
            "region": region,
            "status": np.random.choice(["Active", "Inactive", "Maintenance"]),
            "float_type": np.random.choice(["Core", "Bio", "Deep"]),
            "cycle_number": np.random.randint(0, 300),
            "max_depth": np.random.randint(1000, 3000),
            "institution": "INCOIS",
            "battery_level": np.random.randint(50, 100),
            "last_profile": pd.Timestamp.now().strftime("%Y-%m-%d"),
            "deployment_date": pd.Timestamp.now().strftime("%Y-%m-%d"),
            "temperature_range": "2-30°C",
            "salinity_range": "33-37 PSU"
        })
    return pd.DataFrame(data)


def render_map_page():
    """Render the ARGO floats interactive map with popups and details table."""

    st.markdown("## 🗺️ ARGO Floats Interactive Map")
    st.markdown("Explore global ARGO floats with clickable markers showing detailed information.")

    # --- Generate sample float data if not already ---
    if "float_locations" not in st.session_state:
        try:
            st.session_state.float_locations = st.session_state.data_generator.generate_float_locations(50)
        except AttributeError:
            # fallback to ocean-only generator
            st.session_state.float_locations = generate_ocean_points(50)

    float_data = st.session_state.float_locations

    # --- Filters ---
    st.markdown("### 🔍 Filter Floats")
    col1, col2, col3 = st.columns(3)
    with col1:
        selected_regions = st.multiselect(
            "Select Regions",
            options=float_data["region"].unique(),
            default=float_data["region"].unique()
        )
    with col2:
        selected_status = st.multiselect(
            "Float Status",
            options=float_data["status"].unique(),
            default=float_data["status"].unique()
        )
    with col3:
        selected_types = st.multiselect(
            "Float Types",
            options=float_data["float_type"].unique(),
            default=float_data["float_type"].unique()
        )

    filtered_data = float_data[
        (float_data["region"].isin(selected_regions)) &
        (float_data["status"].isin(selected_status)) &
        (float_data["float_type"].isin(selected_types))
    ]

    # --- Folium Map ---
    if filtered_data.empty:
        render_info_box("No Floats Found", "Adjust your filters to see floats on the map.", "warning")
        return

    center_lat = filtered_data["latitude"].mean()
    center_lon = filtered_data["longitude"].mean()

    # Dark mode map 🌑
    m = folium.Map(location=[center_lat, center_lon], zoom_start=2, tiles="CartoDB dark_matter")

    status_color = {"Active": "green", "Inactive": "red", "Maintenance": "orange"}

    for idx, row in filtered_data.iterrows():
        popup_html = f"""
        <div style="font-family: Arial; font-size: 13px; width: 220px;">
            <h4 style="margin-bottom:5px; color:#1f77b4">{row['float_id']}</h4>
            <p><b>Status:</b> {row['status']}</p>
            <p><b>Region:</b> {row['region']}</p>
            <p><b>Type:</b> {row['float_type']}</p>
            <p><b>Cycle:</b> {row['cycle_number']}</p>
            <p><b>Max Depth:</b> {row['max_depth']} m</p>
            <p><b>Battery:</b> {row['battery_level']}%</p>
            <p><b>Temperature:</b> {row['temperature_range']}</p>
            <p><b>Salinity:</b> {row['salinity_range']}</p>
        </div>
        """
        folium.CircleMarker(
            location=[row["latitude"], row["longitude"]],
            radius=6,
            fill=True,
            color="black",
            weight=1,
            fillColor=status_color.get(row["status"], "blue"),
            fill_opacity=0.8,
            popup=folium.Popup(popup_html, max_width=240),
            tooltip=row["float_id"]
        ).add_to(m)

    st_folium(m, width=900, height=500)

    # --- Data Table ---
    st.markdown("---")
    st.markdown("### 📋 ARGO Float Details Table")
    display_cols = ["float_id", "region", "latitude", "longitude", "status", "float_type", "cycle_number", "battery_level", "last_profile"]
    render_data_table(filtered_data[display_cols], "Filtered ARGO Floats")

    # --- Export Options ---
    st.markdown("#### Download Filtered Data")
    csv_export = filtered_data.to_csv(index=False)
    st.download_button(
        label="Download CSV",
        data=csv_export,
        file_name="argo_floats_filtered.csv",
        mime="text/csv"
    )
