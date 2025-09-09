from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Tuple

import pandas as pd
import streamlit as st
from sqlalchemy import Column, DateTime, Integer, String, Text, create_engine, select, func
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column


class Base(DeclarativeBase):
    pass


class ChatRecord(Base):
    __tablename__ = "chat_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    session_id: Mapped[str] = mapped_column(String(128), index=True)
    user_message: Mapped[str] = mapped_column(Text)
    bot_response: Mapped[str] = mapped_column(Text)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=False), default=datetime.utcnow, index=True)


@st.cache_resource(show_spinner=False)
def get_engine() -> Engine:
    url = os.getenv("DATABASE_URL")
    if not url:
        # Local dev default
        url = "sqlite:///floatchat.db"
    # For SQLite, enable check_same_thread=False for Streamlit multi-threads
    connect_args = {"check_same_thread": False} if url.startswith("sqlite") else {}
    engine = create_engine(url, echo=False, future=True, connect_args=connect_args)
    Base.metadata.create_all(engine)
    return engine


def init_db() -> None:
    # Ensures tables are created
    _ = get_engine()


def save_chat_message(session_id: str, user_message: str, bot_response: str, ts: Optional[datetime] = None) -> int:
    engine = get_engine()
    record = ChatRecord(session_id=session_id, user_message=user_message, bot_response=bot_response, timestamp=ts or datetime.utcnow())
    with Session(engine) as s:
        s.add(record)
        s.commit()
        s.refresh(record)
        # Invalidate cached fetch for this session
        fetch_chat_history.clear()
        return record.id


@st.cache_data(show_spinner=False)
def fetch_chat_history(session_id: str, keyword: Optional[str] = None, limit: int = 500) -> pd.DataFrame:
    engine = get_engine()
    with Session(engine) as s:
        stmt = select(ChatRecord).where(ChatRecord.session_id == session_id).order_by(ChatRecord.timestamp.desc()).limit(limit)
        rows = s.execute(stmt).scalars().all()
    data = [
        {
            "id": r.id,
            "session_id": r.session_id,
            "user_message": r.user_message,
            "bot_response": r.bot_response,
            "timestamp": r.timestamp,
        }
        for r in rows
    ]
    df = pd.DataFrame(data)
    if keyword and not df.empty:
        mask = df.apply(lambda row: (keyword.lower() in str(row["user_message"]).lower()) or (keyword.lower() in str(row["bot_response"]).lower()), axis=1)
        df = df[mask]
    return df


def clear_chat_history(session_id: str) -> int:
    engine = get_engine()
    with Session(engine) as s:
        deleted = s.query(ChatRecord).filter(ChatRecord.session_id == session_id).delete()
        s.commit()
        # Invalidate cache
        fetch_chat_history.clear()
        return deleted


def export_history_csv(df: pd.DataFrame) -> str:
    return df.to_csv(index=False) 