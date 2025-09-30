"""
Enhanced data generator for simulating ARGO float data with chat-driven filtering
Based on the old FloatChat project with improvements for Dash integration
"""

import numpy as np
import pandas as pd
import random
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import re

class EnhancedDataGenerator:
    """Generate realistic but simulated ARGO float data with chat integration"""
    
    def __init__(self):
        self.ocean_regions = {
            "Arabian Sea": {"lat_range": (10, 25), "lon_range": (50, 80), "center": {"lat": 17.5, "lon": 65}},
            "Bay of Bengal": {"lat_range": (5, 22), "lon_range": (80, 100), "center": {"lat": 13.5, "lon": 90}},
            "Indian Ocean": {"lat_range": (-40, 25), "lon_range": (20, 120), "center": {"lat": -7.5, "lon": 70}},
            "Pacific Ocean": {"lat_range": (-60, 60), "lon_range": (120, -60), "center": {"lat": 0, "lon": 180}},
            "Atlantic Ocean": {"lat_range": (-60, 70), "lon_range": (-80, 20), "center": {"lat": 5, "lon": -30}},
            "Southern Ocean": {"lat_range": (-70, -40), "lon_range": (-180, 180), "center": {"lat": -55, "lon": 0}},
            "Arctic Ocean": {"lat_range": (66, 90), "lon_range": (-180, 180), "center": {"lat": 78, "lon": 0}}
        }
        
        self.float_types = ["APEX", "NOVA", "ARVOR", "PROVOR", "SOLO"]
        self.institutions = ["INCOIS", "NIOT", "CSIR-NIO", "IIT Mumbai", "NPOL"]
        self.status_options = ["Active", "Inactive", "Maintenance", "Deployed"]
        
    def generate_float_locations(self, count: int = 100, regions: List[str] = None) -> pd.DataFrame:
        """Generate random but realistic ARGO float locations"""
        if regions is None:
            regions = list(self.ocean_regions.keys())
        
        floats_data = []
        
        for i in range(count):
            # Randomly select ocean region from available regions
            region = random.choice(regions)
            region_bounds = self.ocean_regions[region]
            
            # Generate coordinates within region bounds
            lat = np.random.uniform(
                region_bounds["lat_range"][0], 
                region_bounds["lat_range"][1]
            )
            
            lon_min, lon_max = region_bounds["lon_range"]
            if lon_max < lon_min:  # Handle longitude wraparound
                if random.choice([True, False]):
                    lon = np.random.uniform(lon_min, 180)
                else:
                    lon = np.random.uniform(-180, lon_max)
            else:
                lon = np.random.uniform(lon_min, lon_max)
            
            # Generate float metadata
            float_data = {
                "float_id": f"WMO_{5900000 + i}",
                "latitude": round(lat, 4),
                "longitude": round(lon, 4),
                "region": region,
                "float_type": random.choice(self.float_types),
                "institution": random.choice(self.institutions),
                "deployment_date": self._random_date(365*3),  # Last 3 years
                "last_profile": self._random_date(30),  # Last 30 days
                "cycle_number": random.randint(1, 200),
                "status": random.choice(self.status_options),
                "max_depth": random.choice([1000, 1500, 2000, 2500]),
                "battery_level": round(random.uniform(20, 100), 1),
                "temperature_range": f"{random.uniform(0, 5):.1f} - {random.uniform(25, 30):.1f}°C",
                "salinity_range": f"{random.uniform(33, 34):.2f} - {random.uniform(35, 37):.2f} PSU"
            }
            floats_data.append(float_data)
        
        return pd.DataFrame(floats_data)
    
    def generate_profile_data(self, float_id: str, max_depth: int = 2000, parameter: str = "Temperature") -> pd.DataFrame:
        """Generate temperature and salinity profile for a specific float"""
        depths = np.arange(0, max_depth + 1, 25)
        
        profile_data = {"depth": depths, "float_id": float_id}
        
        if parameter.lower() in ["temperature", "temp"]:
            # Realistic temperature profile (decreases with depth)
            surface_temp = random.uniform(20, 30)
            deep_temp = random.uniform(2, 5)
            temperatures = surface_temp * np.exp(-depths / 1000) + deep_temp
            temperatures += np.random.normal(0, 0.5, len(depths))
            profile_data["temperature"] = np.round(temperatures, 2)
        
        if parameter.lower() in ["salinity", "salt", "psu"]:
            # Realistic salinity profile
            surface_salinity = random.uniform(34, 36)
            salinity = surface_salinity + np.random.normal(0, 0.2, len(depths))
            # Add halocline effect
            halocline_depths = (depths > 100) & (depths < 500)
            salinity[halocline_depths] += random.uniform(-0.5, 0.5)
            profile_data["salinity"] = np.round(salinity, 3)
        
        profile_data["profile_date"] = self._random_date(7)
        
        return pd.DataFrame(profile_data)
    
    def generate_time_series_data(self, parameter: str, region: str, months: int = 12) -> pd.DataFrame:
        """Generate time series data for a parameter in a region"""
        dates = pd.date_range(
            start=datetime.now() - timedelta(days=months*30),
            periods=months,
            freq='ME'
        )
        
        # Base values for different parameters and regions
        base_values = {
            "Temperature": {
                "Arabian Sea": 27, "Bay of Bengal": 28, "Indian Ocean": 24,
                "Pacific Ocean": 22, "Atlantic Ocean": 20, "Southern Ocean": 5
            },
            "Salinity": {
                "Arabian Sea": 36.5, "Bay of Bengal": 34.5, "Indian Ocean": 35.2,
                "Pacific Ocean": 34.8, "Atlantic Ocean": 35.0, "Southern Ocean": 34.2
            }
        }
        
        base_value = base_values.get(parameter, {}).get(region, 20)
        
        # Generate realistic time series with seasonal variation
        time_series = []
        for i, date in enumerate(dates):
            # Add seasonal variation
            seasonal_factor = np.sin(2 * np.pi * i / 12)
            monthly_value = base_value + seasonal_factor * base_value * 0.1
            
            # Add random noise
            monthly_value += random.gauss(0, base_value * 0.05)
            
            time_series.append({
                "date": date,
                "value": round(monthly_value, 2),
                "parameter": parameter,
                "region": region
            })
        
        return pd.DataFrame(time_series)
    
    def generate_comparison_data(self, regions: List[str], parameter: str) -> pd.DataFrame:
        """Generate comparison data between regions for a parameter"""
        comparison_data = []
        
        for region in regions:
            # Generate multiple data points for statistical significance
            for _ in range(30):
                base_values = {
                    "Temperature": {"Arabian Sea": 27, "Bay of Bengal": 28, "Indian Ocean": 24},
                    "Salinity": {"Arabian Sea": 36.5, "Bay of Bengal": 34.5, "Indian Ocean": 35.2}
                }
                
                base_value = base_values.get(parameter, {}).get(region, 20)
                value = base_value + random.gauss(0, base_value * 0.1)
                
                comparison_data.append({
                    "region": region,
                    "parameter": parameter,
                    "value": round(value, 2),
                    "depth": random.choice([0, 50, 100, 200, 500]),
                    "measurement_date": self._random_date(90)
                })
        
        return pd.DataFrame(comparison_data)
    
    def apply_chat_filters(self, query: str, base_data: pd.DataFrame) -> Tuple[pd.DataFrame, Dict]:
        """Apply filters based on natural language chat query"""
        filtered_data = base_data.copy()
        filters_applied = {}
        
        query_lower = query.lower()
        
        # Region filtering
        detected_regions = []
        for region in self.ocean_regions.keys():
            if region.lower() in query_lower:
                detected_regions.append(region)
        
        if detected_regions:
            filtered_data = filtered_data[filtered_data['region'].isin(detected_regions)]
            filters_applied['region'] = detected_regions
        
        # Status filtering
        if any(word in query_lower for word in ['active', 'working', 'operational']):
            if 'float_status' in filtered_data.columns:
                filtered_data = filtered_data[filtered_data['float_status'] == 'Active']
                filters_applied['status'] = 'Active'
        elif any(word in query_lower for word in ['inactive', 'not working', 'dead']):
            if 'float_status' in filtered_data.columns:
                filtered_data = filtered_data[filtered_data['float_status'] == 'Inactive']
                filters_applied['status'] = 'Inactive'
        
        # Depth filtering - check available column names
        depth_col = None
        if 'depth' in filtered_data.columns:
            depth_col = 'depth'
        elif 'max_depth' in filtered_data.columns:
            depth_col = 'max_depth'
            
        if depth_col and any(word in query_lower for word in ['shallow', 'surface', 'top']):
            if depth_col == 'depth':
                filtered_data = filtered_data[filtered_data[depth_col] < 500]
                filters_applied['depth'] = 'Shallow (<500m)'
            else:  # max_depth
                filtered_data = filtered_data[filtered_data[depth_col] < 1000]
                filters_applied['depth'] = 'Shallow (<1000m)'
        elif depth_col and any(word in query_lower for word in ['deep', 'bottom', 'abyssal']):
            if depth_col == 'depth':
                filtered_data = filtered_data[filtered_data[depth_col] > 1000]
                filters_applied['depth'] = 'Deep (>1000m)'
            else:  # max_depth
                filtered_data = filtered_data[filtered_data[depth_col] > 1500]
                filters_applied['depth'] = 'Deep (>1500m)'
        
        # Float type filtering
        for float_type in self.float_types:
            if float_type.lower() in query_lower:
                if 'float_type' in filtered_data.columns:
                    filtered_data = filtered_data[filtered_data['float_type'] == float_type]
                    filters_applied['float_type'] = float_type
                break
        
        # Parameter-based filtering for analysis focus
        if any(word in query_lower for word in ['temperature', 'temp', 'thermal']):
            filters_applied['parameter_focus'] = 'Temperature'
            # Add temperature range filtering if needed
            if 'temperature' in filtered_data.columns:
                # Filter for reasonable temperature ranges
                filtered_data = filtered_data[filtered_data['temperature'].between(-2, 40)]
                
        if any(word in query_lower for word in ['salinity', 'salt', 'psu']):
            filters_applied['parameter_focus'] = 'Salinity' 
            # Add salinity range filtering if needed
            if 'salinity' in filtered_data.columns:
                # Filter for reasonable salinity ranges
                filtered_data = filtered_data[filtered_data['salinity'].between(30, 40)]
        
        # Analysis type detection
        if any(word in query_lower for word in ['profile', 'depth']):
            filters_applied['analysis_type'] = 'Profile Analysis'
        elif any(word in query_lower for word in ['time', 'trend', 'temporal', 'monthly']):
            filters_applied['analysis_type'] = 'Time Series'
        elif any(word in query_lower for word in ['compare', 'comparison', 'versus', 'vs']):
            filters_applied['analysis_type'] = 'Regional Comparison'
        elif any(word in query_lower for word in ['correlation', 'relationship']):
            filters_applied['analysis_type'] = 'Correlation Analysis'
        
        return filtered_data, filters_applied
    
    def generate_chat_driven_plots(self, query: str, data: pd.DataFrame) -> List[go.Figure]:
        """Generate plots based on chat query analysis"""
        plots = []
        query_lower = query.lower()
        
        # Temperature profile plots
        if any(word in query_lower for word in ['temperature', 'temp', 'thermal']):
            plots.append(self._generate_temperature_profile_plot(data))
        
        # Salinity profile plots
        if any(word in query_lower for word in ['salinity', 'salt', 'psu']):
            plots.append(self._generate_salinity_profile_plot(data))
        
        # Time series plots
        if any(word in query_lower for word in ['time', 'trend', 'series', 'temporal', 'monthly']):
            plots.append(self._generate_time_series_plot(data))
        
        # Regional comparison
        if any(word in query_lower for word in ['compare', 'comparison', 'versus', 'vs', 'between']):
            plots.append(self._generate_regional_comparison_plot(data))
        
        # Correlation analysis
        if any(word in query_lower for word in ['correlation', 'relationship', 'vs']):
            plots.append(self._generate_correlation_plot(data))
        
        # Default overview if no specific plot detected
        if not plots:
            plots.append(self._generate_overview_plot(data))
        
        return plots
    
    def _generate_temperature_profile_plot(self, data: pd.DataFrame) -> go.Figure:
        """Generate temperature vs depth profile plot"""
        fig = go.Figure()
        
        # Generate sample profile data
        depths = np.arange(0, 1000, 50)
        surface_temp = 28
        deep_temp = 4
        temperatures = surface_temp * np.exp(-depths / 800) + deep_temp
        temperatures += np.random.normal(0, 0.3, len(depths))
        
        fig.add_trace(go.Scatter(
            x=temperatures,
            y=-depths,
            mode='lines+markers',
            name='Temperature Profile',
            line=dict(color='red', width=3),
            marker=dict(size=6)
        ))
        
        fig.update_layout(
            title="Temperature vs Depth Profile",
            xaxis_title="Temperature (°C)",
            yaxis_title="Depth (m)",
            height=400,
            template="plotly_white"
        )
        
        return fig
    
    def _generate_salinity_profile_plot(self, data: pd.DataFrame) -> go.Figure:
        """Generate salinity vs depth profile plot"""
        fig = go.Figure()
        
        depths = np.arange(0, 1000, 50)
        surface_salinity = 35.5
        salinity = surface_salinity + np.random.normal(0, 0.2, len(depths))
        
        # Add halocline effect
        halocline_mask = (depths > 100) & (depths < 300)
        salinity[halocline_mask] += np.random.uniform(-0.5, -0.2, sum(halocline_mask))
        
        fig.add_trace(go.Scatter(
            x=salinity,
            y=-depths,
            mode='lines+markers',
            name='Salinity Profile',
            line=dict(color='blue', width=3),
            marker=dict(size=6)
        ))
        
        fig.update_layout(
            title="Salinity vs Depth Profile",
            xaxis_title="Salinity (PSU)",
            yaxis_title="Depth (m)",
            height=400,
            template="plotly_white"
        )
        
        return fig
    
    def _generate_time_series_plot(self, data: pd.DataFrame) -> go.Figure:
        """Generate time series plot"""
        # Generate sample time series data
        dates = pd.date_range('2024-01-01', periods=12, freq='ME')
        temperatures = 26 + 2 * np.sin(2 * np.pi * np.arange(12) / 12) + np.random.normal(0, 0.5, 12)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=dates,
            y=temperatures,
            mode='lines+markers',
            name='Monthly Average Temperature',
            line=dict(color='orange', width=3),
            marker=dict(size=8)
        ))
        
        fig.update_layout(
            title="Temperature Time Series",
            xaxis_title="Date",
            yaxis_title="Temperature (°C)",
            height=400,
            template="plotly_white"
        )
        
        return fig
    
    def _generate_regional_comparison_plot(self, data: pd.DataFrame) -> go.Figure:
        """Generate regional comparison box plot"""
        regions = ["Arabian Sea", "Bay of Bengal", "Indian Ocean"]
        comparison_data = []
        
        for region in regions:
            temps = np.random.normal(
                {"Arabian Sea": 27, "Bay of Bengal": 28, "Indian Ocean": 24}[region],
                2, 25
            )
            for temp in temps:
                comparison_data.append({"region": region, "temperature": temp})
        
        df = pd.DataFrame(comparison_data)
        
        fig = px.box(df, x="region", y="temperature", 
                     title="Temperature Distribution by Region",
                     color="region")
        fig.update_layout(height=400, template="plotly_white")
        
        return fig
    
    def _generate_correlation_plot(self, data: pd.DataFrame) -> go.Figure:
        """Generate correlation scatter plot"""
        # Generate sample correlation data
        temperatures = np.random.normal(25, 3, 50)
        salinities = 35 + 0.2 * temperatures + np.random.normal(0, 0.5, 50)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=temperatures,
            y=salinities,
            mode='markers',
            name='T-S Relationship',
            marker=dict(size=10, color='purple', opacity=0.7)
        ))
        
        fig.update_layout(
            title="Temperature vs Salinity Correlation",
            xaxis_title="Temperature (°C)",
            yaxis_title="Salinity (PSU)",
            height=400,
            template="plotly_white"
        )
        
        return fig
    
    def _generate_overview_plot(self, data: pd.DataFrame) -> go.Figure:
        """Generate overview plot when no specific plot is detected"""
        # Create a summary statistics plot
        if not data.empty:
            regions = data['region'].value_counts()
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=regions.index,
                y=regions.values,
                name='Float Count by Region',
                marker=dict(color='lightblue')
            ))
            
            fig.update_layout(
                title="ARGO Floats by Region",
                xaxis_title="Region",
                yaxis_title="Number of Floats",
                height=400,
                template="plotly_white"
            )
        else:
            fig = go.Figure()
            fig.add_annotation(
                text="No data available for visualization",
                x=0.5, y=0.5,
                xref="paper", yref="paper",
                showarrow=False,
                font=dict(size=16)
            )
            fig.update_layout(height=400, template="plotly_white")
        
        return fig
    
    def _random_date(self, days_back: int) -> str:
        """Generate a random date within the last N days"""
        random_days = random.randint(0, days_back)
        date = datetime.now() - timedelta(days=random_days)
        return date.strftime("%Y-%m-%d")
    
    def get_region_info(self, region: str) -> Dict:
        """Get information about a specific region"""
        if region in self.ocean_regions:
            return self.ocean_regions[region]
        return {"lat_range": (0, 0), "lon_range": (0, 0), "center": {"lat": 0, "lon": 0}}