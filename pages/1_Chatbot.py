import asyncio
import time
import uuid
import streamlit as st

from chat_engine import ChatMessage, build_engine
from utils import export_chat_as_json, export_chat_as_txt, sanitize_user_input
from db import save_chat_message, fetch_chat_history, clear_chat_history, export_history_csv

st.title("🤖 Chatbot")

# Session id for persistence
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# Floating ocean icon for branding
st.markdown("<div class=\"floating-icon\">🌊</div>", unsafe_allow_html=True)

# Neon bubbles background layer
st.markdown(
    """
    <div class="bubbles">
      <span style="left:8%; bottom:12%"></span>
      <span style="left:18%; bottom:8%"></span>
      <span style="left:38%; bottom:10%"></span>
      <span style="left:58%; bottom:14%"></span>
      <span style="left:78%; bottom:9%"></span>
    </div>
    """,
    unsafe_allow_html=True,
)

# messages persisted in st.session_state from app.py
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! I am FloatChat. Ask me about ARGO floats, profiles, or ocean data."}
    ]

# History controls
colH1, colH2, colH3, colH4 = st.columns([1, 1, 1, 1])
with colH1:
    kw = st.text_input("Search history")
with colH2:
    if st.button("Load history"):
        df = fetch_chat_history(st.session_state.session_id, keyword=kw)
        if not df.empty:
            # Merge into messages (latest first in df)
            st.session_state.messages = []
            for _, row in df.sort_values("timestamp").iterrows():
                st.session_state.messages.append({"role": "user", "content": row["user_message"]})
                st.session_state.messages.append({"role": "assistant", "content": row["bot_response"]})
with colH3:
    if st.button("Clear history"):
        clear_chat_history(st.session_state.session_id)
        st.session_state.messages = []
with colH4:
    if st.button("Export .csv"):
        df = fetch_chat_history(st.session_state.session_id)
        st.download_button("Download .csv", export_history_csv(df), file_name="floatchat_history.csv", mime="text/csv")

# Exports
colE1, colE2 = st.columns([1, 1])
with colE1:
    st.download_button("Export .txt", export_chat_as_txt(st.session_state.messages), file_name="floatchat_history.txt")
with colE2:
    st.download_button("Export .json", export_chat_as_json(st.session_state.messages), file_name="floatchat_history.json")

# Render chat history with styled bubbles
for msg in st.session_state.messages:
    cls = "chat-user" if msg["role"] == "user" else "chat-assistant"
    row = "user" if msg["role"] == "user" else "assistant"
    with st.chat_message(msg["role"]):
        st.markdown(f"<div class='chat-row {row}'><div class='chat-bubble {cls}'>{msg['content']}</div></div>", unsafe_allow_html=True)

prompt = st.chat_input("Ask about ocean data…")

async def handle_chat(user_text: str) -> None:
    provider = st.session_state.get("provider", "openai")
    engine = build_engine(provider=provider)
    # Add user message
    clean = sanitize_user_input(user_text)
    st.session_state.messages.append({"role": "user", "content": clean})
    with st.chat_message("user"):
        st.markdown(f"<div class='chat-row user'><div class='chat-bubble chat-user'>{clean}</div></div>", unsafe_allow_html=True)

    # Typing indicator
    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.markdown("<div class='chat-row assistant'><div class='chat-bubble chat-assistant'><span class='typing-dots'><span class='dot'></span><span class='dot'></span><span class='dot'></span></span></div></div>", unsafe_allow_html=True)
        # Stream tokens
        full = ""
        async for token in engine.stream_reply([ChatMessage(**m) for m in st.session_state.messages]):
            full += token
            placeholder.markdown(f"<div class='chat-row assistant'><div class='chat-bubble chat-assistant'>{full}</div></div>", unsafe_allow_html=True)
        # Finalize
        placeholder.markdown(f"<div class='chat-row assistant'><div class='chat-bubble chat-assistant'>{full}</div></div>", unsafe_allow_html=True)
        st.session_state.messages.append({"role": "assistant", "content": full})
        # Persist
        save_chat_message(st.session_state.session_id, clean, full)

if prompt:
    asyncio.run(handle_chat(prompt)) 