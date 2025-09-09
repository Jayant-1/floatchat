import streamlit as st
from datetime import date, timedelta
import os

# App configuration
st.set_page_config(
    page_title="FloatChat",
    layout="wide",
)

# Optional authentication
if os.getenv("ENABLE_AUTH", "false").lower() == "true":
    try:
        import streamlit_authenticator as stauth
        names = [os.getenv("AUTH_NAME", "Demo User")]
        usernames = [os.getenv("AUTH_USERNAME", "demo")]
        passwords = [os.getenv("AUTH_PASSWORD", "demo123")]  # In production, use hashed passwords
        credentials = {"usernames": {usernames[0]: {"name": names[0], "password": passwords[0]}}}
        authenticator = stauth.Authenticate(credentials, "floatchat_cookie", "floatchat_key", cookie_expiry_days=1)
        name, auth_status, username = authenticator.login("Login", "main")
        if auth_status:
            st.session_state["username"] = username
            authenticator.logout("Logout", "sidebar")
        elif auth_status is False:
            st.error("Username/password is incorrect")
        else:
            st.warning("Please enter your username and password")
            st.stop()
    except Exception:
        pass

# Preload Google Fonts
st.markdown(
    """
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Poppins:wght@400;600;700&display=swap" rel="stylesheet">
    """,
    unsafe_allow_html=True,
)

# Load global CSS
try:
    with open("assets/style.css", "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    pass

# Top navbar
st.markdown(
    """
    <div class="topnav">
      <div class="topnav-inner">
        <div class="brand">
          <img src="https://raw.githubusercontent.com/simple-icons/simple-icons/develop/icons/oceanprotocol.svg" alt="logo" />
          <span>FloatChat</span>
        </div>
        <div class="links">
          <a href="/?page=Chatbot">Chatbot</a>
          <a href="/?page=Map%20Explorer">Map</a>
          <a href="/?page=Profile%20Plots">Plots</a>
          <a href="/?page=Data%20Downloads">Downloads</a>
        </div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Initialize session state for global filters/messages
if "filters" not in st.session_state:
    st.session_state.filters = {
        "date_start": date.today() - timedelta(days=60),
        "date_end": date.today(),
        "region": "Global",
        "depth": 2000,
        "variable": "Temperature",
    }
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! I am FloatChat. Ask me about ARGO floats, profiles, or ocean data."}
    ]

# Sidebar: logo + global filters
with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-logo">
          <img src="https://raw.githubusercontent.com/simple-icons/simple-icons/develop/icons/oceanprotocol.svg" alt="FloatChat logo"/>
          <div class="brand">FloatChat</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.info("Global Filters")
    d_start, d_end = st.date_input(
        "Date range",
        value=(st.session_state.filters["date_start"], st.session_state.filters["date_end"]),
    )
    st.session_state.filters["date_start"], st.session_state.filters["date_end"] = d_start, d_end

    region = st.selectbox(
        "Region",
        ["Global", "Indian", "Pacific", "Atlantic", "Southern"],
        index=["Global", "Indian", "Pacific", "Atlantic", "Southern"].index(st.session_state.filters["region"]) if st.session_state.filters["region"] in ["Global", "Indian", "Pacific", "Atlantic", "Southern"] else 0,
    )
    st.session_state.filters["region"] = region

    depth = st.slider("Max depth (m)", 0, 6000, value=st.session_state.filters["depth"], step=50)
    st.session_state.filters["depth"] = depth

    variable = st.radio("Variable", ["Temperature", "Salinity", "Oxygen", "Chl-a"], index=["Temperature", "Salinity", "Oxygen", "Chl-a"].index(st.session_state.filters["variable"]))
    st.session_state.filters["variable"] = variable

    st.caption("Filters persist across pages and update visualizations instantly.")

# Clean hero header (no footer, no bubbles)
st.markdown(
    """
    <div style="padding: 18px 8px;">
      <div style="font-weight:700; font-size: 26px; letter-spacing:0.3px;">FloatChat — Ocean Data, Simplified</div>
      <div style="color:#94a3b8; margin-top:4px;">Chat. Map. Plot. Download. A minimal and stylish ocean analytics workspace.</div>
    </div>
    """,
    unsafe_allow_html=True,
) 