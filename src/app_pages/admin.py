"""
Admin Dashboard for FloatChat application
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import time
from utils.ui_components import render_metric_cards, render_data_table, render_info_box, render_status_indicator

def render_admin_page():
    """Render the admin dashboard page"""
    
    st.markdown("## ⚙️ Admin Dashboard")
    st.markdown("System monitoring, data management, and administrative controls for FloatChat platform.")
    
    # Check admin access (simplified for demo)
    if 'admin_authenticated' not in st.session_state:
        st.session_state.admin_authenticated = False
    
    if not st.session_state.admin_authenticated:
        render_admin_login()
        return
    
    # Main admin interface
    render_admin_interface()

def render_admin_login():
    """Render admin login interface"""
    
    st.markdown("### 🔐 Admin Access Required")
    
    with st.form("admin_login"):
        st.markdown("Please enter admin credentials to access the dashboard.")
        
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        
        if submitted:
            # Simple authentication (in production, use proper auth)
            if username == "admin" and password == "floatchat2025":
                st.session_state.admin_authenticated = True
                st.success("Login successful! Redirecting to admin dashboard...")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Invalid credentials. Please try again.")
    
    st.info("**Demo Credentials:** Username: `admin`, Password: `floatchat2025`")

def render_admin_interface():
    """Render the main admin interface"""
    
    # Logout button
    col1, col2 = st.columns([6, 1])
    with col2:
        if st.button("🚪 Logout"):
            st.session_state.admin_authenticated = False
            st.rerun()
    
    # Admin navigation
    admin_tab1, admin_tab2, admin_tab3, admin_tab4, admin_tab5 = st.tabs([
        "📊 System Overview",
        "🌊 Data Management", 
        "👥 User Analytics",
        "🔧 System Settings",
        "📋 Logs & Monitoring"
    ])
    
    with admin_tab1:
        render_system_overview()
    
    with admin_tab2:
        render_data_management()
    
    with admin_tab3:
        render_user_analytics()
    
    with admin_tab4:
        render_system_settings()
    
    with admin_tab5:
        render_logs_monitoring()

def render_system_overview():
    """Render system overview dashboard"""
    
    st.markdown("### 📊 System Overview")
    
    # Current timestamp
    st.markdown(f"**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Key metrics
    st.markdown("#### 🎯 Key Performance Indicators")
    
    metrics_data = [
        ("System Uptime", "99.8%", "+0.1%", "Last 30 days availability"),
        ("Active Users", "1,247", "+56 today", "Currently online users"),
        ("Data Processing", "2.1M", "Points/day", "Real-time data throughput"),
        ("API Calls", "15.6K", "+890 today", "Total API requests")
    ]
    
    render_metric_cards(metrics_data)
    
    # System health indicators
    st.markdown("#### 🏥 System Health")
    
    health_col1, health_col2, health_col3 = st.columns(3)
    
    with health_col1:
        st.markdown("**Core Services**")
        render_status_indicator("Active", "Web Server")
        render_status_indicator("Active", "Database")
        render_status_indicator("Active", "AI Engine")
        render_status_indicator("Maintenance", "Cache Server")
    
    with health_col2:
        st.markdown("**Data Sources**")
        render_status_indicator("Active", "ARGO GDAC")
        render_status_indicator("Active", "INCOIS Feed")
        render_status_indicator("Active", "Real-time Stream")
        render_status_indicator("Inactive", "Backup Source")
    
    with health_col3:
        st.markdown("**External APIs**")
        render_status_indicator("Active", "Weather API")
        render_status_indicator("Active", "Geocoding API")
        render_status_indicator("Active", "Email Service")
        render_status_indicator("Active", "Analytics API")
    
    # Performance charts
    st.markdown("#### 📈 Performance Metrics")
    
    # Generate sample performance data
    dates = pd.date_range(start=datetime.now()-timedelta(days=7), periods=7, freq='D')
    performance_data = pd.DataFrame({
        'date': dates,
        'response_time': np.random.uniform(200, 800, 7),
        'cpu_usage': np.random.uniform(30, 80, 7),
        'memory_usage': np.random.uniform(40, 85, 7),
        'active_sessions': np.random.randint(800, 1500, 7)
    })
    
    perf_col1, perf_col2 = st.columns(2)
    
    with perf_col1:
        fig_response = px.line(performance_data, x='date', y='response_time', 
                              title='Average Response Time (ms)')
        fig_response.update_layout(height=300)
        st.plotly_chart(fig_response, use_container_width=True)
    
    with perf_col2:
        fig_usage = px.line(performance_data, x='date', y=['cpu_usage', 'memory_usage'], 
                           title='System Resource Usage (%)')
        fig_usage.update_layout(height=300)
        st.plotly_chart(fig_usage, use_container_width=True)
    
    # Error rates and alerts
    st.markdown("#### ⚠️ Alerts & Issues")
    
    alerts_data = pd.DataFrame({
        'Timestamp': [
            datetime.now() - timedelta(hours=2),
            datetime.now() - timedelta(hours=6),
            datetime.now() - timedelta(days=1)
        ],
        'Level': ['Warning', 'Info', 'Warning'],
        'Component': ['Cache Server', 'Data Pipeline', 'Load Balancer'],
        'Message': [
            'High memory usage detected (85%)',
            'Scheduled maintenance completed successfully',
            'Increased response times during peak hours'
        ],
        'Status': ['Active', 'Resolved', 'Resolved']
    })
    
    render_data_table(alerts_data, "Recent System Alerts")

def render_data_management():
    """Render data management interface"""
    
    st.markdown("### 🌊 Data Management")
    
    # Data pipeline status
    st.markdown("#### 🔄 Data Pipeline Status")
    
    pipeline_col1, pipeline_col2 = st.columns(2)
    
    with pipeline_col1:
        st.markdown("**ARGO Data Ingestion**")
        
        # Simulate pipeline progress
        if st.button("🔄 Refresh ARGO Data"):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for i in range(101):
                progress_bar.progress(i)
                status_text.text(f'Processing ARGO data... {i}%')
                time.sleep(0.01)
            
            status_text.text('ARGO data refresh completed!')
            st.success("Successfully updated 3,847 float profiles")
        
        st.markdown("**Last Update:** 2 hours ago")
        st.markdown("**Next Scheduled:** In 4 hours")
        st.markdown("**Data Volume:** 156 MB today")
    
    with pipeline_col2:
        st.markdown("**Quality Control**")
        
        qc_metrics = [
            ("Valid Profiles", "96.8%", "↑ 0.2%"),
            ("Flagged Data", "2.1%", "↓ 0.1%"), 
            ("Missing Values", "1.1%", "→ 0.0%")
        ]
        
        for metric, value, change in qc_metrics:
            st.metric(metric, value, change)
    
    # Data statistics
    st.markdown("#### 📊 Data Statistics")
    
    # Generate sample data statistics
    data_stats = pd.DataFrame({
        'Parameter': ['Temperature', 'Salinity', 'Depth', 'Location'],
        'Total Records': [2156789, 2156789, 2156789, 1876543],
        'Today': [15678, 15678, 15678, 13456],
        'Quality Score': [98.5, 97.8, 99.2, 95.6],
        'Coverage (%)': [100, 100, 100, 87]
    })
    
    render_data_table(data_stats, "Data Quality Statistics")
    
    # Manual data operations
    st.markdown("#### 🛠️ Data Operations")
    
    op_col1, op_col2, op_col3 = st.columns(3)
    
    with op_col1:
        st.markdown("**Import Operations**")
        
        uploaded_file = st.file_uploader(
            "Upload NetCDF File",
            type=['nc', 'netcdf'],
            help="Upload ARGO float data in NetCDF format"
        )
        
        if uploaded_file:
            st.info(f"File: {uploaded_file.name}")
            if st.button("📤 Process Upload"):
                st.success("File processed successfully!")
    
    with op_col2:
        st.markdown("**Export Operations**")
        
        export_format = st.selectbox("Export Format", ["CSV", "JSON", "NetCDF", "Parquet"])
        date_range = st.date_input("Date Range", value=(datetime.now()-timedelta(days=7), datetime.now()))
        
        if st.button("📥 Generate Export"):
            st.info(f"Generating {export_format} export for selected date range...")
    
    with op_col3:
        st.markdown("**Maintenance**")
        
        if st.button("🗑️ Clean Temp Files"):
            st.success("Temporary files cleaned (2.3 GB freed)")
        
        if st.button("🔄 Rebuild Indexes"):
            st.success("Database indexes rebuilt successfully")
        
        if st.button("📦 Backup Database"):
            st.success("Database backup initiated")
    
    # Data validation results
    st.markdown("#### ✅ Data Validation Results")
    
    validation_data = pd.DataFrame({
        'Test': [
            'Temperature Range Check',
            'Salinity Bounds Validation',
            'Depth Sequence Verification',
            'Timestamp Consistency',
            'Duplicate Detection',
            'Coordinate Validation'
        ],
        'Status': ['Passed', 'Passed', 'Warning', 'Passed', 'Passed', 'Failed'],
        'Records Tested': [156789, 156789, 156789, 156789, 156789, 156789],
        'Issues Found': [0, 0, 23, 0, 0, 156],
        'Last Run': [
            '2 hours ago', '2 hours ago', '2 hours ago',
            '2 hours ago', '2 hours ago', '2 hours ago'
        ]
    })
    
    render_data_table(validation_data, "Automated Data Validation")

def render_user_analytics():
    """Render user analytics dashboard"""
    
    st.markdown("### 👥 User Analytics")
    
    # User metrics
    st.markdown("#### 📊 User Engagement")
    
    user_metrics = [
        ("Total Users", "2,456", "+89 this week", "Registered users"),
        ("Active Today", "342", "+12%", "Users active in last 24 hours"),
        ("Avg Session", "18 min", "+2 min", "Average session duration"),
        ("Queries/User", "8.3", "+1.2", "Average queries per session")
    ]
    
    render_metric_cards(user_metrics)
    
    # Usage patterns
    st.markdown("#### 📈 Usage Patterns")
    
    # Generate sample usage data
    hours = list(range(24))
    usage_by_hour = [np.random.poisson(50 + 30*np.sin((h-12)*np.pi/12)) for h in hours]
    
    fig_hourly = px.bar(x=hours, y=usage_by_hour, 
                        title="User Activity by Hour of Day",
                        labels={'x': 'Hour', 'y': 'Active Users'})
    st.plotly_chart(fig_hourly, use_container_width=True)
    
    # Feature usage
    st.markdown("#### 🎯 Feature Usage")
    
    feature_col1, feature_col2 = st.columns(2)
    
    with feature_col1:
        feature_usage = {
            'Map Visualizer': 45,
            'Data Explorer': 32, 
            'FloatChat AI': 28,
            'Research Pages': 15,
            'Admin Dashboard': 2
        }
        
        fig_features = px.pie(values=list(feature_usage.values()), 
                             names=list(feature_usage.keys()),
                             title="Feature Usage Distribution")
        st.plotly_chart(fig_features, use_container_width=True)
    
    with feature_col2:
        # Query types
        query_types = {
            'Temperature Queries': 38,
            'Salinity Analysis': 25,
            'Regional Comparisons': 18,
            'Trend Analysis': 12,
            'General Questions': 7
        }
        
        fig_queries = px.bar(x=list(query_types.values()), 
                            y=list(query_types.keys()),
                            orientation='h',
                            title="AI Query Types")
        st.plotly_chart(fig_queries, use_container_width=True)
    
    # User feedback
    st.markdown("#### 💬 User Feedback")
    
    feedback_data = pd.DataFrame({
        'Date': pd.date_range(start=datetime.now()-timedelta(days=5), periods=5),
        'Feedback Type': ['Bug Report', 'Feature Request', 'Positive', 'Suggestion', 'Question'],
        'User': ['user_123', 'researcher_45', 'student_78', 'policy_12', 'scientist_34'],
        'Category': ['Map', 'AI Chat', 'Overall', 'Data Export', 'Documentation'],
        'Status': ['In Progress', 'Planned', 'Acknowledged', 'Completed', 'Responded'],
        'Priority': ['High', 'Medium', 'Low', 'Medium', 'Low']
    })
    
    render_data_table(feedback_data, "Recent User Feedback")

def render_system_settings():
    """Render system settings interface"""
    
    st.markdown("### 🔧 System Settings")
    
    # General settings
    st.markdown("#### ⚙️ General Configuration")
    
    settings_col1, settings_col2 = st.columns(2)
    
    with settings_col1:
        st.markdown("**Performance Settings**")
        
        max_concurrent_users = st.slider("Max Concurrent Users", 100, 2000, 1000)
        query_timeout = st.slider("Query Timeout (seconds)", 10, 120, 30)
        cache_ttl = st.slider("Cache TTL (hours)", 1, 24, 6)
        
        if st.button("💾 Save Performance Settings"):
            st.success("Performance settings saved successfully!")
    
    with settings_col2:
        st.markdown("**Data Settings**")
        
        auto_refresh = st.checkbox("Auto-refresh ARGO data", value=True)
        data_retention = st.selectbox("Data Retention Period", ["1 year", "2 years", "5 years", "Indefinite"])
        quality_threshold = st.slider("Quality Score Threshold", 0.8, 1.0, 0.95)
        
        if st.button("💾 Save Data Settings"):
            st.success("Data settings saved successfully!")
    
    # API configuration
    st.markdown("#### 🔌 API Configuration")
    
    api_col1, api_col2 = st.columns(2)
    
    with api_col1:
        st.markdown("**Rate Limiting**")
        
        api_rate_limit = st.number_input("Requests per minute", 1, 1000, 100)
        api_burst_limit = st.number_input("Burst limit", 1, 500, 50)
        
        if st.button("💾 Save API Settings"):
            st.success("API settings saved successfully!")
    
    with api_col2:
        st.markdown("**Authentication**")
        
        require_auth = st.checkbox("Require authentication", value=False)
        session_timeout = st.selectbox("Session timeout", ["1 hour", "4 hours", "8 hours", "24 hours"])
        
        if st.button("💾 Save Auth Settings"):
            st.success("Authentication settings saved successfully!")
    
    # AI model settings
    st.markdown("#### 🤖 AI Model Configuration")
    
    ai_col1, ai_col2 = st.columns(2)
    
    with ai_col1:
        st.markdown("**Model Parameters**")
        
        model_temperature = st.slider("Model Temperature", 0.1, 1.0, 0.7)
        max_response_length = st.slider("Max Response Length", 50, 500, 200)
        confidence_threshold = st.slider("Confidence Threshold", 0.5, 1.0, 0.8)
    
    with ai_col2:
        st.markdown("**Training Settings**")
        
        auto_retrain = st.checkbox("Auto-retrain on new data", value=True)
        training_frequency = st.selectbox("Training Frequency", ["Daily", "Weekly", "Monthly"])
        training_data_size = st.selectbox("Training Data Size", ["1K", "10K", "100K", "All"])
    
    if st.button("🤖 Update AI Model Settings"):
        st.success("AI model settings updated successfully!")
    
    # System maintenance
    st.markdown("#### 🛠️ System Maintenance")
    
    maintenance_col1, maintenance_col2 = st.columns(2)
    
    with maintenance_col1:
        st.markdown("**Scheduled Maintenance**")
        
        maintenance_window = st.time_input("Maintenance Window Start", datetime.now().time())
        maintenance_duration = st.selectbox("Duration", ["1 hour", "2 hours", "4 hours"])
        
        if st.button("📅 Schedule Maintenance"):
            st.success("Maintenance scheduled successfully!")
    
    with maintenance_col2:
        st.markdown("**System Controls**")
        
        if st.button("🔄 Restart Services", type="secondary"):
            st.warning("Service restart initiated...")
        
        if st.button("🛑 Enable Maintenance Mode", type="secondary"):
            st.warning("Maintenance mode enabled")
        
        if st.button("⚠️ Emergency Shutdown", type="secondary"):
            st.error("Emergency shutdown procedures activated")

def render_logs_monitoring():
    """Render logs and monitoring interface"""
    
    st.markdown("### 📋 Logs & Monitoring")
    
    # Log filters
    st.markdown("#### 🔍 Log Filters")
    
    filter_col1, filter_col2, filter_col3 = st.columns(3)
    
    with filter_col1:
        log_level = st.selectbox("Log Level", ["All", "ERROR", "WARNING", "INFO", "DEBUG"])
        
    with filter_col2:
        log_component = st.selectbox("Component", ["All", "Web Server", "AI Engine", "Database", "Data Pipeline"])
        
    with filter_col3:
        log_timeframe = st.selectbox("Timeframe", ["Last Hour", "Last 24 Hours", "Last Week", "Custom"])
    
    # Generate sample log data
    log_data = pd.DataFrame({
        'Timestamp': [
            datetime.now() - timedelta(minutes=5),
            datetime.now() - timedelta(minutes=12),
            datetime.now() - timedelta(minutes=23),
            datetime.now() - timedelta(minutes=31),
            datetime.now() - timedelta(minutes=45),
            datetime.now() - timedelta(hours=1, minutes=15),
            datetime.now() - timedelta(hours=2, minutes=5),
            datetime.now() - timedelta(hours=3, minutes=22)
        ],
        'Level': ['INFO', 'WARNING', 'INFO', 'ERROR', 'INFO', 'INFO', 'WARNING', 'INFO'],
        'Component': ['Web Server', 'Database', 'AI Engine', 'Data Pipeline', 'Web Server', 'AI Engine', 'Database', 'Web Server'],
        'Message': [
            'User query processed successfully',
            'High memory usage detected (85%)',
            'Chat response generated in 1.2s',
            'Failed to connect to ARGO GDAC',
            'New user registered: user_1234',
            'Model inference completed',
            'Slow query detected (3.2s)',
            'API request rate limit exceeded'
        ],
        'User': ['user_123', 'system', 'user_456', 'system', 'user_789', 'user_456', 'system', 'user_321']
    })
    
    # Apply filters (simplified)
    filtered_logs = log_data.copy()
    if log_level != "All":
        filtered_logs = filtered_logs[filtered_logs['Level'] == log_level]
    if log_component != "All":
        filtered_logs = filtered_logs[filtered_logs['Component'] == log_component]
    
    render_data_table(filtered_logs, "System Logs")
    
    # Error analysis
    st.markdown("#### ⚠️ Error Analysis")
    
    error_col1, error_col2 = st.columns(2)
    
    with error_col1:
        # Error frequency over time
        error_times = pd.date_range(start=datetime.now()-timedelta(hours=24), periods=24, freq='H')
        error_counts = np.random.poisson(2, 24)
        
        fig_errors = px.line(x=error_times, y=error_counts,
                            title="Error Frequency (Last 24 Hours)",
                            labels={'x': 'Hour', 'y': 'Error Count'})
        st.plotly_chart(fig_errors, use_container_width=True)
    
    with error_col2:
        # Error types
        error_types = {
            'Connection Timeout': 12,
            'Data Validation': 8,
            'Authentication': 5,
            'Resource Limit': 3,
            'Other': 2
        }
        
        fig_error_types = px.pie(values=list(error_types.values()),
                                names=list(error_types.keys()),
                                title="Error Types Distribution")
        st.plotly_chart(fig_error_types, use_container_width=True)
    
    # Performance monitoring
    st.markdown("#### 📊 Performance Monitoring")
    
    # Real-time metrics simulation
    if st.button("🔄 Refresh Real-time Metrics"):
        with st.spinner("Collecting metrics..."):
            time.sleep(1)
            
            real_time_col1, real_time_col2, real_time_col3 = st.columns(3)
            
            with real_time_col1:
                st.metric("CPU Usage", f"{np.random.uniform(30, 80):.1f}%", f"{np.random.uniform(-5, 5):.1f}%")
                st.metric("Memory Usage", f"{np.random.uniform(40, 85):.1f}%", f"{np.random.uniform(-3, 7):.1f}%")
                
            with real_time_col2:
                st.metric("Active Connections", f"{np.random.randint(800, 1200)}", f"{np.random.randint(-50, 100)}")
                st.metric("Queue Length", f"{np.random.randint(0, 25)}", f"{np.random.randint(-10, 15)}")
                
            with real_time_col3:
                st.metric("Response Time", f"{np.random.uniform(200, 800):.0f}ms", f"{np.random.uniform(-100, 200):.0f}ms")
                st.metric("Throughput", f"{np.random.uniform(50, 150):.0f} req/sec", f"{np.random.uniform(-20, 30):.0f}")
    
    # Export logs
    st.markdown("#### 📥 Export Options")
    
    export_col1, export_col2 = st.columns(2)
    
    with export_col1:
        if st.button("📄 Export Filtered Logs"):
            csv_data = filtered_logs.to_csv(index=False)
            st.download_button(
                "Download CSV",
                csv_data,
                f"system_logs_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                "text/csv"
            )
    
    with export_col2:
        if st.button("📊 Generate Report"):
            st.success("System report generated and sent to administrators!")
