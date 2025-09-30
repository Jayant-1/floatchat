"""FloatChat prototype: foundational Dash application setup."""

# === Imports ===
from datetime import date, timedelta

# Dash core components and callback utilities for app structure
from dash import Dash, html, dcc, Input, Output, State, ALL, Patch, callback_context, no_update

from typing import Any
# Dash Bootstrap Components for responsive, modern styling
import dash_bootstrap_components as dbc

# Standard library
import time
import copy

# Third-party utilities
import numpy as np
import pandas as pd
import plotly.graph_objs as go

# Enhanced utilities
from utils.enhanced_data_generator import EnhancedDataGenerator
from utils.chat_utils import ChatManager, ChatResponseGenerator
from utils.map_utils import MapGenerator

# === App Initialization ===
# Google Fonts stylesheet for sleek typography and Great Vibes for branding
ROBOTO_FONT = "https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap"
GREAT_VIBES_FONT = "https://fonts.googleapis.com/css2?family=Great+Vibes&display=swap"

# Initialize the Dash app with Lumen light theme and blue accents
app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.LUMEN, ROBOTO_FONT, GREAT_VIBES_FONT],
    suppress_callback_exceptions=True,
    title="FloatChat Prototype",
)
server = app.server  # Expose the underlying Flask server for deployment

# === Prototype Data & Quick Queries ===
# Dictionary of keyword tuples mapped to canned responses for the prototype
DUMMY_RESPONSES: dict[tuple[str, ...], str] = {
    ("salinity", "equator"): "Synthetic salinity profiles near the equator: average 35 PSU at 100m depth, slight freshening toward 400m.",
    ("temperature", "north atlantic"): "Mock North Atlantic temperature slice: surface 18°C, thermocline drop to 6°C by 600m.",
    ("float", "locations"): "Currently tracking 42 placeholder floats clustered around 15°N, 45°W with weekly deployment cadence.",
    ("depth", "profile"): "Deep profile mock-up: synthetic float shows stable gradient from 2°C at 1000m to 1.2°C at 4000m.",
    ("compare", "pacific", "atlantic"): "Comparison placeholder: Pacific mixed layer salinity 34.5 PSU vs Atlantic 35.1 PSU this quarter.",
    ("argo", "summary"): "ARGO program snapshot (simulated): 3,900 floats reporting, 97% telemetry uptime, datasets refreshed daily.",
}

# Quick query bubbles that auto-fill the chat input
QUICK_QUERY_OPTIONS = [
    {
        "key": "temperature_arabian",
        "label": "Temperature in Arabian Sea",
        "query": "Show me temperature profile in the Arabian Sea region.",
    },
    {
        "key": "salinity_bengal",
        "label": "Salinity in Bay of Bengal", 
        "query": "Salinity profile in Bay of Bengal",
    },
    {
        "key": "active_floats",
        "label": "Active Float Locations",
        "query": "Where are the active floats currently reporting?",
    },
    {
        "key": "temp_sal_comparison",
        "label": "Compare Temperature & Salinity",
        "query": "Compare temperature and salinity trends",
    },
    {
        "key": "monthly_trends",
        "label": "Monthly Temperature Trends",
        "query": "Show monthly average temperature trend",
    },
    {
        "key": "depth_profiles",
        "label": "Depth Profile Analysis", 
        "query": "Depth profile of temperature and salinity",
    },
    {
        "key": "regional_comparison",
        "label": "Regional Ocean Comparison",
        "query": "Compare ocean regions temperature data",
    },
    {
        "key": "correlation_analysis",
        "label": "Temperature-Salinity Correlation",
        "query": "Show correlation between temperature and salinity",
    },
]

QUICK_QUERY_LOOKUP = {option["key"]: option["query"] for option in QUICK_QUERY_OPTIONS}

OCEAN_REGION_OPTIONS = [
    {"label": "Arabian Sea", "value": "arabian_sea"},
    {"label": "Bay of Bengal", "value": "bay_of_bengal"},
    {"label": "Atlantic Ocean", "value": "atlantic_basin"},
    {"label": "Pacific Ocean", "value": "pacific_basin"},
    {"label": "Indian Ocean", "value": "indian_ocean"},
    {"label": "Southern Ocean", "value": "southern_ocean"},
    {"label": "Global Network", "value": "global_float_network"},
]

FLOAT_STATUS_OPTIONS = [
    {"label": "Active", "value": "Active"},
    {"label": "Inactive", "value": "Inactive"},
    {"label": "Maintenance", "value": "Maintenance"},
]

FLOAT_TYPE_OPTIONS = [
    {"label": "Core", "value": "Core"},
    {"label": "Bio", "value": "Bio"},
    {"label": "Deep", "value": "Deep"},
]

STATUS_COLOR_MAP = {
    "Active": "#22c55e",
    "Inactive": "#ef4444",
    "Maintenance": "#fbbf24",
    "Deployed": "#3b82f6",
}

PARAMETER_COLUMN_MAP = {
    "Temperature": "temperature",
    "Salinity": "salinity",
    "Depth": "depth",
}

PARAMETER_UNITS = {
    "Temperature": "°C",
    "Salinity": "PSU",
    "Depth": "m",
}

DEFAULT_CHAT_STORE = {
    "conversations": [],
    "active_id": None,
    "conversation_counter": 0,
    "message_counter": 0,
}

DEFAULT_REGION = "indian_ocean"

REGION_CONFIGS = {
    "indian_ocean": {
        "center": {"lat": 0, "lon": 75},
        "zoom": 2.5,
        "lat_range": (-20, 20),
        "lon_range": (50, 100),
        "point_count": 12,
        "title": "Indian Ocean Snapshot",
        "description": "Synthesized float activity across the northern Indian Ocean basin.",
        "dropdown_defaults": {},
    },
    "arabian_sea": {
        "center": {"lat": 18, "lon": 64},
        "zoom": 4.1,
        "lat_range": (12, 22),
        "lon_range": (56, 70),
        "point_count": 8,
        "title": "Arabian Sea Focus",
        "description": "Mock float trajectories concentrated along the Arabian Sea convection zone.",
        "dropdown_defaults": {"salin": "SALIN_2", "location": "LOCATION_3"},
    },
    "bay_of_bengal": {
        "center": {"lat": 15, "lon": 88},
        "zoom": 4.2,
        "lat_range": (5, 22),
        "lon_range": (80, 95),
        "point_count": 10,
        "title": "Bay of Bengal Pulse",
        "description": "Synthetic freshwater plume signatures across the Bay of Bengal.",
        "dropdown_defaults": {},
    },
    "equatorial_band": {
        "center": {"lat": 0, "lon": -20},
        "zoom": 3.2,
        "lat_range": (-5, 5),
        "lon_range": (-40, 10),
        "point_count": 9,
        "title": "Equatorial Salinity Section",
        "description": "Fabricated salinity slice hugging the equatorial corridor.",
        "dropdown_defaults": {"salin": "SALIN_2"},
    },
    "global_float_network": {
        "center": {"lat": 5, "lon": -30},
        "zoom": 1.7,
        "lat_range": (-35, 35),
        "lon_range": (-80, 60),
        "point_count": 18,
        "title": "Global Float Network",
        "description": "Overview of placeholder float deployments across major basins.",
        "dropdown_defaults": {"location": "LOCATION_1"},
    },
    "atlantic_basin": {
        "center": {"lat": 10, "lon": -40},
        "zoom": 2.6,
        "lat_range": (-40, 45),
        "lon_range": (-80, 10),
        "point_count": 20,
        "title": "Atlantic Basin Overview",
        "description": "Imagined float coverage across the wider Atlantic basin.",
        "dropdown_defaults": {},
    },
    "pacific_basin": {
        "center": {"lat": -5, "lon": -150},
        "zoom": 2.3,
        "lat_range": (-45, 35),
        "lon_range": (-180, -100),
        "point_count": 24,
        "title": "Pacific Basin Overview",
        "description": "Placeholder float density spanning the Pacific gyres.",
        "dropdown_defaults": {},
    },
    "southern_ocean": {
        "center": {"lat": -55, "lon": 20},
        "zoom": 2.8,
        "lat_range": (-70, -45),
        "lon_range": (-10, 80),
        "point_count": 16,
        "title": "Southern Ocean Transects",
        "description": "Hypothetical polar float sampling around the Antarctic Circumpolar Current.",
        "dropdown_defaults": {},
    },
    "deep_profile_window": {
        "center": {"lat": -4, "lon": 155},
        "zoom": 3.3,
        "lat_range": (-10, 2),
        "lon_range": (145, 165),
        "point_count": 6,
        "title": "Deep Profile Corridor",
        "description": "Imagined deep profiling mission highlighting abyssal gradients.",
        "dropdown_defaults": {"temp": "TEMP_3", "pressure": "PRESSURE_2"},
    },
}

SIDEBAR_PRESETS = [
    {
        "keywords": ("arabian", "sea"),
        "region": "arabian_sea",
        "dropdowns": {"salin": "SALIN_2", "location": "LOCATION_3"},
    },
    {
        "keywords": ("salinity", "equator"),
        "region": "equatorial_band",
        "dropdowns": {"salin": "SALIN_2"},
    },
    {
        "keywords": ("float", "locations"),
        "region": "global_float_network",
        "dropdowns": {"location": "LOCATION_2"},
    },
    {
        "keywords": ("argo", "summary"),
        "region": "global_float_network",
        "dropdowns": {"location": "LOCATION_1"},
    },
    {
        "keywords": ("map",),
        "region": "global_float_network",
        "dropdowns": {},
    },
    {
        "keywords": ("deep", "profile"),
        "region": "deep_profile_window",
        "dropdowns": {"temp": "TEMP_3", "pressure": "PRESSURE_2"},
    },
]

# === Layout Components ===
# Navbar with brand and About Us link that triggers a modal
navbar = dbc.Navbar(
    dbc.Container(
        [
            # Split FloatChat title: "Float" in blue, "Chat" in dark gray with Great Vibes font
            dbc.NavbarBrand(
                [
                    html.Span("Float", style={
                        "color": "#2859CA", 
                        "fontSize": "2.2rem",
                        "fontFamily": "'Great Vibes', cursive",
                        "fontWeight": "400"
                    }),
                    html.Span("Chat", style={
                        "color": "#495057", 
                        "fontSize": "2.2rem",
                        "fontFamily": "'Great Vibes', cursive",
                        "fontWeight": "400"
                    }),
                ],
                className="great-vibes-regular",
            ),
            dbc.Nav(
                [
                    dbc.Button(
                        "About Us",
                        id="about-nav-button",
                        color="primary",  # Use primary color for light theme
                        size="sm",  # Smaller button size
                        className="fw-semibold",
                        n_clicks=0,
                    ),
                ],
                className="ms-auto",
                navbar=True,
            ),
        ]
    ),
    style={"backgroundColor": "#F1F2F2", "minHeight": "3.5rem"},  # Custom color and smaller height
    dark=False,     # Light mode navbar
    sticky="top",
    class_name="shadow-sm",
)


# Modal placeholder providing About Us content
about_modal = dbc.Modal(
    [
        dbc.ModalHeader(dbc.ModalTitle("About FloatChat")),
        dbc.ModalBody(
            "FloatChat is an AI-assisted workspace for exploring ARGO ocean data. "
            "This placeholder modal will be updated with real content in future sections."
        ),
        dbc.ModalFooter(
            dbc.Button("Close", id="about-modal-close", color="secondary", className="ms-auto", n_clicks=0)
        ),
    ],
    id="about-modal",
    is_open=False,
    centered=True,
    backdrop="static",
)


# === Layout Skeleton ===
# Root container holds the navbar, modal, and an expandable content area
app.layout = html.Div(
    id="app-container",
    children=[
        navbar,
        about_modal,
        dcc.Store(id="chat-store", data=copy.deepcopy(DEFAULT_CHAT_STORE), storage_type="memory"),
        dcc.Store(id="sidebar-context", data=None, storage_type="memory"),
        # Track the latest rendered message ID so the UI can append new bubbles without rebuilding the list.
        dcc.Store(id="chat-render-meta", data={"last_rendered_id": 0, "active_conversation_id": None}, storage_type="memory"),
        html.Main(
            id="main-content",
            children=[
                html.Aside(
                    id="left-sidebar",
                    className="left-sidebar",
                    children=[
                        html.Button(
                            children=[
                                html.Span("＋", className="new-chat-btn-icon"),
                                html.Span("New Chat", className="new-chat-btn-text"),
                            ],
                            id="new-chat-btn",
                            className="new-chat-btn",
                            n_clicks=0,
                        ),
                        html.Div(id="history-list", className="history-list"),
                    ],
                ),
                dbc.Container(
                    [
                        html.Section(
                            [
                                dcc.Loading(
                                    id="chat-loading",
                                    type="default",
                                    parent_className="chat-loading",
                                    children=html.Div(
                                        id="chat-history",
                                        children=[],
                                    ),
                                ),
                                html.Div(
                                    className="suggested-queries-header",
                                    children=[
                                        html.H6("Suggested Queries:", className="suggested-queries-title"),
                                    ]
                                ),
                                html.Div(
                                    className="quick-actions",
                                    children=[
                                        html.Button(
                                            option["label"],
                                            id={"type": "quick-bubble", "index": option["key"]},
                                            className="quick-bubble",
                                            n_clicks=0,
                                        )
                                        for option in QUICK_QUERY_OPTIONS
                                    ],
                                ),
                                html.Div(
                                    className="chat-input-row",
                                    children=[
                                        dcc.Input(
                                            id="chat-input",
                                            type="text",
                                            placeholder="Ask FloatChat about ARGO ocean insights...",
                                            className="chat-input",
                                            debounce=False,
                                            n_submit=0,
                                        ),
                                        html.Button(
                                            id="send-button",
                                            className="send-button",
                                            title="Send message",
                                            n_clicks=0,
                                            children=html.Span("➤", className="send-icon"),
                                        ),
                                    ],
                                ),
                            ],
                            className="chat-wrapper",
                        ),
                        # Sidebar flag button and sidebar
                        html.Div(
                            id="sidebar-flag",
                            className="sidebar-flag",
                            children=[
                                html.Button(
                                    id="open-sidebar-btn",
                                    className="sidebar-flag-btn",
                                    title="Show Data & Map",
                                    children=[
                                        html.Span("🗺", className="sidebar-flag-icon", **{"aria-hidden": "true"}),
                                        html.Span("Map & Data", className="sidebar-flag-label"),
                                    ],
                                    n_clicks=0,
                                ),
                            ],
                        ),
                        html.Div(
                            id="right-sidebar",
                            className="right-sidebar",
                            children=[
                                html.Button(
                                    id="close-sidebar-btn",
                                    className="close-sidebar-btn",
                                    title="Close Sidebar",
                                    children="×",
                                    n_clicks=0,
                                ),
                                html.H4("ARGO Data & Map", className="sidebar-title"),
                                html.Div(
                                    id="chat-analysis-section",
                                    className="analysis-section chat-analysis-section",
                                    children=[
                                        html.H5("Chat-Driven Analysis", className="analysis-section-title"),
                                        html.Div(id="chat-analysis-content", className="analysis-content"),
                                    ],
                                ),
                                html.Div(
                                    id="filter-analysis-section",
                                    className="analysis-section filter-analysis-section",
                                    children=[
                                        html.H5("Filter-Driven Analysis", className="analysis-section-title"),
                                        html.Div(id="filter-analysis-content", className="analysis-content"),
                                        html.Div(
                                            className="sidebar-filters",
                                            children=[
                                                html.Div(
                                                    className="filter-control",
                                                    children=[
                                                        dbc.Label("Ocean Region", html_for="filter-region", className="filter-label"),
                                                        dcc.Dropdown(
                                                            id="filter-region",
                                                            options=OCEAN_REGION_OPTIONS,
                                                            multi=True,
                                                            placeholder="Select regions",
                                                            className="filter-dropdown",
                                                            clearable=True,
                                                        ),
                                                    ],
                                                ),
                                                html.Div(
                                                    className="filter-control",
                                                    children=[
                                                        dbc.Label("Latitude Range", html_for="filter-latitude", className="filter-label"),
                                                        dcc.RangeSlider(
                                                            id="filter-latitude",
                                                            min=-90,
                                                            max=90,
                                                            value=[-20, 20],
                                                            marks={-60: "-60°", 0: "0°", 60: "60°"},
                                                            tooltip={"placement": "bottom", "always_visible": False},
                                                            allowCross=False,
                                                        ),
                                                    ],
                                                ),
                                                html.Div(
                                                    className="filter-control",
                                                    children=[
                                                        dbc.Label("Longitude Range", html_for="filter-longitude", className="filter-label"),
                                                        dcc.RangeSlider(
                                                            id="filter-longitude",
                                                            min=-180,
                                                            max=180,
                                                            value=[-80, 80],
                                                            marks={-120: "-120°", 0: "0°", 120: "120°"},
                                                            tooltip={"placement": "bottom", "always_visible": False},
                                                            allowCross=False,
                                                        ),
                                                    ],
                                                ),
                                                html.Div(
                                                    className="filter-control",
                                                    children=[
                                                        dbc.Label("Float Status", html_for="filter-status", className="filter-label"),
                                                        dcc.Dropdown(
                                                            id="filter-status",
                                                            options=FLOAT_STATUS_OPTIONS,
                                                            multi=True,
                                                            placeholder="Any status",
                                                            className="filter-dropdown",
                                                            clearable=True,
                                                        ),
                                                    ],
                                                ),
                                                html.Div(
                                                    className="filter-control",
                                                    children=[
                                                        dbc.Label("Float Type", html_for="filter-type", className="filter-label"),
                                                        dcc.Dropdown(
                                                            id="filter-type",
                                                            options=FLOAT_TYPE_OPTIONS,
                                                            multi=True,
                                                            placeholder="Any type",
                                                            className="filter-dropdown",
                                                            clearable=True,
                                                        ),
                                                    ],
                                                ),
                                                html.Div(
                                                    className="filter-control",
                                                    children=[
                                                        dbc.Label("Depth Range (m)", html_for="filter-depth", className="filter-label"),
                                                        dcc.RangeSlider(
                                                            id="filter-depth",
                                                            min=0,
                                                            max=6000,
                                                            step=50,
                                                            value=[0, 4000],
                                                            marks={0: "0", 2000: "2k", 4000: "4k", 6000: "6k"},
                                                            tooltip={"placement": "bottom", "always_visible": False},
                                                            allowCross=False,
                                                        ),
                                                    ],
                                                ),
                                            ],
                                        ),
                                    ],
                                ),
                                # Float map moved to bottom
                                html.Div(
                                    [
                                        html.H5("ARGO Float Locations", className="sidebar-details-title"),
                                        dcc.Graph(
                                            id="sidebar-map",
                                            config={"displayModeBar": False},
                                            style={"height": "320px", "maxHeight": "320px"},
                                        ),
                                    ],
                                    className="sidebar-map-wrapper",
                                ),
                                # Float list under the map
                                html.Div(
                                    id="float-list-container",
                                    className="float-list-section",
                                    children=[
                                        html.H6("Active Floats in View", className="sidebar-section-title"),
                                        html.Div(id="float-list"),
                                    ],
                                ),
                                # Filtered table display showing ARGO float samples matching current criteria.
                                html.Div(
                                    id="filtered-table-container",
                                    children=[
                                        html.H5("Filtered Float Samples", className="sidebar-details-title"),
                                        html.Div(id="filtered-table"),
                                    ],
                                ),
                                html.Button(
                                    id="sidebar-export-btn",
                                    className="sidebar-export-btn",
                                    children="Download Filtered Data",
                                    n_clicks=0,
                                ),
                                dcc.Download(id="sidebar-download"),
                            ],
                        ),
                    ],
                    fluid=True,
                    className="chat-container",
                ),
            ],
        ),
    ],
)


# === Dummy Response Logic ===
def generate_dummy_response(message: str) -> str:
    """Return a canned response based on keyword matches or a fallback message."""

    normalized = (message or "").lower()
    for keywords, response in DUMMY_RESPONSES.items():
        if all(keyword in normalized for keyword in keywords):
            return response
    return "Query not recognized yet—try asking about salinity, temperature, or float locations."


# === Enhanced Data Generation Functions ===
# Initialize enhanced utilities for better chat experience

# Global instances of enhanced utilities
enhanced_data_generator = EnhancedDataGenerator()
chat_manager = ChatManager()
chat_response_generator = ChatResponseGenerator(enhanced_data_generator)
map_generator = MapGenerator()


# === Enhanced Plot Generation Functions ===
# Chat-driven plot generation based on user queries

def generate_chat_driven_plots(user_query: str, filtered_data: pd.DataFrame, filters_applied: dict) -> list:
    """Generate plots based on natural language user query"""
    query_lower = user_query.lower()
    plots = []
    
    # Temperature profile plot
    if "temperature" in query_lower and ("profile" in query_lower or "depth" in query_lower):
        plots.append(generate_temperature_profile_plot(filtered_data, filters_applied))
    
    # Salinity profile plot  
    elif "salinity" in query_lower and ("profile" in query_lower or "depth" in query_lower):
        plots.append(generate_salinity_profile_plot(filtered_data, filters_applied))
    
    # Time series trend plot
    elif any(word in query_lower for word in ["trend", "time", "series", "monthly"]):
        parameter = filters_applied.get("parameter_focus", "Temperature")
        plots.append(generate_time_series_plot(parameter, filters_applied))
    
    # Regional comparison
    elif "compare" in query_lower or "comparison" in query_lower:
        plots.append(generate_regional_comparison_plot(filtered_data))
    
    # Correlation analysis
    elif "correlation" in query_lower or "relationship" in query_lower:
        plots.append(generate_correlation_plot(filtered_data))
    
    # Default: show overview plots
    else:
        if not filtered_data.empty:
            plots.append(generate_overview_plot(filtered_data, filters_applied))
    
    return plots

def generate_temperature_profile_plot(data: pd.DataFrame, filters: dict) -> go.Figure:
    """Generate temperature vs depth profile plot"""
    # Use sample float for profile demonstration
    float_id = data['float_id'].iloc[0] if not data.empty else "DEMO-001"
    region_value = filters.get("region", "Indian Ocean")
    if isinstance(region_value, (list, tuple, set)):
        region = ", ".join(str(item) for item in region_value)
    else:
        region = str(region_value)
    
    profile_data = enhanced_data_generator.generate_profile_data(
        float_id, parameter="Temperature"
    )
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=profile_data['temperature'],
        y=-profile_data['depth'],  # Negative for depth below surface
        mode='lines+markers',
        name=f'Temperature Profile - {float_id}',
        line=dict(color='#2859CA', width=3),
        marker=dict(size=6, color='#2859CA')
    ))
    
    fig.update_layout(
        title=f"Temperature Profile in {region}",
        xaxis_title="Temperature (°C)",
        yaxis_title="Depth (m)",
        template="plotly_white",
        height=400,
        showlegend=True
    )
    
    return fig

def generate_salinity_profile_plot(data: pd.DataFrame, filters: dict) -> go.Figure:
    """Generate salinity vs depth profile plot"""
    float_id = data['float_id'].iloc[0] if not data.empty else "DEMO-001"
    region_value = filters.get("region", "Indian Ocean")
    if isinstance(region_value, (list, tuple, set)):
        region = ", ".join(str(item) for item in region_value)
    else:
        region = str(region_value)
    
    profile_data = enhanced_data_generator.generate_profile_data(
        float_id, parameter="Salinity"
    )
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=profile_data['salinity'],
        y=-profile_data['depth'],
        mode='lines+markers',
        name=f'Salinity Profile - {float_id}',
        line=dict(color='#00cc96', width=3),
        marker=dict(size=6, color='#00cc96')
    ))
    
    fig.update_layout(
        title=f"Salinity Profile in {region}",
        xaxis_title="Salinity (PSU)",
        yaxis_title="Depth (m)",
        template="plotly_white",
        height=400,
        showlegend=True
    )
    
    return fig

def generate_time_series_plot(parameter: str, filters: dict) -> go.Figure:
    """Generate time series plot for parameter"""
    region_value = filters.get("region", "indian_ocean")
    if isinstance(region_value, (list, tuple, set)):
        region = str(next(iter(region_value), "indian_ocean"))
    else:
        region = str(region_value)
    
    time_data = enhanced_data_generator.generate_time_series_data(parameter, region)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=time_data['date'],
        y=time_data['value'],
        mode='lines+markers',
        name=f'{parameter} Time Series',
        line=dict(color='#2859CA', width=2),
        marker=dict(size=4)
    ))
    
    fig.update_layout(
        title=f"{parameter} Trend Over Time",
        xaxis_title="Date",
        yaxis_title=f"{parameter} ({time_data['unit'].iloc[0]})",
        template="plotly_white",
        height=400
    )
    
    return fig

def generate_regional_comparison_plot(data: pd.DataFrame) -> go.Figure:
    """Generate regional comparison plot"""
    # Group by region and calculate mean temperature
    if data.empty:
        # Generate sample data for regions
        regions = ["arabian_sea", "bay_of_bengal", "indian_ocean"]
        temp_data = []
        for region in regions:
            region_name = region.replace("_", " ").title()
            temps = np.random.normal(25, 3, 20)
            for temp in temps:
                temp_data.append({"region": region_name, "temperature": temp})
        data = pd.DataFrame(temp_data)
        
    fig = go.Figure()
    
    for region in data['region'].unique():
        region_data = data[data['region'] == region]
        fig.add_trace(go.Box(
            y=region_data['temperature'] if 'temperature' in region_data.columns else region_data['depth'],
            name=region,
            boxpoints='all'
        ))
    
    fig.update_layout(
        title="Regional Parameter Comparison",
        yaxis_title="Temperature (°C)" if 'temperature' in data.columns else "Depth (m)",
        template="plotly_white",
        height=400
    )
    
    return fig

def generate_correlation_plot(data: pd.DataFrame) -> go.Figure:
    """Generate correlation scatter plot"""
    if data.empty or len(data) < 2:
        # Generate sample correlation data
        n_points = 50
        depth = np.random.uniform(0, 2000, n_points)
        temperature = 30 - 0.01 * depth + np.random.normal(0, 2, n_points)
        data = pd.DataFrame({"depth": depth, "temperature": temperature})
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data['depth'] if 'depth' in data.columns else data.iloc[:, 0],
        y=data['temperature'] if 'temperature' in data.columns else data.iloc[:, 1],
        mode='markers',
        name='Data Points',
        marker=dict(color='#2859CA', size=8, opacity=0.7)
    ))
    
    fig.update_layout(
        title="Parameter Correlation Analysis",
        xaxis_title="Depth (m)" if 'depth' in data.columns else "Parameter 1",
        yaxis_title="Temperature (°C)" if 'temperature' in data.columns else "Parameter 2",
        template="plotly_white",
        height=400
    )
    
    return fig

def generate_overview_plot(data: pd.DataFrame, filters: dict) -> go.Figure:
    """Generate overview plot based on available data"""
    if data.empty:
        return generate_temperature_profile_plot(data, filters)
    
    # Create overview based on most relevant parameter
    parameter_focus = filters.get("parameter_focus", "Temperature")
    
    if parameter_focus == "Temperature":
        return generate_temperature_profile_plot(data, filters)
    elif parameter_focus == "Salinity":
        return generate_salinity_profile_plot(data, filters)
    else:
        return generate_regional_comparison_plot(data)


def seeded_rng(label: str) -> np.random.Generator:
    """Return a deterministic random generator for the supplied label."""

    seed = sum(ord(char) for char in label) % (2**32 - 1)
    return np.random.default_rng(seed or 1)


def generate_sidebar_payload(message: str) -> dict | None:
    """Determine sidebar context metadata from the user's message using advanced filtering."""

    if not message:
        return None

    normalized = message.lower()
    
    # First check existing presets for backward compatibility
    for preset in SIDEBAR_PRESETS:
        if all(keyword in normalized for keyword in preset["keywords"]):
            payload = {
                "region": preset["region"],
                "dropdowns": preset.get("dropdowns", {}),
                "source_query": message,
            }
            return payload

    # Generate base dataset for filtering
    base_dataset = build_filtered_dataset(["indian_ocean", "arabian_sea", "bay_of_bengal"], None, None, None, None, None, None)
    
    # Apply chat-driven filters
    filtered_data, filters_applied = enhanced_data_generator.apply_chat_filters(message, base_dataset)
    
    if filters_applied:
        # Generate plots based on the query
        plots = enhanced_data_generator.generate_chat_driven_plots(message, filtered_data)
        
        # Determine primary region for sidebar
        region = "indian_ocean"  # default
        normalized = message.lower().replace(" ", "_")
        for region_name in enhanced_data_generator.ocean_regions.keys():
            if region_name.lower() in normalized:
                region = region_name.lower().replace(" ", "_")
                break
        
        payload = {
            "region": region,
            "dropdowns": {},
            "source_query": message,
            "filters_applied": filters_applied,
            "filtered_data_count": len(filtered_data),
            "enhanced_plots": plots
        }
        
        # Set appropriate dropdowns based on detected parameters
        if filters_applied.get("parameter_focus") == "Temperature":
            payload["dropdowns"]["temp"] = "TEMP_1"
        elif filters_applied.get("parameter_focus") == "Salinity":
            payload["dropdowns"]["salin"] = "SALIN_1"
        elif filters_applied.get("parameter_focus") == "Depth":
            payload["dropdowns"]["location"] = "LOCATION_1"
        
        return payload

    # Fallback to original logic for simple queries
    if "arabian" in normalized:
        return {"region": "arabian_sea", "dropdowns": {"location": "LOCATION_3"}, "source_query": message}
    if "salinity" in normalized:
        return {"region": "equatorial_band", "dropdowns": {"salin": "SALIN_2"}, "source_query": message}
    if "float" in normalized or "map" in normalized:
        return {"region": "global_float_network", "dropdowns": {"location": "LOCATION_1"}, "source_query": message}
    
    return None


def initialize_store(data: dict | None) -> dict:
    """Return a deep-copied chat store with default keys populated."""

    store = copy.deepcopy(DEFAULT_CHAT_STORE)
    if data:
        for key in store:
            if key in data:
                store[key] = copy.deepcopy(data[key])
        if "counter" in data and "conversation_counter" not in data:
            store["conversation_counter"] = data["counter"]
    return store


def ensure_active_conversation(store: dict) -> dict:
    """Ensure there is an active conversation and return it."""

    active_id = store.get("active_id")
    if active_id is not None:
        for conversation in store.get("conversations", []):
            if conversation["id"] == active_id:
                return conversation

    new_id = store["conversation_counter"] + 1
    store["conversation_counter"] = new_id
    new_conversation = {"id": new_id, "title": "New Chat", "messages": []}
    store["conversations"] = [
        new_conversation,
        *[conversation for conversation in store["conversations"] if conversation["id"] != new_id],
    ]
    store["active_id"] = new_id
    return new_conversation


def update_conversation_title(conversation: dict) -> None:
    """Derive a compact title from the first user message."""

    first_user_message = next(
        (message["content"].strip() for message in conversation.get("messages", []) if message["sender"] == "user"),
        "",
    )
    if first_user_message:
        conversation["title"] = first_user_message[:33].strip() + ("…" if len(first_user_message) > 36 else "")
    else:
        conversation["title"] = "New Chat"


def build_chat_message(message: dict) -> html.Div:
    """Construct a single chat bubble with optional sidebar action button."""

    bubble = html.Div(
        message.get("content", ""),
        className="chat-bubble user-bubble" if message.get("sender") == "user" else "chat-bubble bot-bubble",
    )

    container_class = (
        "chat-message chat-message-user" if message.get("sender") == "user" else "chat-message chat-message-bot"
    )
    children = [bubble]

    if message.get("sender") == "bot" and message.get("sidebar_payload"):
        children.append(
            html.Button(
                "View in Map & Data Page",
                id={"type": "sidebar-action", "index": message.get("id")},
                className="sidebar-link-btn",
                n_clicks=0,
            )
        )

    attrs = {"className": container_class}
    message_id = message.get("id")
    if message_id is not None:
        attrs["key"] = f"msg-{message_id}"
        attrs["data-message-id"] = message_id

    return html.Div(children, **attrs)


def render_chat_messages(messages: list[dict]) -> list:
    """Transform stored messages into styled chat entries."""

    if not messages:
        return [
            html.Div(
                "Start a conversation with FloatChat or revisit a previous chat from the left.",
                className="chat-empty-state",
            )
        ]

    return [build_chat_message(message) for message in messages]


def render_history_list(store: dict) -> list:
    """Render the chat history sidebar entries."""

    conversations = store.get("conversations", [])
    active_id = store.get("active_id")
    if not conversations:
        return [html.Div("No saved chats yet.", className="history-empty")]

    entries: list = []
    for conversation in conversations:
        classes = "history-item"
        if conversation["id"] == active_id:
            classes += " active"
        entries.append(
            html.Button(
                conversation.get("title") or f"Chat {conversation['id']}",
                id={"type": "history-entry", "index": conversation["id"]},
                className=classes,
                n_clicks=0,
            )
        )
    return entries


def find_message_payload(store: dict, message_id: int | None) -> dict | None:
    """Locate a sidebar payload for the given message identifier."""

    if message_id is None:
        return None
    for conversation in store.get("conversations", []):
        for message in conversation.get("messages", []):
            if message.get("id") == message_id:
                return copy.deepcopy(message.get("sidebar_payload"))
    return None

# === Sidebar Dummy Data Generation ===
def generate_dummy_map_data(region: str) -> pd.DataFrame:
    """Create a deterministic float catalog for the supplied region.

    The resulting DataFrame carries positional, categorical, and analytic fields so
    downstream filters can trim the data set without regenerating the UI tree.
    """

    config = REGION_CONFIGS.get(region, REGION_CONFIGS[DEFAULT_REGION])
    point_count = max(config.get("point_count", 12) * 10, 200)  # Ensure very dense catalog per region
    lat_range = config.get("lat_range", (-20, 20))
    lon_range = config.get("lon_range", (55, 95))

    rng = seeded_rng(f"{region}-map")
    floats = [f"{region[:2].upper()}-{i + 1:03d}" for i in range(point_count)]
    lats = rng.uniform(lat_range[0], lat_range[1], point_count)
    lons = rng.uniform(lon_range[0], lon_range[1], point_count)
    depths = rng.uniform(0, 4500, point_count)
    statuses = rng.choice([option["value"] for option in FLOAT_STATUS_OPTIONS], size=point_count)
    types = rng.choice([option["value"] for option in FLOAT_TYPE_OPTIONS], size=point_count)
    base_date = date.today() - timedelta(days=30)
    days_offset = rng.integers(0, 30, size=point_count)
    timestamps = [pd.Timestamp(base_date + timedelta(days=int(delta))) for delta in days_offset]
    temperatures = 20 - 0.005 * depths + rng.normal(0, 0.35, point_count)
    salinity = 35 + rng.normal(0, 0.2, point_count)
    cycle_numbers = rng.integers(10, 300, size=point_count)
    battery_levels = rng.uniform(15, 100, size=point_count)
    last_profiles = [
        pd.Timestamp(date.today() - timedelta(days=int(delta))) for delta in rng.integers(0, 15, size=point_count)
    ]

    df = pd.DataFrame(
        {
            "float_id": floats,
            "region": region,
            "latitude": lats,
            "longitude": lons,
            "depth": depths,
            "float_status": statuses,
            "float_type": types,
            "timestamp": timestamps,
            "temperature": temperatures,
            "salinity": salinity,
            "cycle_number": cycle_numbers,
            "battery_level": battery_levels,
            "last_profile": last_profiles,
        }
    )
    def _format_last_profile(value: object) -> str:
        if isinstance(value, pd.Timestamp):
            return value.strftime("%Y-%m-%d")
        if hasattr(value, "strftime"):
            try:
                return value.strftime("%Y-%m-%d")  # type: ignore[call-arg]
            except Exception:
                pass
        if value is None:
            return "N/A"
        return str(value)

    df["hover"] = [
        (
            f"{row.float_id} • {row.float_status} {row.float_type} • Cycle {row.cycle_number}<br>"
            f"Depth: {row.depth:.0f} m | Temp: {row.temperature:.2f} °C | Sal: {row.salinity:.2f} PSU<br>"
            f"Battery: {row.battery_level:.1f}% | Last profile: {_format_last_profile(row.last_profile)}"
        )
        for row in df.itertuples()
    ]
    return df


def build_filtered_dataset(
    regions: list[str] | None,
    lat_range: list[float] | None,
    lon_range: list[float] | None,
    depth_range: list[float] | None,
    date_range: tuple | list | None,
    statuses: list[str] | None,
    float_types: list[str] | None,
) -> pd.DataFrame:
    """Generate a deterministic dataset and apply the sidebar filters in-memory."""

    region_keys = regions or []
    if not region_keys:
        region_keys = [DEFAULT_REGION]

    frames = [generate_dummy_map_data(region_key) for region_key in region_keys]
    dataset = pd.concat(frames, ignore_index=True)

    if lat_range and len(lat_range) == 2:
        lat_min, lat_max = sorted(lat_range)
        dataset = dataset[dataset["latitude"].between(lat_min, lat_max)]

    if lon_range and len(lon_range) == 2:
        lon_min, lon_max = sorted(lon_range)
        dataset = dataset[dataset["longitude"].between(lon_min, lon_max)]

    if depth_range and len(depth_range) == 2:
        depth_min, depth_max = sorted(depth_range)
        dataset = dataset[dataset["depth"].between(depth_min, depth_max)]

    if date_range and all(date_range):
        start_raw, end_raw = date_range
        start_date = pd.to_datetime(start_raw)
        end_date = pd.to_datetime(end_raw)
        dataset = dataset[(dataset["timestamp"] >= start_date) & (dataset["timestamp"] <= end_date)]

    if statuses:
        dataset = dataset[dataset["float_status"].isin(statuses)]

    if float_types:
        dataset = dataset[dataset["float_type"].isin(float_types)]

    return dataset.sort_values("timestamp").reset_index(drop=True)


def compute_parameter_snapshot(
    dataset: pd.DataFrame, parameter: str | None, method: str | None = None
) -> dict | None:
    """Return an aggregated snapshot for the selected parameter and method."""

    if dataset.empty or not parameter:
        return None

    if parameter == "Location":
        unique_floats = dataset["float_id"].nunique()
        return {"label": "Unique Floats", "value": unique_floats, "unit": "count", "method": "Count"}

    column = PARAMETER_COLUMN_MAP.get(parameter)
    if not column or column not in dataset.columns:
        return None

    series = dataset[column].dropna()
    if series.empty:
        return None

    method = method or "Mean"
    if method == "Mean":
        value = float(series.mean())
    elif method == "Median":
        value = float(series.median())
    elif method == "Min":
        value = float(series.min())
    elif method == "Max":
        value = float(series.max())
    else:
        value = float(series.mean())

    unit = PARAMETER_UNITS.get(parameter, "")
    return {"label": parameter, "value": value, "unit": unit, "method": method}


def generate_depth_time_plot(region: str, parameters: list[str] | None) -> go.Scatter:
    """Generate enhanced depth-time profile plot for selected parameters.
    
    Creates synthetic depth profiles based on the region's characteristics and
    selected parameters. Data generation is deterministic for reproducibility.
    """
    
    rng = seeded_rng(f"{region}-depth-time")
    depths = np.linspace(0, 2000, 40)
    
    primary_param = parameters[0] if parameters else "Temperature"
    
    if primary_param == "Temperature":
        base_values = 20 - 0.008 * depths
        anomaly = rng.normal(0, 0.4, depths.shape)
        values = base_values + anomaly
        name = "Temperature (°C)"
        color = "#ef4444"
    elif primary_param == "Salinity":
        base_values = 35 + 0.0001 * depths
        anomaly = rng.normal(0, 0.15, depths.shape)
        values = base_values + anomaly
        name = "Salinity (PSU)"
        color = "#3b82f6"
    else:
        base_values = 20 - 0.008 * depths
        anomaly = rng.normal(0, 0.3, depths.shape)
        values = base_values + anomaly
        name = f"{primary_param} Profile"
        color = "#10b981"
    
    return go.Scatter(
        x=values,
        y=depths,
        mode="markers+lines",
        marker=dict(color=color, size=6),
        line=dict(color=color, width=2),
        name=name,
        yaxis="y",
        showlegend=True,
    )


def generate_hovmoller_plot(region: str, parameters: list[str] | None) -> go.Heatmap:
    """Generate Hovmoller diagram (time vs depth) for oceanographic parameters.
    
    Creates synthetic time-depth heatmap data representing parameter evolution
    over time. The data pattern is seeded by region for consistency.
    """
    
    rng = seeded_rng(f"{region}-hovmoller")
    
    # Time axis (12 months) and depth axis (24 levels)
    months = np.arange(1, 13)
    depths = np.linspace(0, 2000, 24)
    
    primary_param = parameters[0] if parameters else "Temperature"
    
    if primary_param == "Temperature":
        # Temperature decreases with depth, seasonal variation at surface
        baseline = np.linspace(22, 4, len(depths)).reshape(-1, 1)
        seasonal = np.sin(2 * np.pi * (months - 3) / 12) * np.exp(-depths.reshape(-1, 1) / 500)
        perturbation = rng.uniform(-1.2, 1.2, (len(depths), len(months)))
        z_values = baseline + seasonal + perturbation
        colorscale = "RdYlBu_r"
        name = "Temperature"
    elif primary_param == "Salinity":
        # Salinity increases slightly with depth, less seasonal variation
        baseline = np.linspace(34.5, 35.2, len(depths)).reshape(-1, 1)
        seasonal = np.sin(2 * np.pi * (months - 6) / 12) * 0.1 * np.exp(-depths.reshape(-1, 1) / 800)
        perturbation = rng.uniform(-0.3, 0.3, (len(depths), len(months)))
        z_values = baseline + seasonal + perturbation
        colorscale = "Viridis"
        name = "Salinity"
    else:
        # Generic parameter with moderate variation
        baseline = np.linspace(10, 2, len(depths)).reshape(-1, 1)
        seasonal = np.sin(2 * np.pi * (months - 4) / 12) * np.exp(-depths.reshape(-1, 1) / 600)
        perturbation = rng.uniform(-0.8, 0.8, (len(depths), len(months)))
        z_values = baseline + seasonal + perturbation
        colorscale = "Plasma"
        name = primary_param
    
    return go.Heatmap(
        z=z_values,
        x=months,
        y=depths,
        colorscale=colorscale,
        name=f"{name} Hovmoller",
        showscale=True,
        colorbar=dict(
            title=name,
            len=0.7,
        ),
    )


def generate_dummy_export_df(
    regions: list[str] | None,
    lat_range: list[float] | None,
    lon_range: list[float] | None,
    depth_range: list[float] | None,
    date_range: tuple | list | None,
    statuses: list[str] | None,
    float_types: list[str] | None,
    parameters: list[str] | None,
) -> pd.DataFrame:
    """Return a filtered dataset ready for CSV export."""

    dataset = build_filtered_dataset(regions, lat_range, lon_range, depth_range, date_range, statuses, float_types)

    base_columns = [
        "float_id",
        "region",
        "latitude",
        "longitude",
        "timestamp",
        "float_status",
        "float_type",
        "depth",
        "cycle_number",
        "battery_level",
        "last_profile",
    ]

    parameter_columns: list[str] = []
    if parameters:
        for parameter in parameters:
            column = PARAMETER_COLUMN_MAP.get(parameter)
            if column and column not in parameter_columns:
                parameter_columns.append(column)

    # Always include key environmental metrics even when no parameter is selected for clarity.
    if not parameter_columns:
        parameter_columns = list(PARAMETER_COLUMN_MAP.values())

    combined_columns = base_columns + parameter_columns
    export_columns: list[str] = []
    for column in combined_columns:
        if column not in export_columns:
            export_columns.append(column)
    export = dataset[export_columns].copy() if not dataset.empty else pd.DataFrame(columns=export_columns)

    rename_map = {
        "latitude": "Latitude",
        "longitude": "Longitude",
        "timestamp": "Date",
        "depth": "Depth_m",
        "temperature": "Temp_C",
        "salinity": "Salinity_PSU",
    }
    export.rename(columns={k: v for k, v in rename_map.items() if k in export.columns}, inplace=True)

    if "Date" in export.columns:
        export["Date"] = pd.to_datetime(export["Date"], errors="coerce").dt.strftime("%Y-%m-%d")

    return export.reset_index(drop=True)
@app.callback(
    Output("right-sidebar", "className"),
    Input("open-sidebar-btn", "n_clicks"),
    Input("close-sidebar-btn", "n_clicks"),
    Input("sidebar-context", "data"),
    State("right-sidebar", "className"),
)
def toggle_sidebar(open_clicks, close_clicks, context_data, current_class):
    """Manage right sidebar visibility, auto-opening when context updates."""

    ctx = callback_context
    current_class = current_class or "right-sidebar"

    if not ctx.triggered:
        return current_class

    trigger = ctx.triggered_id
    if trigger == "open-sidebar-btn":
        return "right-sidebar open"
    if trigger == "close-sidebar-btn":
        return "right-sidebar"
    if trigger == "sidebar-context" and context_data:
        return "right-sidebar open"
    return current_class


@app.callback(
    Output("sidebar-map", "figure"),
    Output("chat-analysis-content", "children"),
    Output("filter-analysis-content", "children"),
    Output("filtered-table", "children"),
    Output("float-list", "children"),
    Input("right-sidebar", "className"),
    Input("sidebar-context", "data"),
    Input("filter-region", "value"),
    Input("filter-latitude", "value"),
    Input("filter-longitude", "value"),
    Input("filter-status", "value"),
    Input("filter-type", "value"),
    Input("filter-depth", "value"),
)
def update_sidebar_content(
    sidebar_class,
    sidebar_context,
    region_filter,
    lat_range,
    lon_range,
    status_filter,
    type_filter,
    depth_range,
):
    """Refresh sidebar map, plots, analytics, and filtered table based on the advanced filters."""

    context = sidebar_context or {}
    region_from_context = context.get("region", DEFAULT_REGION)
    selected_regions = region_filter if region_filter else [region_from_context]
    readable_regions = ", ".join(region.replace("_", " ").title() for region in selected_regions)

    filters_applied = context.get("filters_applied") or {}
    date_window = None
    if isinstance(filters_applied, dict):
        candidate = filters_applied.get("date_range")
        if candidate and len(candidate) == 2 and all(candidate):
            date_window = candidate

    status_filter = status_filter or []
    type_filter = type_filter or []

    # Build the deterministic float catalog once, then trim it client-side using the active filters.
    dataset = build_filtered_dataset(selected_regions, lat_range, lon_range, depth_range, date_window, status_filter, type_filter)

    primary_region = selected_regions[0]
    region_config = REGION_CONFIGS.get(primary_region, REGION_CONFIGS[DEFAULT_REGION])

    # Map visualization with color-coded markers
    map_trace = go.Scattermap(
        lat=dataset["latitude"] if not dataset.empty else [],
        lon=dataset["longitude"] if not dataset.empty else [],
        mode="markers",
        marker=dict(
            size=11,
            color=[STATUS_COLOR_MAP.get(status, "#60a5fa") for status in dataset["float_status"]]
            if not dataset.empty
            else "#94a3b8",
        ),
        hovertext=dataset["hover"] if not dataset.empty else [],
        name="ARGO Floats",
    )

    map_fig = go.Figure(map_trace)
    if dataset.empty:
        map_center = region_config.get("center", {"lat": 0, "lon": 0})
        zoom_level = region_config.get("zoom", 2.5)
        map_fig.add_annotation(
            text="No floats match the current filters",
            font=dict(color="#94a3b8", size=14),
            showarrow=False,
            x=0.5,
            y=0.5,
            xref="paper",
            yref="paper",
        )
    else:
        map_center = {"lat": float(dataset["latitude"].mean()), "lon": float(dataset["longitude"].mean())}
        zoom_level = region_config.get("zoom", 2.8)

    map_fig.update_layout(
        map=dict(style="open-street-map", center=map_center, zoom=zoom_level),
        margin=dict(l=0, r=0, t=0, b=0),
        height=300,  # Increased height for better visibility
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )

    # Generate chat section content
    chat_children: list[Any] = []
    chat_source = context.get("source_query") if context else None
    chat_summary = context.get("summary") if context else None

    if chat_summary:
        chat_children.append(html.P(chat_summary, className="analysis-summary"))

    chat_plots = context.get("enhanced_plots", []) if context else []
    if chat_plots:
        for plot in chat_plots:
            chat_children.append(dcc.Graph(figure=plot, config={"displayModeBar": False}))
    else:
        chat_children.append(
            html.P(
                "Ask Floatchat about mission trends or float health to see prompt-specific insight here.",
                className="analysis-placeholder",
            )
        )

    if chat_source:
        chat_children.append(
            html.P(
                f"Prompt: \"{chat_source}\"",
                className="analysis-source-label",
            )
        )

    region_label = readable_regions if readable_regions else "the selected regions"
    if dataset.empty:
        filter_analysis_children = [
            html.P(
                "No floats match the current filter criteria. Adjust the controls to view data.",
                className="analysis-placeholder",
            )
        ]
    else:
        filter_analysis_children = [
            html.P(
                f"{len(dataset)} floats match the current filters for {region_label}.",
                className="analysis-summary",
            )
        ]
        if context.get("filters_applied"):
            filter_analysis_children.append(
                html.P(
                    "Filters were derived from your latest chat request.",
                    className="analysis-source-label",
                )
            )

    # Generate filtered table display with extension-ready column selection
    table_data = []
    if not dataset.empty:
        # Limit to first 100 rows for display performance, full dataset available in export
        display_dataset = dataset.head(100)
        for _, row in display_dataset.iterrows():
            table_data.append({
                "Float ID": row["float_id"],
                "Region": row["region"].replace("_", " ").title(),
                "Latitude": f"{row['latitude']:.4f}°",
                "Longitude": f"{row['longitude']:.4f}°",
                "Status": row["float_status"],
                "Type": row["float_type"],
                "Cycle": int(row["cycle_number"]),
                "Battery": f"{row['battery_level']:.1f}%",
                "Last Profile": row["last_profile"].strftime("%Y-%m-%d"),
            })
    
    # Create responsive table with Dash Bootstrap Components for consistent styling
    if table_data:
        table_component = dbc.Table.from_dataframe(  # type: ignore[attr-defined]
            pd.DataFrame(table_data),
            striped=True,
            bordered=True,
            hover=True,
            responsive=True,
            size="sm",
            className="filtered-data-table",
        )
        if len(dataset) > 100:
            table_footer = html.P(
                f"Showing first 100 of {len(dataset)} filtered floats. Download full dataset using the button below.",
                className="table-footer-note",
            )
            table_display = html.Div([table_component, table_footer])
        else:
            table_display = table_component
    else:
        table_display = html.P(
            "No floats match the current filter criteria. Adjust filters to view data.",
            className="table-empty-message",
        )

    # Generate float list for display under the map
    float_list_items = []
    if not dataset.empty:
        # Show first 100 floats for quick reference (scrollable in UI)
        display_floats = dataset.head(100)
        for _, row in display_floats.iterrows():
            status_color = STATUS_COLOR_MAP.get(row["float_status"], "#60a5fa")
            float_item = html.Div([
                html.Span(
                    "●", 
                    style={"color": status_color, "margin-right": "8px", "font-size": "12px"}
                ),
                html.Span(
                    row["float_id"], 
                    style={"font-weight": "bold", "margin-right": "8px"}
                ),
                html.Span(
                    f"({row['latitude']:.2f}°, {row['longitude']:.2f}°)",
                    style={"color": "#94a3b8", "font-size": "12px", "margin-right": "8px"}
                ),
                html.Span(
                    row["float_status"],
                    style={"color": status_color, "font-size": "11px"}
                )
            ], className="float-list-item")
            float_list_items.append(float_item)
        
        if len(dataset) > 100:
            float_list_items.append(
                html.P(
                    f"... and {len(dataset) - 100} more floats",
                    className="float-list-more",
                    style={"color": "#94a3b8", "font-style": "italic", "margin-top": "10px"},
                )
            )
    else:
        float_list_items = [html.P("No floats to display", className="float-list-empty")]

    float_list_display = html.Div(float_list_items, className="float-list-container")

    return map_fig, chat_children, filter_analysis_children, table_display, float_list_display


@app.callback(
    Output("sidebar-download", "data"),
    Input("sidebar-export-btn", "n_clicks"),
    State("sidebar-context", "data"),
    State("filter-region", "value"),
    State("filter-latitude", "value"),
    State("filter-longitude", "value"),
    State("filter-status", "value"),
    State("filter-type", "value"),
    State("filter-depth", "value"),
    prevent_initial_call=True,
)
def export_sidebar_data(
    n_clicks,
    sidebar_context,
    region_filter,
    lat_range,
    lon_range,
    status_filter,
    type_filter,
    depth_range,
):
    if not n_clicks:
        return None

    context = sidebar_context or {}
    region_from_context = context.get("region", DEFAULT_REGION)
    selected_regions = region_filter if region_filter else [region_from_context]

    filters_applied = context.get("filters_applied") or {}
    date_window = None
    if isinstance(filters_applied, dict):
        candidate = filters_applied.get("date_range")
        if candidate and len(candidate) == 2 and all(candidate):
            date_window = candidate

    parameter_selection: list[str] | None = None
    if isinstance(filters_applied, dict):
        selection = filters_applied.get("parameters")
        if isinstance(selection, (list, tuple, set)):
            parameter_selection = [str(item) for item in selection if isinstance(item, str)] or None
        elif isinstance(selection, str):
            parameter_selection = [selection]
        if not parameter_selection:
            focus = filters_applied.get("parameter_focus")
            if isinstance(focus, str):
                parameter_selection = [focus]

    df = generate_dummy_export_df(
        selected_regions,
        lat_range,
        lon_range,
        depth_range,
        date_window,
        status_filter,
        type_filter,
        parameter_selection,
    )

    filename = "floatchat_filtered_export.csv"
    # Persist the filtered slice so analysts can reproduce the exact view outside of the dashboard.
    return dcc.send_data_frame(df.to_csv, filename, index=False)  # type: ignore[attr-defined]


@app.callback(
    Output("sidebar-context", "data"),
    Input({"type": "sidebar-action", "index": ALL}, "n_clicks"),
    State("chat-store", "data"),
    prevent_initial_call=True,
)
def handle_sidebar_action(_action_clicks, store_data):
    """Update sidebar context when a bot suggestion button is clicked."""

    ctx = callback_context
    triggered = ctx.triggered_id if ctx.triggered else None

    if not isinstance(triggered, dict) or triggered.get("type") != "sidebar-action":
        return no_update

    store = initialize_store(store_data)
    payload = find_message_payload(store, triggered.get("index"))
    if not payload:
        return no_update

    payload["timestamp"] = time.time()
    return payload

@app.callback(
    Output("about-modal", "is_open"),
    Input("about-nav-button", "n_clicks"),
    Input("about-modal-close", "n_clicks"),
    State("about-modal", "is_open"),
)
def toggle_about_modal(open_clicks: int | None, close_clicks: int | None, is_open: bool) -> bool:
    """Toggle the About Us modal when the navbar button or close button is clicked."""

    if not (open_clicks or close_clicks):
        # No interaction yet; maintain the current state
        return is_open

    ctx = callback_context
    if not ctx.triggered:  # Safety check: fallback to current state
        return is_open

    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if trigger_id == "about-nav-button":
        return True
    if trigger_id == "about-modal-close":
        return False
    return is_open


@app.callback(
    Output("chat-history", "children"),
    Output("history-list", "children"),
    Output("chat-render-meta", "data"),
    Input("chat-store", "data"),
    State("chat-render-meta", "data"),
)
def render_chat_from_store(store_data: dict | None, render_meta: dict | None):
    """Append new chat bubbles without re-rendering the full conversation list.

    The callback keeps the message transcript responsive by diffing the latest
    conversation against the last rendered message ID stored in-memory. When
    new messages arrive we append them via a Dash ``Patch`` instead of
    rebuilding the entire ``chat-history`` children tree.
    """

    store = initialize_store(store_data)
    history_children = render_history_list(store)

    active_conversation = next(
        (conversation for conversation in store.get("conversations", []) if conversation["id"] == store.get("active_id")),
        None,
    )
    if active_conversation is None and store.get("conversations"):
        active_conversation = store["conversations"][0]

    render_state = render_meta or {"last_rendered_id": 0, "active_conversation_id": None}
    last_rendered_id = int(render_state.get("last_rendered_id", 0) or 0)
    previous_conversation_id = render_state.get("active_conversation_id")

    if not active_conversation:
        # No active conversation yet, return empty state and reset render tracker.
        return (
            render_chat_messages([]),
            history_children,
            {"last_rendered_id": 0, "active_conversation_id": None},
        )

    messages = active_conversation.get("messages", [])
    message_ids = [msg.get("id") for msg in messages if isinstance(msg.get("id"), int)]
    latest_id = max(message_ids, default=0)

    if active_conversation["id"] != previous_conversation_id:
        # Conversation switch: rebuild the full list once for the new context.
        return (
            render_chat_messages(messages),
            history_children,
            {"last_rendered_id": latest_id, "active_conversation_id": active_conversation["id"]},
        )

    new_messages = [
        message
        for message in messages
        if (message.get("id") is None) or (isinstance(message.get("id"), int) and message["id"] > last_rendered_id)
    ]

    if not new_messages:
        # Nothing new to render—preserve the current DOM while keeping counters in sync.
        return (
            no_update,
            history_children,
            {"last_rendered_id": latest_id, "active_conversation_id": active_conversation["id"]},
        )

    patch = Patch()
    for message in new_messages:
        patch.append(build_chat_message(message))

    return (
        patch,
        history_children,
        {"last_rendered_id": latest_id, "active_conversation_id": active_conversation["id"]},
    )


@app.callback(
    Output("chat-store", "data"),
    Output("chat-input", "value"),
    Input("send-button", "n_clicks"),
    Input("chat-input", "n_submit"),
    Input({"type": "quick-bubble", "index": ALL}, "n_clicks"),
    Input("new-chat-btn", "n_clicks"),
    Input({"type": "history-entry", "index": ALL}, "n_clicks"),
    State("chat-input", "value"),
    State("chat-store", "data"),
    prevent_initial_call=True,
)
def process_chat_events(
    _send_clicks: int | None,
    _submit_presses: int | None,
    _quick_clicks: list[int] | None,
    _new_chat_clicks: int | None,
    _history_clicks: list[int] | None,
    current_value: str | None,
    store_data: dict | None,
):
    """Process chat interactions and persist them in the store."""

    store = initialize_store(store_data)
    ctx = callback_context
    triggered_id = ctx.triggered_id if ctx.triggered else None

    # Handle new chat creation
    if triggered_id == "new-chat-btn":
        store["active_id"] = None
        conversation = ensure_active_conversation(store)
        conversation["messages"] = []
        update_conversation_title(conversation)
        store["conversations"] = [
            conversation,
            *[conv for conv in store["conversations"] if conv["id"] != conversation["id"]],
        ]
        return store, ""

    # Handle selecting an existing conversation
    if isinstance(triggered_id, dict) and triggered_id.get("type") == "history-entry":
        selected_id = triggered_id.get("index")
        store["active_id"] = selected_id
        store["conversations"] = [
            *[conv for conv in store["conversations"] if conv["id"] == selected_id],
            *[conv for conv in store["conversations"] if conv["id"] != selected_id],
        ]
        return store, ""

    message_to_send = (current_value or "").strip()

    if isinstance(triggered_id, dict) and triggered_id.get("type") == "quick-bubble":
        raw_key = triggered_id.get("index")
        bubble_key = str(raw_key) if raw_key is not None else ""
        message_to_send = QUICK_QUERY_LOOKUP.get(bubble_key, "").strip()
    elif triggered_id not in {"send-button", "chat-input"}:
        # No relevant trigger for sending a message
        return store, current_value or ""

    if not message_to_send:
        return store, current_value or ""

    conversation = ensure_active_conversation(store)

    conversation.setdefault("messages", [])

    store["message_counter"] += 1
    user_message_id = store["message_counter"]
    conversation["messages"].append({"id": user_message_id, "sender": "user", "content": message_to_send})

    # Enhanced bot response using new chat utilities
    base_data = build_filtered_dataset(["arabian_sea", "bay_of_bengal", "indian_ocean"], None, None, None, None, [], [])
    response_data = chat_response_generator.generate_response(message_to_send, base_data)
    
    bot_reply = response_data["text"]
    sidebar_payload = None
    
    # Generate sidebar payload for map updates
    if response_data["map_needed"] or response_data["figures"]:
        sidebar_payload = {
            "region": "indian_ocean",
            "dropdowns": {},
            "source_query": message_to_send,
            "filters_applied": response_data["filters_applied"],
            "filtered_data_count": len(response_data["filtered_data"]),
            "enhanced_plots": response_data["figures"]
        }

    store["message_counter"] += 1
    bot_message_id = store["message_counter"]
    bot_message = {"id": bot_message_id, "sender": "bot", "content": bot_reply}
    if sidebar_payload:
        bot_message["sidebar_payload"] = sidebar_payload
    conversation["messages"].append(bot_message)

    update_conversation_title(conversation)
    store["conversations"] = [
        conversation,
        *[conv for conv in store["conversations"] if conv["id"] != conversation["id"]],
    ]
    store["active_id"] = conversation["id"]

    return store, ""


# === Auto-scroll and UI Enhancement Callbacks ===

app.clientside_callback(
    """
    function(store_data) {
        // Auto-scroll to bottom of chat when new messages are added
        setTimeout(function() {
            const chatContainer = document.querySelector('#chat-interface .chat-message:last-child');
            if (chatContainer) {
                chatContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            }
        }, 100);
        return window.dash_clientside.no_update;
    }
    """,
    Output("chat-interface", "id"),  # Use a dummy output that doesn't conflict
    Input("chat-store", "data"),
    prevent_initial_call=True
)


if __name__ == "__main__":
    # Run the app in development mode with hot reloading
    app.run(debug=True, port=8053)
