# FloatChat - Conversational AI for ARGO Ocean Data

[![Smart India Hackathon 2025](https://img.shields.io/badge/SIH-2025-blue.svg)](https://sih.gov.in/)
[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.49+-red.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

FloatChat is a revolutionary platform that transforms how researchers, policymakers, and ocean enthusiasts interact with ARGO float oceanographic data through conversational AI.

## 🌊 Project Overview

FloatChat leverages cutting-edge AI technology to make ARGO float data accessible through natural language conversations. Our platform bridges the gap between complex oceanographic datasets and actionable insights for climate research, marine policy, and educational purposes.

### 🎯 Key Features

- **🗺️ Interactive Mapping**: Explore ARGO floats across global oceans with real-time positioning
- **💬 Natural Language Queries**: Ask questions in plain English and get instant insights
- **📊 Advanced Analytics**: Deep dive into temperature, salinity, and oceanographic parameters
- **🤖 AI-Powered Insights**: Get intelligent recommendations and pattern analysis
- **📚 Educational Tools**: Interactive learning for students and researchers
- **🏛️ Policy Support**: Evidence-based insights for marine policy making

## 🚀 Quick Start

### Prerequisites

- Python 3.13 or higher
- Virtual environment (recommended)
- Git

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Jayant-1/floatchat.git
   cd floatchat
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   streamlit run src/main.py
   ```

5. **Open your browser:**
   - Navigate to `http://localhost:8501`
   - Start exploring ocean data!

## 🚀 Deployment

### Deploy on Render
This application is configured for easy deployment on Render:

1. **Fork/Clone** this repository
2. **Connect** to Render (it will auto-detect the render.yaml configuration)
3. **Deploy** - Render will automatically:
   - Install dependencies from requirements.txt
   - Use Python 3.11.10 (specified in runtime.txt)
   - Start the application with the correct Streamlit command

### Live Demo
🌐 **[View Live Application](https://your-render-app-url.onrender.com)** *(Update with your Render URL)*

## 📋 Application Structure

```
floatchat2/
├── src/
│   ├── main.py                 # Main Streamlit application
│   ├── pages/                  # Individual page components
│   │   ├── home.py             # Home/overview page
│   │   ├── map_visualizer.py   # Interactive ARGO floats map
│   │   ├── data_explorer.py    # Data query and analysis
│   │   ├── chatbot.py          # Conversational AI interface
│   │   ├── about.py            # Research and documentation
│   │   └── admin.py            # Admin dashboard
│   └── utils/                  # Utility modules
│       ├── config.py           # Configuration settings
│       ├── data_generator.py   # Demo data generation
│       └── ui_components.py    # Reusable UI components
├── assets/                     # Static assets
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## 🎮 Using FloatChat

### 1. 🏠 Home Page
- Project overview and key features
- Quick navigation to different sections
- Platform statistics and recent updates

### 2. 🗺️ ARGO Floats Map
- Interactive world map with float locations
- Filter by region, status, and float type
- Click floats for detailed profiles
- View trajectory data and oceanographic measurements

### 3. 📊 Data Explorer
- Natural language query interface
- Advanced filtering and analysis tools
- Generate visualizations and comparisons
- Export data in multiple formats

### 4. 🤖 FloatChat AI
- Conversational interface for ocean data
- Ask questions in natural language
- Get intelligent insights and recommendations
- Export chat history and results

### 5. 📚 Research & About
- Comprehensive project documentation
- Research applications and case studies
- Technical references and bibliography
- Team information and credits

### 6. ⚙️ Admin Dashboard
- System monitoring and performance metrics
- Data management and quality control
- User analytics and usage patterns
- System settings and maintenance

## 💡 Example Queries

Try these sample queries in the Data Explorer or ChatBot:

- "Show me temperature profiles near the equator"
- "What's the average salinity in the Arabian Sea?"
- "Compare oxygen levels between different ocean regions"
- "Show me recent ARGO float trajectories"
- "What are the seasonal patterns in ocean temperature?"
- "Detect anomalies in recent temperature data"

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# Database Configuration
DATABASE_URL=postgresql://user:password@localhost/floatchat

# API Keys
ARGO_API_KEY=your_argo_api_key
WEATHER_API_KEY=your_weather_api_key

# AI Configuration
OPENAI_API_KEY=your_openai_key
MODEL_TEMPERATURE=0.7
MAX_TOKENS=2048

# Application Settings
DEBUG=False
LOG_LEVEL=INFO
CACHE_TTL=3600
```

### Advanced Configuration

Modify `src/utils/config.py` to customize:

- UI themes and colors
- Data processing parameters
- AI model settings
- Cache configuration

## 🧪 Development

### Running in Development Mode

```bash
# Enable debug mode
export STREAMLIT_ENV=development

# Run with auto-reload
streamlit run src/main.py --server.runOnSave=true
```

### Adding New Features

1. **New Page**: Create a new file in `src/pages/`
2. **UI Components**: Add reusable components to `src/utils/ui_components.py`
3. **Data Processing**: Extend `src/utils/data_generator.py`
4. **Configuration**: Update `src/utils/config.py`

### Code Style

- Follow PEP 8 guidelines
- Use type hints where possible
- Add docstrings to functions and classes
- Keep functions small and focused

## 🌐 Deployment

### Local Production

```bash
# Install production dependencies
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```

### Docker Deployment

```bash
# Build Docker image
docker build -t floatchat:latest .

# Run container
docker run -p 8501:8501 floatchat:latest
```

### Cloud Deployment

The application is cloud-ready and can be deployed on:

- **Streamlit Cloud**: Direct GitHub integration
- **Heroku**: Using `Procfile` and `requirements.txt`
- **AWS**: Using ECS or EC2 instances
- **Google Cloud**: Using Cloud Run or Compute Engine
- **Azure**: Using Container Instances or App Service

## 📊 Data Sources

- **ARGO Global Data Assembly Centre (GDAC)**: Primary ARGO float data
- **INCOIS**: Regional ocean data and validation
- **NIOT**: Technology and instrumentation data
- **Global Ocean Observing System (GOOS)**: Coordination and standards
- **World Ocean Database (WOD)**: Historical oceanographic data

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Ways to Contribute

- **Bug Reports**: Submit issues with detailed descriptions
- **Feature Requests**: Suggest new capabilities
- **Code Contributions**: Submit pull requests
- **Documentation**: Improve docs and tutorials
- **Testing**: Help test new features

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **ARGO Program**: For providing open access to global ocean data
- **Ministry of Earth Sciences**: For supporting ocean research and innovation
- **Smart India Hackathon 2025**: For the platform to develop innovative solutions
- **Open Source Community**: For the tools and frameworks that made this possible

## 📞 Contact

- **Project Team**: floatchat@oceanai.org
- **Technical Support**: support@floatchat.ai
- **Research Collaboration**: research@floatchat.ai
- **GitHub Repository**: [github.com/floatchat/ai-ocean](https://github.com/floatchat/ai-ocean)

## 🏆 Smart India Hackathon 2025

This project was developed for the Smart India Hackathon 2025, addressing the challenge of making ocean data accessible through conversational AI. Our solution demonstrates:

- **Innovation**: First conversational AI for ARGO data
- **Impact**: Democratizing access to ocean science
- **Scalability**: Ready for national deployment
- **Sustainability**: Supporting climate research and policy

---

<div align="center">
  <h3>🌊 Making Ocean Data Accessible to Everyone 🌊</h3>
  <p><em>Developed for Smart India Hackathon 2025</em></p>
</div>
