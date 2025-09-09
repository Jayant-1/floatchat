import time
from datetime import datetime, UTC

import numpy as np
import pandas as pd
import pydeck as pdk
import streamlit as st

st.title("🗺️ Map Explorer")

# Read global filters
filters = st.session_state.get("filters", None)
region = filters["region"] if filters else "Global"
# Derive days from date range
if filters:
    days = (filters["date_end"] - filters["date_start"]).days or 1
else:
    days = 60

# Generate mock ARGO float points with proper datetime
np.random.seed(7)
N = 300
now = datetime.now(UTC)
start = now - pd.Timedelta(days=days)

lats = np.random.uniform(-70, 70, size=N)
lons = np.random.uniform(-180, 180, size=N)
rand = np.random.rand(N)
when = pd.to_datetime(start) + pd.to_timedelta((now - start).total_seconds() * rand, unit="s")
ids = np.arange(N)

df = pd.DataFrame({"id": ids, "lat": lats, "lon": lons, "time": when})

# Region filter (simple bounding boxes for demo)
boxes = {
    "North Atlantic": ((0, -80), (70, 20)),
    "South Atlantic": ((-70, -60), (0, 20)),
    "Atlantic": ((-70, -80), (70, 20)),
    "North Pacific": ((0, 120), (70, -120)),
    "South Pacific": ((-70, 120), (0, -120)),
    "Pacific": ((-70, 120), (70, -120)),
    "Indian": ((-50, 20), (30, 120)),
    "Southern": ((-90, -180), (-50, 180)),
}
if region != "Global":
    key = region
    (lat0, lon0), (lat1, lon1) = boxes[key]
    df = df[(df.lat.between(lat0, lat1)) & (df.lon.apply(lambda x: (x >= lon0) if lon0 <= lon1 else (x >= lon0 or x <= lon1)))]

# Pydeck dark-themed layer with hover auto highlight and glow
layer = pdk.Layer(
    "ScatterplotLayer",
    data=df,
    get_position='[lon, lat]',
    get_radius=25000,
    get_fill_color=[34, 211, 238, 140],
    get_line_color=[34, 211, 238],
    line_width_min_pixels=1,
    stroked=True,
    pickable=True,
    auto_highlight=True,
)

view_state = pdk.ViewState(latitude=0, longitude=0, zoom=1.1)

tooltip = {
    "html": "<b>Float</b> {id}<br/><b>Lat</b> {lat}<br/><b>Lon</b> {lon}<br/><b>Time</b> {time}",
    "style": {"backgroundColor": "rgba(2,6,23,0.95)", "color": "#e5f9ff"},
}

deck = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    map_style="mapbox://styles/mapbox/dark-v11",
    tooltip=tooltip,
)

placeholder = st.empty()
with placeholder.container():
    st.pydeck_chart(deck, use_container_width=True)

st.caption("Hover a float to glow-highlight. Filters in the sidebar update this map.") 