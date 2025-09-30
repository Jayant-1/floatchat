"""
Chat utilities for enhanced chat experience with better performance
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Any
import plotly.graph_objects as go

class ChatManager:
    """Manage chat messages and state efficiently"""
    
    def __init__(self, chat_file: str = "chat_history.json"):
        self.chat_file = chat_file
        self.messages = self.load_chat_history()
    
    def load_chat_history(self) -> List[Dict]:
        """Load chat history from file"""
        try:
            if os.path.exists(self.chat_file):
                with open(self.chat_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception:
            pass
        return self._get_welcome_message()
    
    def save_chat_history(self):
        """Save chat history to file"""
        try:
            with open(self.chat_file, 'w', encoding='utf-8') as f:
                json.dump(self.messages, f, ensure_ascii=False, indent=2, default=str)
        except Exception:
            pass
    
    def add_message(self, role: str, content: str, **kwargs) -> Dict:
        """Add a new message to chat history"""
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            **kwargs
        }
        self.messages.append(message)
        self.save_chat_history()
        return message
    
    def add_user_message(self, content: str) -> Dict:
        """Add user message"""
        return self.add_message("user", content)
    
    def add_bot_message(self, content: str, figures: List = None, map_data: Dict = None) -> Dict:
        """Add bot message with optional figures and map data"""
        kwargs = {}
        if figures:
            kwargs["figures"] = figures
        if map_data:
            kwargs["map_data"] = map_data
        return self.add_message("assistant", content, **kwargs)
    
    def clear_history(self):
        """Clear chat history"""
        self.messages = self._get_welcome_message()
        self.save_chat_history()
    
    def get_messages(self) -> List[Dict]:
        """Get all messages"""
        return self.messages
    
    def _get_welcome_message(self) -> List[Dict]:
        """Get welcome message"""
        return [{
            "role": "assistant",
            "content": "🌊 Welcome to FloatChat! I can help you explore ARGO ocean data. Ask me about temperature profiles, salinity data, float locations, or regional comparisons. Try queries like:\n\n• \"Show temperature profile in Arabian Sea\"\n• \"Compare salinity between regions\"\n• \"Where are active floats located?\"",
            "timestamp": datetime.now().isoformat()
        }]

class ChatResponseGenerator:
    """Generate intelligent responses to user queries"""
    
    def __init__(self, data_generator):
        self.data_generator = data_generator
        
    def generate_response(self, user_input: str, base_data) -> Dict:
        """Generate response with plots and data based on user input"""
        query_lower = user_input.lower()
        
        # Apply filters based on query
        filtered_data, filters_applied = self.data_generator.apply_chat_filters(user_input, base_data)
        
        # Generate plots based on query
        figures = self.data_generator.generate_chat_driven_plots(user_input, filtered_data)
        
        # Generate text response
        response_text = self._generate_text_response(user_input, filtered_data, filters_applied)
        
        # Determine if map update is needed
        map_needed = any(word in query_lower for word in [
            'map', 'location', 'where', 'floats', 'region', 'arabian sea', 
            'bay of bengal', 'indian ocean', 'pacific', 'atlantic'
        ])
        
        return {
            "text": response_text,
            "figures": figures,
            "filtered_data": filtered_data,
            "filters_applied": filters_applied,
            "map_needed": map_needed
        }
    
    def _generate_text_response(self, query: str, data, filters) -> str:
        """Generate intelligent text response"""
        query_lower = query.lower()
        
        responses = []
        
        # Data summary with context
        if not data.empty:
            responses.append(f"Found {len(data)} ARGO floats matching your query.")
            
            # Add parameter-specific context
            if 'parameter_focus' in filters:
                param = filters['parameter_focus']
                if param == 'Temperature':
                    if 'temperature' in data.columns:
                        avg_temp = data['temperature'].mean()
                        responses.append(f"Average temperature: {avg_temp:.1f}°C across selected floats.")
                elif param == 'Salinity':
                    if 'salinity' in data.columns:
                        avg_sal = data['salinity'].mean()
                        responses.append(f"Average salinity: {avg_sal:.2f} PSU across selected floats.")
            
            # Add region-specific context
            if 'region' in filters:
                region_list = filters['region']
                if isinstance(region_list, list):
                    region_names = ', '.join([r.replace('_', ' ').title() for r in region_list])
                    responses.append(f"Focus region(s): {region_names}")
        else:
            responses.append("No floats match your current query. Try adjusting your criteria.")
        
        # Filter acknowledgment with more detail
        if filters:
            filter_texts = []
            for key, value in filters.items():
                if key == 'parameter_focus':
                    filter_texts.append(f"Parameter focus: {value}")
                elif key == 'analysis_type':
                    filter_texts.append(f"Analysis type: {value}")
                elif key == 'status':
                    filter_texts.append(f"Float status: {value}")
                elif key == 'depth':
                    filter_texts.append(f"Depth range: {value}")
                elif isinstance(value, list):
                    filter_texts.append(f"{key.replace('_', ' ').title()}: {', '.join(value)}")
                else:
                    filter_texts.append(f"{key.replace('_', ' ').title()}: {value}")
            if filter_texts:
                responses.append(f"Applied filters: {'; '.join(filter_texts)}")
        
        # Analysis type acknowledgment with specific context
        if any(word in query_lower for word in ['temperature', 'temp']):
            responses.append("🌡️ Temperature profile analysis generated.")
        
        if any(word in query_lower for word in ['salinity', 'salt', 'psu']):
            responses.append("🧂 Salinity profile analysis included.")
        
        if any(word in query_lower for word in ['time', 'trend', 'temporal', 'monthly']):
            responses.append("📈 Time series analysis prepared.")
        
        if any(word in query_lower for word in ['compare', 'comparison', 'versus', 'vs']):
            responses.append("📊 Regional comparison analysis completed.")
        
        if any(word in query_lower for word in ['correlation', 'relationship']):
            responses.append("🔗 Correlation analysis generated.")
        
        if any(word in query_lower for word in ['map', 'location', 'where', 'floats']):
            responses.append("🗺️ Map view updated with filtered float locations.")
        
        if any(word in query_lower for word in ['profile', 'depth']):
            responses.append("📊 Depth profile visualization created.")
        
        # Add helpful context based on the analysis
        if 'arabian sea' in query_lower:
            responses.append("Arabian Sea region selected - known for high salinity waters.")
        elif 'bay of bengal' in query_lower:
            responses.append("Bay of Bengal region selected - characterized by lower salinity due to river discharge.")
        elif 'indian ocean' in query_lower:
            responses.append("Indian Ocean region selected - diverse thermal and salinity characteristics.")
        
        # Default response if nothing specific detected but filters applied
        if len(responses) == 1 and filters:  # Only the data summary
            responses.append("Analysis complete. Use the sidebar to explore the filtered data and visualizations.")
        elif len(responses) == 1:  # Only the data summary and no filters
            responses.append("Try asking about temperature profiles, salinity data, float locations, or regional comparisons.")
        
        return " ".join(responses)

def serialize_figures_for_storage(figures: List[go.Figure]) -> List[Dict]:
    """Convert plotly figures to JSON-serializable format for storage"""
    serialized = []
    for fig in figures:
        try:
            serialized.append(fig.to_dict())
        except Exception:
            # If serialization fails, skip the figure
            continue
    return serialized

def deserialize_figures_from_storage(serialized_figures: List[Dict]) -> List[go.Figure]:
    """Convert stored JSON data back to plotly figures"""
    figures = []
    for fig_dict in serialized_figures:
        try:
            fig = go.Figure(fig_dict)
            figures.append(fig)
        except Exception:
            # If deserialization fails, skip the figure
            continue
    return figures