"""
FloatChat Conversational AI Interface
"""

import streamlit as st
import time
import random
from datetime import datetime
from utils.ui_components import render_chat_message, render_info_box
from utils.config import CHATBOT_CONFIG

def should_show_navigation_buttons(response_content):
    """Determine if navigation buttons should be shown based on response content"""
    data_keywords = [
        "temperature", "salinity", "depth", "location", "data", "analysis", "visualization", 
        "profile", "regional", "trends", "patterns", "floats", "arabian sea", 
        "bay of bengal", "indian ocean", "compare", "explore", "show", "map", "latitude", "longitude"
    ]
    content_lower = response_content.lower()
    return any(keyword in content_lower for keyword in data_keywords)

def render_chatbot_page():
    """Render the conversational AI chatbot page"""
    
    st.markdown("## 🤖 FloatChat Conversational AI")
    st.markdown("Interact with our AI assistant to explore ARGO ocean data through natural conversation.")
    
    # Initialize chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = [
            {"role": "assistant", "content": CHATBOT_CONFIG["welcome_message"], "timestamp": datetime.now()}
        ]
    
    # Chat features panel removed per user request – minimal interface only
    show_timestamps = True
    enable_voice = False
    
    # Main chat interface
    # Single-column chat interface
    st.markdown("### 💬 Chat Interface")
    
    # Add custom CSS for blue send button
    st.markdown("""
    <style>
    /* Custom blue styling for send buttons */
    .stForm button[kind="secondaryFormSubmit"] {
        background-color: #1f77b4 !important;
        border-color: #1f77b4 !important;
        color: white !important;
    }
    .stForm button[kind="secondaryFormSubmit"]:hover {
        background-color: #1565c0 !important;
        border-color: #1565c0 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Chat container
    chat_container = st.container()

    # Display chat history
    with chat_container:
        for message in st.session_state.chat_history:
            display_message(message, show_timestamps, enable_voice)


    # Use form to enable Enter key submission and auto-clear
    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_input(
            "Message", 
            placeholder="Ask me anything about ARGO ocean data...",
            key="user_input_form",
            label_visibility="collapsed"
        )
        
        # Send button with blue styling
        submitted = st.form_submit_button("➤ Send Message", type="secondary")
        
        if submitted and user_input:
            process_user_message(user_input)
            st.rerun()

def display_message(message, show_timestamps, enable_voice):
    """Display a chat message with styling"""
    
    is_user = message["role"] == "user"
    content = message["content"]
    timestamp = message["timestamp"]
    
    # Create message container
    if is_user:
        st.markdown(f"""
        <div style="
            background-color: #e3f2fd;
            color: #000000;
            padding: 1rem;
            border-radius: 15px 15px 5px 15px;
            margin: 0.5rem 0 0.5rem 20%;
            border-left: 4px solid #1976d2;
        ">
            <strong>You:</strong> {content}
            {f'<br><small style="color: #666;">{timestamp.strftime("%H:%M")}</small>' if show_timestamps else ''}
        </div>
        """, unsafe_allow_html=True)
    else:
        # Bot message with more features
        st.markdown(f"""
        <div style="
            background-color: #f5f5f5;
            color: #000000;
            padding: 1rem;
            border-radius: 15px 15px 15px 5px;
            margin: 0.5rem 20% 0.5rem 0;
            border-left: 4px solid #4caf50;
        ">
            <strong>🤖 FloatChat:</strong> {content}
            {f'<br><small style="color: #666;">{timestamp.strftime("%H:%M")}</small>' if show_timestamps else ''}
        </div>
        """, unsafe_allow_html=True)
        
        # Add navigation buttons for data-related responses
        if should_show_navigation_buttons(content):
            # Add CSS to make buttons shorter and stick together on left
            st.markdown("""
            <style>
            .nav-buttons-container {
                display: flex !important;
                gap: 0px !important;
                justify-content: flex-start !important;
                margin: 0rem 0 !important;
            }
            .nav-buttons-container .stButton > button {
                height: 2rem !important;
                padding: 0.25rem 0.75rem !important;
                font-size: 0.85rem !important;
                margin: 0 !important;
                width: auto !important;
                min-width: auto !important;
                margin-right: 1px !important;
            }
            .nav-buttons-container .stButton {
                margin-right: 0 !important;
                margin-left: 0 !important;
            }
            </style>
            """, unsafe_allow_html=True)
            
            # Create container div and use very tight columns
            st.markdown('<div class="nav-buttons-container">', unsafe_allow_html=True)
            col1, col2, col3 = st.columns([0.6, 0.6, 3], gap="small")
            
            with col1:
                if st.button("🗺️ View on Map", key=f"map_{timestamp}", type="secondary"):
                    st.session_state.current_page = "ARGO Floats Map"
                    st.rerun()
            with col2:
                if st.button("📊 Explore Data", key=f"data_{timestamp}", type="secondary"):
                    st.session_state.current_page = "Data Explorer"
                    st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Add voice button if enabled
        if enable_voice:
            if st.button(f"🔊 Read Aloud", key=f"voice_{timestamp}"):
                st.info("Text-to-speech feature coming soon!")

def process_user_message(user_input):
    """Process user message and generate bot response"""
    
    # Add user message to history
    st.session_state.chat_history.append({
        "role": "user",
        "content": user_input,
        "timestamp": datetime.now()
    })
    
    # Generate bot response
    bot_response = generate_bot_response(user_input)
    
    # Add bot response to history
    st.session_state.chat_history.append({
        "role": "assistant", 
        "content": bot_response,
        "timestamp": datetime.now()
    })
    
    # Limit chat history size
    if len(st.session_state.chat_history) > CHATBOT_CONFIG["max_chat_history"]:
        st.session_state.chat_history = st.session_state.chat_history[-CHATBOT_CONFIG["max_chat_history"]:]

def generate_bot_response(user_input):
    """Generate contextual bot response based on user input"""
    
    user_input_lower = user_input.lower()
    
    # Temperature-related queries
    if any(word in user_input_lower for word in ["temperature", "temp", "warm", "cold", "heat"]):
        responses = [
            "Based on recent ARGO data, I can see interesting temperature patterns! The Arabian Sea shows an average surface temperature of 27.3°C, while deeper waters (500m+) maintain around 12-15°C. Would you like me to show you a specific depth profile or regional comparison?",
            "Temperature analysis shows fascinating seasonal variations! In the Indian Ocean, we see surface temperatures ranging from 24-30°C depending on the season and location. The thermal stratification is particularly strong during monsoon seasons. What specific temperature aspect interests you most?",
            "Great question about temperature! Our ARGO floats reveal that equatorial regions maintain consistently higher surface temperatures (26-29°C) compared to polar regions. The temperature gradient with depth is quite dramatic - dropping to 2-4°C at 2000m depth. Would you like to explore temperature trends in a specific region?"
        ]
        
    # Salinity-related queries
    elif any(word in user_input_lower for word in ["salinity", "salt", "psu"]):
        responses = [
            "Salinity patterns are fascinating! The Arabian Sea shows higher salinity levels (36.2 PSU average) due to high evaporation rates, while the Bay of Bengal has lower salinity (34.5 PSU) influenced by freshwater from major rivers. The vertical salinity profile typically shows a halocline between 50-200m depth.",
            "Excellent salinity question! ARGO data reveals that surface salinity varies significantly across regions. Monsoon patterns also create seasonal salinity variations of ±0.5 PSU. Which region's salinity patterns interest you?",
            "Salinity analysis from our floats shows intriguing patterns! Generally, salinity increases with depth in most ocean regions, but there are fascinating exceptions like in polar regions where cold, fresh water can create inverse profiles. The global average is around 35 PSU, but regional variations tell amazing stories about ocean circulation."
        ]
    
    # Depth-related queries  
    elif any(word in user_input_lower for word in ["depth", "deep", "profile", "vertical"]):
        responses = [
            "Depth profiles reveal incredible ocean structure! Our ARGO floats dive to depths of 2000m, measuring temperature and salinity changes throughout the water column. Surface waters show the most variability, while deep waters (>1000m) are more stable. Would you like to see a specific depth profile?",
            "Great depth question! Temperature typically decreases from 25-30°C at the surface to 2-4°C at 2000m depth. Salinity patterns are more complex, often showing a halocline (rapid salinity change) between 50-200m. The depth profiles tell us about water mass origins and mixing processes.",
            "Depth analysis shows fascinating vertical structure! Each ocean region has unique depth characteristics - the Arabian Sea has distinct layering due to high surface evaporation, while the Bay of Bengal shows strong stratification from river inputs. Which depth range interests you most?"
        ]
    
    # Location/region queries
    elif any(word in user_input_lower for word in ["location", "latitude", "longitude", "position", "coordinate"]):
        responses = [
            "Location data is fundamental to our analysis! Our ARGO floats provide precise latitude/longitude coordinates, allowing us to track ocean conditions across different regions. Each location tells a unique story about local oceanography. Which coordinates or region would you like to explore?",
            "Excellent location question! We track float positions from the Arabian Sea (10-25°N, 50-80°E) to the Bay of Bengal (5-22°N, 80-100°E) and broader Indian Ocean. Each coordinate pair represents valuable oceanographic data. What specific location interests you?",
            "Location analysis reveals regional patterns! Different latitude/longitude combinations show unique temperature and salinity characteristics. Equatorial regions tend to be warmer, while higher latitudes show more seasonal variation. Would you like to explore data from specific coordinates?"
        ]
    
    # Location/region queries
    elif any(word in user_input_lower for word in ["arabian sea", "bay of bengal", "indian ocean", "location", "region", "where"]):
        responses = [
            "Our ARGO network provides excellent coverage across these regions! The Arabian Sea has 15 active floats, Bay of Bengal has 12, and the broader Indian Ocean has 23. Each region shows unique characteristics - the Arabian Sea is more saline and warmer, while the Bay of Bengal shows strong seasonal variations due to monsoons.",
            "Regional analysis is one of our strengths! The Indian Ocean basin shows fascinating diversity - from the warm, salty Arabian Sea to the fresher Bay of Bengal influenced by river discharge. Our floats track these regional differences in real-time. Which specific regional comparison would you like to explore?",
            "Great regional question! Our ARGO network reveals that each ocean region has its unique 'fingerprint' in terms of temperature, salinity, and depth characteristics. The Arabian Sea is known for its high salinity, while the Bay of Bengal shows dramatic seasonal changes. Current data shows interesting patterns right now!"
        ]
    
    # Data/analysis queries
    elif any(word in user_input_lower for word in ["data", "analysis", "show", "compare", "trend"]):
        responses = [
            "I can help you analyze the data in several ways! We have real-time data from 3,847 active floats with over 2.1 million data points covering temperature, salinity, depth, and location. Would you like me to generate a specific visualization, run a statistical comparison, or show you recent trends? I can create depth profiles, time series, or regional comparisons.",
            "Excellent! Our analysis capabilities include trend detection, anomaly identification, and multi-parameter correlations. Recent analysis shows interesting patterns - for example, a 0.2°C warming trend in surface waters over the past 5 years, and salinity changes in key regions. What type of analysis would be most helpful for your research?",
            "Data analysis is my specialty! I can provide statistical summaries, create visualizations, or run comparative studies across different regions and time periods. Our machine learning models have identified several interesting temperature and salinity patterns in recent months. What specific analysis or comparison would you like me to perform?"
        ]
    
    # Research/scientific queries
    elif any(word in user_input_lower for word in ["research", "study", "climate", "pattern", "trend", "science"]):
        responses = [
            "From a research perspective, our ARGO data is revealing crucial insights into climate change impacts! We're seeing clear warming trends in the upper 2000m of the ocean, changes in salinity patterns due to altered precipitation/evaporation cycles, and variations in temperature-depth relationships. What aspect of climate research interests you most?",
            "Scientific applications of our data are vast! Researchers are using ARGO data for climate model validation, studying ocean heat content changes, tracking marine heatwaves, and understanding temperature-salinity relationships at various depths. Recent studies have shown significant findings in regional patterns. How can I help with your research needs?",
            "The research implications are fascinating! Our data contributes to understanding ocean's role in climate regulation, tracking changes in water mass properties, and predicting future ocean conditions. Recent patterns suggest interesting temperature and salinity correlations with depth. What research question can I help you explore?"
        ]
    
    # Help/general queries
    elif any(word in user_input_lower for word in ["help", "how", "what", "explain", "guide"]):
        responses = [
            "I'm here to help you explore ocean data! You can ask me about temperature and salinity patterns, depth profiles, location-based comparisons, or request data visualizations. Try asking something like 'Show me temperature trends with depth in the Arabian Sea' or 'Compare salinity between different locations'.",
            "I can assist with various ocean data questions! My capabilities include analyzing ARGO float data for temperature, salinity, depth, and location parameters, creating visualizations, and providing research insights. You can ask about specific parameters, regions, depth ranges, or coordinate-based comparisons. What would you like to explore?",
            "Welcome! I can help you understand ocean data through natural conversation. You can ask about current conditions, depth patterns, regional differences, or specific phenomena related to temperature, salinity, depth, and location data. I can also generate charts, provide statistical analysis, and explain complex oceanographic processes. What interests you most about the ocean?"
        ]
    
    # Greeting
    elif any(word in user_input_lower for word in ["hello", "hi", "hey", "good morning", "good afternoon"]):
        responses = [
            "Hello! I'm excited to help you explore the fascinating world of ocean data. Our ARGO floats are continuously measuring temperature, salinity, and other parameters across the global oceans. What would you like to discover today?",
            "Hi there! Welcome to FloatChat. I have access to real-time data from thousands of ARGO floats around the world. Whether you're interested in temperature trends, salinity patterns, or regional comparisons, I'm here to help. What ocean mysteries shall we explore together?",
            "Greetings! I'm your AI ocean data assistant. Our ARGO network provides incredible insights into ocean conditions worldwide. From climate research to marine ecosystem studies, there's so much to discover. What aspect of ocean science interests you most?"
        ]
    
    # Default response
    else:
        responses = [
            "That's an interesting question! While I don't have a specific answer for that, I can help you explore ARGO ocean data in many ways. Try asking about temperature patterns, salinity trends, regional comparisons, or specific float locations. What ocean data would you like to investigate?",
            "I'd love to help you with that! My expertise is in ARGO ocean data analysis. I can provide information about temperature and salinity profiles, compare different ocean regions, show recent trends, or explain oceanographic phenomena. How can I redirect this to help you explore ocean data?",
            "Great question! Let me help you explore our extensive ARGO dataset instead. We have fascinating information about ocean temperature, salinity, oxygen levels, and much more across different regions and depths. What specific ocean data topic interests you most?",
            "I appreciate your question! As an ocean data specialist, I'm best equipped to help with ARGO float data analysis, oceanographic trends, and marine research insights. Our database contains millions of measurements from around the globe. What ocean-related question can I answer for you?"
        ]
    
    # Select random response and add personal touch
    base_response = random.choice(responses)
    
    # Add current data context occasionally
    if random.random() < 0.3:
        data_additions = [
            "\n\n📊 Current status: 3,847 active floats reporting data.",
            "\n\n🌊 Latest update: New data from 156 floats in the last 24 hours.",
            "\n\n📈 Trending: Recent temperature anomalies detected in the Pacific region.",
            "\n\n🔍 Tip: Try asking for a specific visualization or regional comparison!"
        ]
        base_response += random.choice(data_additions)
    
    return base_response

def generate_topic_message(topic):
    """Generate a user message based on selected topic"""
    topic_messages = {
        "🌡️ Temperature Analysis": "Show me temperature analysis for different ocean regions",
        "🧂 Salinity Patterns": "What are the current salinity patterns across the oceans?",
        "🌊 Ocean Currents": "How do ocean currents affect temperature and salinity?",
        "📍 Float Locations": "Where are the ARGO floats currently located?",
        "📈 Trends & Predictions": "What trends do you see in recent ocean data?",
        "🔬 Research Applications": "How is ARGO data used in climate research?"
    }
    return topic_messages.get(topic, "Tell me more about ocean data")

def export_chat_history():
    """Export chat history to downloadable format"""
    
    # Create export data
    export_data = []
    for message in st.session_state.chat_history:
        export_data.append({
            "timestamp": message["timestamp"].strftime("%Y-%m-%d %H:%M:%S"),
            "role": message["role"],
            "content": message["content"]
        })
    
    # Convert to string format
    export_text = "FloatChat Conversation Export\n"
    export_text += "=" * 50 + "\n\n"
    
    for message in export_data:
        role_name = "You" if message["role"] == "user" else "FloatChat"
        export_text += f"[{message['timestamp']}] {role_name}: {message['content']}\n\n"
    
    # Provide download
    st.sidebar.download_button(
        label="📄 Download Chat",
        data=export_text,
        file_name=f"floatchat_conversation_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
        mime="text/plain"
    )
    
    st.sidebar.success("Chat exported successfully!")
