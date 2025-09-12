"""
Data generator for simulating ARGO float data
"""

import numpy as np
import pandas as pd
import random
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import json

class DataGenerator:
    """Generate realistic but simulated ARGO float data for demonstration"""
    
    def __init__(self):
        self.ocean_regions = {
            "Arabian Sea": {"lat_range": (10, 25), "lon_range": (50, 80)},
            "Bay of Bengal": {"lat_range": (5, 22), "lon_range": (80, 100)},
            "Indian Ocean": {"lat_range": (-40, 25), "lon_range": (20, 120)},
            "Pacific Ocean": {"lat_range": (-60, 60), "lon_range": (120, -60)},
            "Atlantic Ocean": {"lat_range": (-60, 70), "lon_range": (-80, 20)},
            "Southern Ocean": {"lat_range": (-70, -40), "lon_range": (-180, 180)},
            "Arctic Ocean": {"lat_range": (66, 90), "lon_range": (-180, 180)}
        }
        
        self.float_types = ["APEX", "NOVA", "ARVOR", "PROVOR", "SOLO"]
        self.institutions = ["INCOIS", "NIOT", "CSIR-NIO", "IIT Mumbai", "NPOL"]
    
    def generate_float_locations(self, count: int = 50) -> pd.DataFrame:
        """Generate random but realistic ARGO float locations"""
        floats_data = []
        
        for i in range(count):
            # Randomly select ocean region
            region = random.choice(list(self.ocean_regions.keys()))
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
                "status": random.choice(["Active", "Inactive", "Maintenance"]),
                "max_depth": random.choice([1000, 1500, 2000, 2500]),
                "battery_level": round(random.uniform(20, 100), 1),
                "temperature_range": f"{random.uniform(0, 5):.1f} - {random.uniform(25, 30):.1f}°C",
                "salinity_range": f"{random.uniform(33, 34):.2f} - {random.uniform(35, 37):.2f} PSU"
            }
            floats_data.append(float_data)
        
        return pd.DataFrame(floats_data)
    
    def generate_profile_data(self, float_id: str, max_depth: int = 2000) -> pd.DataFrame:
        """Generate temperature and salinity profile for a specific float"""
        depths = np.arange(0, max_depth + 1, 10)
        
        # Realistic temperature profile (decreases with depth)
        surface_temp = random.uniform(20, 30)
        deep_temp = random.uniform(2, 5)
        temperatures = surface_temp * np.exp(-depths / 1000) + deep_temp
        
        # Add some noise
        temperatures += np.random.normal(0, 0.5, len(depths))
        
        # Realistic salinity profile
        surface_salinity = random.uniform(34, 36)
        salinity = surface_salinity + np.random.normal(0, 0.2, len(depths))
        
        profile_data = pd.DataFrame({
            "depth": depths,
            "temperature": np.round(temperatures, 2),
            "salinity": np.round(salinity, 3),
            "float_id": float_id,
            "profile_date": self._random_date(7)
        })
        
        return profile_data
    
    def generate_trajectory_data(self, float_id: str, days: int = 30) -> pd.DataFrame:
        """Generate trajectory data for a float over specified days"""
        # Start from a random location
        start_lat = random.uniform(-60, 60)
        start_lon = random.uniform(-180, 180)
        
        trajectory_data = []
        current_lat, current_lon = start_lat, start_lon
        
        for day in range(days):
            # Simulate drift (small daily movement)
            daily_drift_lat = random.uniform(-0.1, 0.1)
            daily_drift_lon = random.uniform(-0.1, 0.1)
            
            current_lat += daily_drift_lat
            current_lon += daily_drift_lon
            
            # Keep within reasonable bounds
            current_lat = max(-80, min(80, current_lat))
            if current_lon > 180:
                current_lon -= 360
            elif current_lon < -180:
                current_lon += 360
            
            trajectory_data.append({
                "float_id": float_id,
                "date": datetime.now() - timedelta(days=days-day),
                "latitude": round(current_lat, 4),
                "longitude": round(current_lon, 4),
                "day": day + 1
            })
        
        return pd.DataFrame(trajectory_data)
    
    def generate_regional_summary(self) -> Dict:
        """Generate summary statistics by ocean region"""
        summary = {}
        
        for region, bounds in self.ocean_regions.items():
            # Generate random but realistic statistics
            float_count = random.randint(5, 15)
            avg_temp = random.uniform(15, 28)
            avg_salinity = random.uniform(34, 36)
            
            summary[region] = {
                "active_floats": float_count,
                "avg_surface_temperature": round(avg_temp, 1),
                "avg_surface_salinity": round(avg_salinity, 2),
                "data_coverage": f"{random.randint(70, 95)}%",
                "last_update": self._random_date(3)
            }
        
        return summary
    
    def generate_time_series_data(self, parameter: str, region: str, months: int = 12) -> pd.DataFrame:
        """Generate time series data for a parameter in a region"""
        dates = pd.date_range(
            start=datetime.now() - timedelta(days=months*30),
            periods=months*30,
            freq='D'
        )
        
        # Base values for the 4 supported parameters
        base_values = {
            "Temperature": 25,
            "Salinity": 35,
            "Depth": 500,
            "Location": 0  # For coordinate variations
        }
        
        base_value = base_values.get(parameter, 10)
        
        # Generate realistic time series with seasonal variation
        time_series = []
        for i, date in enumerate(dates):
            # Add seasonal variation
            seasonal_factor = np.sin(2 * np.pi * i / 365)
            daily_value = base_value + seasonal_factor * base_value * 0.1
            
            # Add random noise
            daily_value += random.gauss(0, base_value * 0.05)
            
            time_series.append({
                "date": date,
                "value": round(daily_value, 2),
                "parameter": parameter,
                "region": region
            })
        
        return pd.DataFrame(time_series)
    
    def generate_comparison_data(self, regions: List[str], parameter: str) -> pd.DataFrame:
        """Generate comparison data between regions for a parameter"""
        comparison_data = []
        
        for region in regions:
            # Generate multiple data points for statistical significance
            for _ in range(20):
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
    
    def _random_date(self, days_back: int) -> str:
        """Generate a random date within the last N days"""
        random_days = random.randint(0, days_back)
        date = datetime.now() - timedelta(days=random_days)
        return date.strftime("%Y-%m-%d")
    
    def get_sample_queries_results(self) -> Dict:
        """Get pre-generated results for sample queries"""
        return {
            "temperature_depth": {
                "query": "Show me temperature profiles for different depths",
                "result_summary": "Found 12 ARGO floats with depth-temperature data",
                "avg_surface_temp": "27.3°C",
                "depth_range": "0-2000m",
                "data_points": 156
            },
            "salinity_arabian_sea": {
                "query": "What's the average salinity in the Arabian Sea?",
                "result_summary": "Analyzed 8 active floats in Arabian Sea region",
                "avg_salinity": "36.2 PSU",
                "std_deviation": "±0.4 PSU",
                "sample_size": 89
            },
            "location_comparison": {
                "query": "Compare temperature and salinity between ocean regions",
                "result_summary": "Multi-region location comparison completed",
                "regions_analyzed": 5,
                "highest_temp": "Bay of Bengal (28.1°C)",
                "highest_salinity": "Arabian Sea (36.5 PSU)"
            }
        }
