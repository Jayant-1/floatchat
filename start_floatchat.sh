#!/bin/bash

# FloatChat Startup Script
# Smart India Hackathon 2025

echo "🌊 Starting FloatChat - Conversational AI for ARGO Ocean Data 🌊"
echo "================================================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed. Please install Python 3.13 or higher."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
REQUIRED_VERSION="3.13"

if [[ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]]; then
    echo "❌ Error: Python $REQUIRED_VERSION or higher is required. Found: $PYTHON_VERSION"
    exit 1
fi

echo "✅ Python $PYTHON_VERSION detected"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "❌ Error: Failed to create virtual environment"
        exit 1
    fi
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Check if requirements are installed
if [ ! -f "venv/lib/python*/site-packages/streamlit/__init__.py" ]; then
    echo "📥 Installing dependencies..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ Error: Failed to install dependencies"
        exit 1
    fi
    echo "✅ Dependencies installed"
else
    echo "✅ Dependencies already installed"
fi

# Change to source directory
cd src

# Check if main.py exists
if [ ! -f "main.py" ]; then
    echo "❌ Error: main.py not found in src directory"
    exit 1
fi

echo "🚀 Launching FloatChat application..."
echo ""
echo "📋 Application will open in your default browser at:"
echo "🌐 http://localhost:8501"
echo ""
echo "💡 Tips:"
echo "   - Use Ctrl+C to stop the application"
echo "   - Navigate between pages using the sidebar"
echo "   - Try the sample queries in the chatbot"
echo "   - Explore the interactive map by clicking on float markers"
echo ""
echo "================================================================"

# Start Streamlit application
streamlit run main.py --server.headless=true --server.address=0.0.0.0 --server.port=8501

echo ""
echo "👋 FloatChat application stopped. Thank you for using our platform!"
echo "🌊 Smart India Hackathon 2025 - Making Ocean Data Accessible 🌊"
