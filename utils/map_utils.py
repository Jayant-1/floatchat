"""
Enhanced map utilities for interactive ARGO float visualization
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional

class MapGenerator:
    """Generate interactive maps for ARGO float data"""
    
    def __init__(self):
        self.status_colors = {
            "Active": "#10B981",      # Green
            "Inactive": "#EF4444",    # Red
            "Maintenance": "#F59E0B", # Orange
            "Deployed": "#3B82F6"     # Blue
        }
        
        self.region_colors = {
            "Arabian Sea": "#EF4444",
            "Bay of Bengal": "#3B82F6", 
            "Indian Ocean": "#10B981",
            "Pacific Ocean": "#8B5CF6",
            "Atlantic Ocean": "#F59E0B",
            "Southern Ocean": "#EC4899",
            "Arctic Ocean": "#6B7280"
        }
    
    def generate_interactive_map(self, data: pd.DataFrame, color_by: str = "status") -> go.Figure:
        """Generate interactive map with float locations"""
        if data.empty:
            return self._create_empty_map()
        
        # Choose color scheme
        if color_by == "status":
            colors = [self.status_colors.get(status, "#6B7280") for status in data["status"]]
            color_title = "Float Status"
        elif color_by == "region":
            colors = [self.region_colors.get(region, "#6B7280") for region in data["region"]]
            color_title = "Ocean Region"
        else:
            colors = ["#3B82F6"] * len(data)
            color_title = "ARGO Floats"
        
        # Create hover text
        hover_text = []
        for _, row in data.iterrows():
            hover_info = (
                f"<b>{row['float_id']}</b><br>"
                f"Region: {row['region']}<br>"
                f"Status: {row['status']}<br>"
                f"Type: {row['float_type']}<br>"
                f"Cycle: {row['cycle_number']}<br>"
                f"Battery: {row['battery_level']:.1f}%<br>"
                f"Max Depth: {row['max_depth']}m<br>"
                f"Last Profile: {row['last_profile']}"
            )
            hover_text.append(hover_info)
        
        # Create map
        fig = go.Figure()
        
        # Add scatter points
        fig.add_trace(go.Scattermap(
            lat=data["latitude"],
            lon=data["longitude"],
            mode="markers",
            marker=dict(
                size=12,
                color=colors,
                opacity=0.8,
                line=dict(width=1, color="white")
            ),
            hovertext=hover_text,
            hovertemplate="%{hovertext}<extra></extra>",
            name="ARGO Floats"
        ))
        
        # Calculate center and zoom
        center_lat = data["latitude"].mean()
        center_lon = data["longitude"].mean()
        
        # Determine zoom level based on data spread
        lat_range = data["latitude"].max() - data["latitude"].min()
        lon_range = data["longitude"].max() - data["longitude"].min()
        max_range = max(lat_range, lon_range)
        
        if max_range > 100:
            zoom = 1
        elif max_range > 50:
            zoom = 2
        elif max_range > 20:
            zoom = 3
        elif max_range > 10:
            zoom = 4
        else:
            zoom = 5
        
        # Update layout
        fig.update_layout(
            map=dict(
                style="open-street-map",
                center=dict(lat=center_lat, lon=center_lon),
                zoom=zoom
            ),
            margin=dict(l=0, r=0, t=0, b=0),
            height=500,
            showlegend=False,
            title=dict(
                text=f"ARGO Floats Map ({len(data)} floats)",
                x=0.5,
                y=0.95,
                font=dict(size=16)
            )
        )
        
        return fig
    
    def generate_density_map(self, data: pd.DataFrame) -> go.Figure:
        """Generate density heatmap of float locations"""
        if data.empty:
            return self._create_empty_map()
        
        fig = go.Figure()
        
        # Create density map
        fig.add_trace(go.Densitymap(
            lat=data["latitude"],
            lon=data["longitude"],
            radius=20,
            opacity=0.6,
            colorscale="Viridis"
        ))
        
        # Add individual points
        fig.add_trace(go.Scattermap(
            lat=data["latitude"],
            lon=data["longitude"],
            mode="markers",
            marker=dict(size=6, color="white", opacity=0.8),
            name="Float Locations"
        ))
        
        center_lat = data["latitude"].mean()
        center_lon = data["longitude"].mean()
        
        fig.update_layout(
            map=dict(
                style="open-street-map",
                center=dict(lat=center_lat, lon=center_lon),
                zoom=3
            ),
            margin=dict(l=0, r=0, t=0, b=0),
            height=500,
            showlegend=False,
            title=dict(
                text="ARGO Float Density Map",
                x=0.5,
                y=0.95,
                font=dict(size=16)
            )
        )
        
        return fig
    
    def generate_regional_map(self, region: str, data: pd.DataFrame) -> go.Figure:
        """Generate focused map for a specific region"""
        region_bounds = {
            "Arabian Sea": {"lat": [10, 25], "lon": [50, 80], "zoom": 5},
            "Bay of Bengal": {"lat": [5, 22], "lon": [80, 100], "zoom": 5},
            "Indian Ocean": {"lat": [-40, 25], "lon": [20, 120], "zoom": 3},
            "Pacific Ocean": {"lat": [-60, 60], "lon": [120, -60], "zoom": 2},
            "Atlantic Ocean": {"lat": [-60, 70], "lon": [-80, 20], "zoom": 2},
            "Southern Ocean": {"lat": [-70, -40], "lon": [-180, 180], "zoom": 3},
            "Arctic Ocean": {"lat": [66, 90], "lon": [-180, 180], "zoom": 4}
        }
        
        if region not in region_bounds:
            return self.generate_interactive_map(data)
        
        bounds = region_bounds[region]
        
        # Filter data for region if available
        if not data.empty and 'region' in data.columns:
            region_data = data[data['region'] == region]
            if not region_data.empty:
                data = region_data
        
        fig = self.generate_interactive_map(data)
        
        # Update map center and zoom for the specific region
        center_lat = (bounds["lat"][0] + bounds["lat"][1]) / 2
        center_lon = (bounds["lon"][0] + bounds["lon"][1]) / 2
        
        fig.update_layout(
            map=dict(
                center=dict(lat=center_lat, lon=center_lon),
                zoom=bounds["zoom"]
            ),
            title=dict(text=f"ARGO Floats in {region}")
        )
        
        return fig
    
    def _create_empty_map(self) -> go.Figure:
        """Create empty map with message"""
        fig = go.Figure()
        
        fig.add_trace(go.Scattermap(
            lat=[0],
            lon=[0],
            mode="markers",
            marker=dict(size=0),
            showlegend=False
        ))
        
        fig.add_annotation(
            text="No float data available for the current filters",
            x=0.5, y=0.5,
            xref="paper", yref="paper",
            showarrow=False,
            font=dict(size=16, color="gray")
        )
        
        fig.update_layout(
            map=dict(
                style="open-street-map",
                center=dict(lat=0, lon=0),
                zoom=2
            ),
            margin=dict(l=0, r=0, t=0, b=0),
            height=500,
            showlegend=False
        )
        
        return fig
    
    def generate_trajectory_map(self, float_id: str) -> go.Figure:
        """Generate trajectory map for a specific float"""
        # Generate sample trajectory data
        n_points = 20
        
        # Start from random location
        start_lat = np.random.uniform(-60, 60)
        start_lon = np.random.uniform(-180, 180)
        
        # Generate drift trajectory
        lats = [start_lat]
        lons = [start_lon]
        
        for i in range(1, n_points):
            # Small daily drift
            lat_drift = np.random.uniform(-0.1, 0.1)
            lon_drift = np.random.uniform(-0.1, 0.1)
            
            new_lat = lats[-1] + lat_drift
            new_lon = lons[-1] + lon_drift
            
            # Keep within bounds
            new_lat = max(-80, min(80, new_lat))
            if new_lon > 180:
                new_lon -= 360
            elif new_lon < -180:
                new_lon += 360
            
            lats.append(new_lat)
            lons.append(new_lon)
        
        fig = go.Figure()
        
        # Add trajectory line
        fig.add_trace(go.Scattermap(
            lat=lats,
            lon=lons,
            mode="lines+markers",
            line=dict(width=3, color="blue"),
            marker=dict(size=8, color="red"),
            name=f"Float {float_id} Trajectory"
        ))
        
        # Highlight start and end points
        fig.add_trace(go.Scattermap(
            lat=[lats[0]],
            lon=[lons[0]],
            mode="markers",
            marker=dict(size=15, color="green", symbol="diamond"),
            name="Start"
        ))
        
        fig.add_trace(go.Scattermap(
            lat=[lats[-1]],
            lon=[lons[-1]],
            mode="markers",
            marker=dict(size=15, color="red", symbol="star"),
            name="Current"
        ))
        
        fig.update_layout(
            map=dict(
                style="open-street-map",
                center=dict(lat=np.mean(lats), lon=np.mean(lons)),
                zoom=5
            ),
            margin=dict(l=0, r=0, t=0, b=0),
            height=500,
            title=dict(
                text=f"Float {float_id} Trajectory",
                x=0.5,
                y=0.95,
                font=dict(size=16)
            )
        )
        
        return fig