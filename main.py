import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Financial Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark mode aesthetics
st.markdown("""
    <style>
    /* Main theme colors */
    :root {
        --bg-primary: #0e1117;
        --bg-secondary: #1a1d24;
        --bg-card: #262730;
        --text-primary: #e8e8ea;
        --text-secondary: #b0b3b8;
        --accent: #00d4ff;
        --accent-hover: #00a8cc;
        --success: #00ff88;
        --warning: #ffaa00;
        --danger: #ff3366;
    }
    
    /* Streamlit modifications */
    .stApp {
        background: linear-gradient(135deg, #0e1117 0%, #1a1d24 100%);
    }
    
    /* Metric cards */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, #262730 0%, #1a1d24 100%);
        border: 1px solid rgba(0, 212, 255, 0.2);
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    [data-testid="metric-container"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 212, 255, 0.2);
    }
    
    /* Headers */
    .custom-header {
        background: linear-gradient(135deg, #00d4ff 0%, #00ff88 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 48px;
        font-weight: 800;
        text-align: center;
        margin-bottom: 10px;
        font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .custom-subheader {
        color: #b0b3b8;
        text-align: center;
        font-size: 16px;
        margin-bottom: 30px;
        font-family: 'SF Pro Text', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Cards */
    .stat-card {
        background: rgba(38, 39, 48, 0.6);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(0, 212, 255, 0.1);
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div {
        background-color: #262730;
        border: 1px solid rgba(0, 212, 255, 0.3);
    }
    
    /* DataFrame styling */
    .dataframe {
        border: none !important;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1d24 0%, #0e1117 100%);
        border-right: 1px solid rgba(0, 212, 255, 0.1);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background-color: rgba(38, 39, 48, 0.5);
        border-radius: 10px;
        padding: 5px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        color: #b0b3b8;
        border-radius: 8px;
        font-weight: 500;
    }
    
    .stTabs [aria
