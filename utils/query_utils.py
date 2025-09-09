"""Query helper functions.

This module will contain helpers to build and validate user queries.
"""

from datetime import date, timedelta
import streamlit as st


def init_session_state() -> None:
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
            {
                "role": "assistant",
                "content": "Hi! I am FloatChat. Ask me about ARGO floats, profiles, or ocean data.",
            }
        ]


def render_global_sidebar() -> None:
    with st.sidebar:
        st.markdown(
            """
            <div class=\"sidebar-logo\">
              <img src=\"https://raw.githubusercontent.com/simple-icons/simple-icons/develop/icons/oceanprotocol.svg\" alt=\"FloatChat logo\"/>
              <div class=\"brand\">FloatChat</div>
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