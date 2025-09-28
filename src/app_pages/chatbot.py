import streamlit as st
import random
from datetime import datetime
import shelve
import os
import json
import tempfile
import traceback
import plotly.express as px
import pandas as pd
import folium
from streamlit_folium import st_folium
from utils.config import CHATBOT_CONFIG

USER_AVATAR = "👤"
BOT_AVATAR = "🤖"
LOCK_PATH = "floatchat_history.lock"
SHELVE_FILENAME = "floatchat_history"
JSON_FALLBACK = "floatchat_history.json"

# Note: st.set_page_config() is handled by main.py, not individual pages

# --- Persistence helpers ---
def _acquire_lock(lock_path):
    try:
        import fcntl
    except:
        return None
    f = open(lock_path, "w")
    try:
        fcntl.flock(f, fcntl.LOCK_EX)
        return f
    except:
        try: f.close()
        except: pass
        return None

def _release_lock(lock_file):
    if not lock_file: return
    try:
        import fcntl
        fcntl.flock(lock_file, fcntl.LOCK_UN)
    finally:
        try: lock_file.close()
        except: pass

def load_chat_history():
    lock_file = None
    try:
        lock_file = _acquire_lock(LOCK_PATH)
        with shelve.open(SHELVE_FILENAME) as db:
            return db.get("messages", [])
    except:
        try:
            if os.path.exists(JSON_FALLBACK):
                with open(JSON_FALLBACK, "r", encoding="utf-8") as fh:
                    return json.load(fh)
        except: pass
        return []
    finally:
        _release_lock(lock_file)

def save_chat_history(messages):
    lock_file = None
    try:
        lock_file = _acquire_lock(LOCK_PATH)
        try:
            with shelve.open(SHELVE_FILENAME) as db:
                db["messages"] = messages
            return
        except: pass
    finally:
        _release_lock(lock_file)
    try:
        tmp = tempfile.NamedTemporaryFile("w", delete=False, dir=".")
        tmp_name = tmp.name
        with open(tmp_name, "w", encoding="utf-8") as fh:
            json.dump(messages, fh, ensure_ascii=False, indent=2)
        os.replace(tmp_name, JSON_FALLBACK)
    except: pass

# --- Generate float coordinates and store in session_state ---
def generate_float_data():
    if "float_data" not in st.session_state:
        regions = {
            "Arabian Sea": {"lat": (5, 25), "lon": (60, 75)},
            "Bay of Bengal": {"lat": (5, 22), "lon": (85, 95)},
            "Indian Ocean": {"lat": (-30, 20), "lon": (50, 95)},
        }
        float_data = {"Latitude": [], "Longitude": [], "Region": []}
        for region, bounds in regions.items():
            for _ in range(3):
                lat = random.uniform(*bounds["lat"])
                lon = random.uniform(*bounds["lon"])
                float_data["Latitude"].append(lat)
                float_data["Longitude"].append(lon)
                float_data["Region"].append(region)
        st.session_state["float_data"] = float_data
    return st.session_state["float_data"]

# --- Render stable Leaflet map with unique key ---
def render_float_map(dark_mode=True, terrain=False, key=None):
    float_data = generate_float_data()
    df_map = pd.DataFrame(float_data)
    
    tiles = 'CartoDB dark_matter' if dark_mode else 'OpenStreetMap'
    m = folium.Map(location=[df_map["Latitude"].mean(), df_map["Longitude"].mean()],
                   zoom_start=4, tiles=tiles)

    if terrain:
        folium.TileLayer(
            tiles='https://stamen-tiles.a.ssl.fastly.net/terrain/{z}/{x}/{y}.jpg',
            attr='Map tiles by <a href="http://stamen.com">Stamen Design</a>, '
                 'under <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a>. '
                 'Data by <a href="http://openstreetmap.org">OpenStreetMap</a>.',
            name='Stamen Terrain',
            overlay=True,
            control=True
        ).add_to(m)

    for _, row in df_map.iterrows():
        folium.Marker(
            location=[row["Latitude"], row["Longitude"]],
            popup=f"{row['Region']}",
            icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(m)

    if key is None:
        key = str(datetime.now().timestamp())
    st_folium(m, width=700, height=500, key=key)

# --- Generate Plotly charts ---
def generate_demo_graphs(user_input):
    text = user_input.lower()
    figs = []

    if "temperature" in text or "temp" in text:
        df_temp = pd.DataFrame({"Depth (m)": [0,50,100,200,500,1000],
                                "Temperature (°C)":[28,27,25,20,15,12]})
        fig_temp = px.line(df_temp, x="Temperature (°C)", y="Depth (m)", markers=True, title="Temperature Profile")
        fig_temp.update_yaxes(autorange="reversed")
        figs.append(fig_temp)

    if "salinity" in text or "salt" in text or "psu" in text:
        df_sal = pd.DataFrame({"Depth (m)":[0,50,100,200,500,1000],
                               "Salinity (PSU)":[36.2,36,35.7,35.5,35,34.8]})
        fig_sal = px.line(df_sal, x="Salinity (PSU)", y="Depth (m)", markers=True, title="Salinity Profile")
        fig_sal.update_yaxes(autorange="reversed")
        figs.append(fig_sal)

    if any(w in text for w in ["data","trend","analysis"]):
        df_trend = pd.DataFrame({"Date": pd.date_range(start="2025-01-01", periods=6, freq="M"),
                                 "Average Temperature":[27.5,27.6,27.8,28,28.2,28.1]})
        fig_trend = px.line(df_trend, x="Date", y="Average Temperature", markers=True, title="Monthly Avg Temperature Trend")
        figs.append(fig_trend)

    return figs

# --- Generate bot response ---
def generate_bot_response(user_input):
    figs = generate_demo_graphs(user_input)
    text = user_input.lower()
    responses = []
    if "temperature" in text: responses.append("Temperature profile generated.")
    if "salinity" in text: responses.append("Salinity profile included.")
    if any(w in text for w in ["floats","region","arabian sea","bay of bengal","indian ocean"]):
        responses.append("ARGO float locations mapped.")
    if any(w in text for w in ["data","trend","analysis"]):
        responses.append("Trend visualization prepared.")
    if not responses: responses=["Try asking about temperature, salinity, depth, or float locations."]
    return " ".join(responses), figs

# --- Display chat messages ---
def display_chat_messages(messages):
    for message in messages:
        if message.get("role")=="system": continue
        avatar = USER_AVATAR if message.get("role","assistant")=="user" else BOT_AVATAR
        with st.chat_message(message.get("role","assistant"), avatar=avatar):
            st.markdown(message.get("content",""))
            if figs := message.get("figures"):
                for i, fig in enumerate(figs):
                    st.plotly_chart(fig, use_container_width=True, key=f"{message['timestamp']}_{i}")
            if message.get("map"):
                render_float_map(dark_mode=True, terrain=True, key=f"map_{message['timestamp']}")
            if ts := message.get("timestamp"):
                try:
                    dt = datetime.fromisoformat(ts)
                    st.caption(dt.strftime("%Y-%m-%d %H:%M:%S"))
                except: pass

# --- Render chatbot ---
def render_floatchat():
    st.markdown('<div style="max-width: 900px; margin: auto;">', unsafe_allow_html=True)
    st.markdown("## 🤖 FloatChat AI")
    st.markdown("Interact with our AI assistant naturally.")

    # Sidebar
    with st.sidebar:
        st.markdown("### 💡 Suggested Queries")
        suggested_queries = [
            "Show me temperature profile in the Arabian Sea",
            "Salinity profile in Bay of Bengal",
            "Where are the active floats currently reporting?",
            "Compare temperature and salinity trends",
            "Show monthly average temperature trend",
            "Depth profile of temperature and salinity"
        ]
        for q in suggested_queries:
            if st.button(q, key=q):
                st.session_state["prefill_input"] = q

        if st.button("🗑️ Delete Chat History", key="delete_chat"):
            st.session_state.messages=[]
            if "float_data" in st.session_state: del st.session_state["float_data"]
            save_chat_history([])
            st.success("Chat history deleted.")
            st.rerun()

    # Load/init messages
    if "messages" not in st.session_state:
        st.session_state.messages = load_chat_history()
        if not st.session_state.messages:
            st.session_state.messages = [{
                "role":"assistant",
                "content":CHATBOT_CONFIG.get("welcome_message","Hello! Ask me about ARGO float data."),
                "timestamp":datetime.now().isoformat()
            }]
            save_chat_history(st.session_state.messages)

    display_chat_messages(st.session_state.messages)

    # --- Chat input with prefill ---
    prefill = st.session_state.pop("prefill_input", "") if "prefill_input" in st.session_state else ""
    if prefill:
        user_input = st.text_input("Ask me anything about ARGO ocean data...", value=prefill, key=f"prefill_{datetime.now().timestamp()}")
    else:
        user_input = st.chat_input("Ask me anything about ARGO ocean data...")

    if user_input:
        timestamp = datetime.now().isoformat()
        st.session_state.messages.append({"role":"user","content":user_input,"timestamp":timestamp})
        with st.chat_message("user", avatar=USER_AVATAR):
            st.markdown(user_input)

        bot_response, figs = generate_bot_response(user_input)
        map_needed = any(w in user_input.lower() for w in ["floats","region","arabian sea","bay of bengal","indian ocean"])
        st.session_state.messages.append({
            "role":"assistant",
            "content":bot_response,
            "figures":figs,
            "map": map_needed,
            "timestamp":timestamp
        })
        with st.chat_message("assistant", avatar=BOT_AVATAR):
            st.markdown(bot_response)
            for i, fig in enumerate(figs):
                st.plotly_chart(fig, use_container_width=True, key=f"{timestamp}_{i}")
            if map_needed:
                render_float_map(dark_mode=True, terrain=True, key=f"map_{timestamp}")

        save_chat_history(st.session_state.messages)

    st.markdown('</div>', unsafe_allow_html=True)
