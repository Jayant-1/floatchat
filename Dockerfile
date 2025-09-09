# syntax=docker/dockerfile:1
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy and install deps first (better layer caching)
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Copy app
COPY . .

# Expose default Streamlit port
EXPOSE 8501

# Environment
ENV STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Run
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"] 