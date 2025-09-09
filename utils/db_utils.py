"""Database utility functions.

This module will contain helpers for connecting to and querying databases.
"""

from typing import Any
import time
import pandas as pd
import streamlit as st


@st.cache_resource(show_spinner=False)
def get_vector_db() -> Any:
    # Placeholder for a vector DB client
    time.sleep(0.25)
    return {"client": "mock-vector-db"}


@st.cache_data(show_spinner=False)
def load_float_metadata(days: int = 60) -> pd.DataFrame:
    # Simulate a heavier data load (cached)
    time.sleep(0.25)
    return pd.DataFrame({"id": [1, 2, 3], "days": [days, days, days]}) 