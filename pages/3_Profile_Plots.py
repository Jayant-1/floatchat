import time

import numpy as np
import plotly.graph_objects as go
import streamlit as st

st.title("📈 Profile Plots")

filters = st.session_state.get("filters", None)
variable = (filters["variable"] if filters else "Temperature")
max_depth = (filters["depth"] if filters else 2000)

# UI mirrors global state for clarity
col1, col2 = st.columns([1, 2])
with col1:
    st.caption(f"Variable: {variable}")
with col2:
    depth_range = st.slider("Depth range (m)", min_value=0, max_value=int(max_depth), value=(0, int(max_depth)), step=50)

# Mock profile data based on selected variable
np.random.seed(3)
depth = np.linspace(depth_range[0], depth_range[1], 150)
if variable.startswith("Temperature"):
    x = 20 - 0.015 * depth + np.random.normal(0, 0.05, size=depth.size)
    x_label = "Temperature (°C)"
    color = "#22d3ee"
elif variable.startswith("Salinity"):
    x = 35 - 0.001 * depth + np.random.normal(0, 0.01, size=depth.size)
    x_label = "Salinity (PSU)"
    color = "#14b8a6"
elif variable.startswith("Oxygen"):
    x = 7 - 0.002 * depth + np.random.normal(0, 0.02, size=depth.size)
    x_label = "Oxygen (mg/L)"
    color = "#60a5fa"
else:
    x = 2 + 0.0005 * depth + np.random.normal(0, 0.02, size=depth.size)
    x_label = "Chl-a (mg/m³)"
    color = "#22c55e"

fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=depth, mode="lines", line=dict(color=color, width=3)))
fig.update_yaxes(autorange="reversed", title_text="Depth (m)")
fig.update_xaxes(title_text=x_label)
fig.update_layout(template="plotly_dark", paper_bgcolor="#0f172a", plot_bgcolor="#0b1220", height=520, margin=dict(l=40, r=20, t=20, b=40))

placeholder = st.empty()

colA, colB = st.columns([1, 1])
with colA:
    animate = st.button("Animate profile", help="Progressively draw the line", type="primary")
with colB:
    st.caption("Filters update the plot instantly; use Animate for a transition.")

if animate or st.session_state.get("_animate_on_filter_change", False):
    st.session_state["_animate_on_filter_change"] = False
    for i in range(5, len(depth) + 1, 5):
        f = go.Figure()
        f.add_trace(go.Scatter(x=x[:i], y=depth[:i], mode="lines", line=dict(color=color, width=3)))
        f.update_yaxes(autorange="reversed", title_text="Depth (m)")
        f.update_xaxes(title_text=x_label)
        f.update_layout(template="plotly_dark", paper_bgcolor="#0f172a", plot_bgcolor="#0b1220", height=520, margin=dict(l=40, r=20, t=20, b=40))
        placeholder.plotly_chart(f, use_container_width=True)
        time.sleep(0.02)
else:
    placeholder.plotly_chart(fig, use_container_width=True) 