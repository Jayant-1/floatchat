# FloatChat Dockerfile
# Smart India Hackathon 2025

FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY README.md .
COPY start_floatchat.sh .

# Create .streamlit directory and copy config
RUN mkdir -p ./.streamlit


# Make startup script executable
RUN chmod +x start_floatchat.sh

# Create non-root user
RUN useradd -m -s /bin/bash floatchat
RUN chown -R floatchat:floatchat /app
USER floatchat

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Start command
CMD ["streamlit", "run", "src/main2.py", "--server.address", "0.0.0.0", "--server.port", "8501"]
