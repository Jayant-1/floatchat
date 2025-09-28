import streamlit as st
import pydeck as pdk
import pandas as pd

st.title("FloatChat 3D Globe Preview")

data = pd.DataFrame({
    "latitude": [10, -20, 30],
    "longitude": [50, 80, -60],
    "status": ["Active", "Inactive", "Maintenance"],
    "float_id": ["F001", "F002", "F003"],
    "color": [[0,200,0], [200,0,0], [255,165,0]],
    "radius": [50000, 50000, 50000]
})

scatter_layer = pdk.Layer(
    "ScatterplotLayer",
    data=data,
    get_position=["longitude", "latitude"],
    get_color="color",
    get_radius="radius",
    pickable=True,
    elevation_scale=0
)

deck = pdk.Deck(
    layers=[scatter_layer],
    initial_view_state=pdk.ViewState(latitude=0, longitude=0, zoom=0),
    views=[pdk.View(type="GlobeView", controller=True)],
    tooltip={"text": "{float_id}\nStatus: {status}"}
)

st.pydeck_chart(deck, use_container_width=True)
