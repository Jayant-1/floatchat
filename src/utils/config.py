"""
Configuration settings for FloatChat Streamlit application
"""

# Page configuration
PAGE_CONFIG = {
    "title": "FloatChat - ARGO Ocean Data AI",
    "icon": "🌊",
    "layout": "wide",
    "sidebar_state": "expanded",
    "menu_items": {
        "Get help": "https://github.com/floatchat/help",
        "Report a bug": "https://github.com/floatchat/issues",
        "About": "FloatChat - Conversational AI for ARGO Ocean Data (SIH 2025)"
    }
}

# Theme configuration
THEME_CONFIG = {
    "primary_color": "#1f77b4",
    "secondary_color": "#0ee7ff", 
    "background_color": "#ffffff",
    "text_color": "#262730",
    "sidebar_color": "#f0f2f6",
    "accent_color": "#00cc96",
    "custom_css": """
        /* Custom CSS for FloatChat - Light Theme */
        .main-header {
            background: linear-gradient(90deg, #1f77b4 0%, #00cc96 100%);
            padding: 1rem;
            border-radius: 10px;
            margin-bottom: 2rem;
            color: white;
        }
        
        .metric-card {
            background: white;
            padding: 1rem;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            border-left: 4px solid #1f77b4;
        }
        
        .chat-message {
            padding: 1rem;
            border-radius: 10px;
            margin: 0.5rem 0;
            max-width: 80%;
        }
        
        .user-message {
            background-color: #e3f2fd;
            color: #000000;
            margin-left: auto;
            text-align: right;
        }
        
        .bot-message {
            background-color: #f5f5f5;
            color: #000000;
            margin-right: auto;
        }
        
        .sidebar-content {
            padding: 1rem 0;
        }
        
        .feature-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1.5rem;
            border-radius: 12px;
            margin: 1rem 0;
            text-align: center;
        }
        
        .stButton > button {
            background: linear-gradient(90deg, #1f77b4 0%, #00cc96 100%);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.5rem 1rem;
            font-weight: 600;
        }
        
        .stSelectbox > div > div {
            border: 2px solid #1f77b4;
            border-radius: 8px;
        }
        
        .map-container {
            border: 2px solid #e0e0e0;
            border-radius: 12px;
            padding: 1rem;
            background: white;
        }
        
        .data-table {
            border-radius: 8px;
            overflow: hidden;
        }
        
        .navigation-button {
            background: linear-gradient(90deg, #1f77b4 0%, #00cc96 100%);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.8rem 1.5rem;
            font-weight: 600;
            margin: 0.5rem;
            transition: transform 0.2s ease;
        }
        
        .navigation-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }
    """
}

# Data configuration
DATA_CONFIG = {
    "float_count": 50,
    "ocean_regions": [
        "Arabian Sea", "Bay of Bengal", "Indian Ocean", "Pacific Ocean",
        "Atlantic Ocean", "Southern Ocean", "Arctic Ocean"
    ],
    "parameters": [
        "Temperature", "Salinity", "Depth", "Location"
    ],
    "depth_ranges": [0, 10, 50, 100, 200, 500, 1000, 2000, 5000],
    "time_range": {
        "start": "2020-01-01",
        "end": "2025-09-11"
    }
}

# Navigation configuration
NAVIGATION = {
    "pages": [
        {"name": "Home", "icon": "🏠", "description": "Project overview and introduction"},
        {"name": "ARGO Floats Map", "icon": "🗺️", "description": "Interactive map of ARGO floats"},
        {"name": "Data Explorer", "icon": "📊", "description": "Query and explore ocean data"},
        {"name": "FloatChat AI", "icon": "🤖", "description": "Conversational AI interface"},
        {"name": "Admin Dashboard", "icon": "⚙️", "description": "Data management and system status"}
    ]
}

# Chatbot configuration
CHATBOT_CONFIG = {
    "welcome_message": "Hello! I'm FloatChat, your AI assistant for ARGO ocean data. I can help you explore temperature, salinity, depth, and location data from our global network of ocean floats. How can I help you explore the oceans today?",
    "sample_queries": [
        "Show me temperature profiles for different depths",
        "What's the average salinity in the Arabian Sea?",
        "Compare temperature and salinity between ocean regions",
        "Show me ARGO float locations and depths",
        "What are the depth vs temperature patterns?"
    ],
    "max_chat_history": 20
}
