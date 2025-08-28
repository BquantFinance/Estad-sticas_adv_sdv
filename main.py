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
    page_title="Quantum Financial Analytics",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Advanced CSS for ultra-modern design
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    /* Global Variables */
    :root {
        --primary-bg: #0a0a0f;
        --secondary-bg: #12121a;
        --card-bg: #1a1a25;
        --glass-bg: rgba(26, 26, 37, 0.7);
        --accent-cyan: #00ffff;
        --accent-purple: #b794f6;
        --accent-pink: #f687b3;
        --accent-blue: #4299e1;
        --accent-green: #48bb78;
        --text-primary: #ffffff;
        --text-secondary: #a0aec0;
        --border-color: rgba(255, 255, 255, 0.1);
        --gradient-1: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --gradient-2: linear-gradient(135deg, #00ffff 0%, #b794f6 100%);
        --gradient-3: linear-gradient(135deg, #ff0844 0%, #ffb199 100%);
    }
    
    /* Main App Background */
    .stApp {
        background: 
            radial-gradient(circle at 20% 50%, rgba(120, 119, 198, 0.3) 0%, transparent 50%),
            radial-gradient(circle at 80% 80%, rgba(255, 119, 198, 0.3) 0%, transparent 50%),
            radial-gradient(circle at 40% 20%, rgba(0, 255, 255, 0.2) 0%, transparent 50%),
            linear-gradient(180deg, #0a0a0f 0%, #12121a 100%);
        background-attachment: fixed;
    }
    
    /* Animated Header */
    .main-header {
        background: linear-gradient(270deg, #00ffff, #b794f6, #f687b3, #00ffff);
        background-size: 400% 400%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradient 8s ease infinite;
        font-size: 56px;
        font-weight: 900;
        text-align: center;
        margin-bottom: 5px;
        font-family: 'Inter', sans-serif;
        letter-spacing: -2px;
        line-height: 1.1;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .sub-header {
        text-align: center;
        color: #a0aec0;
        font-size: 14px;
        font-weight: 500;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 40px;
    }
    
    /* Glassmorphism Cards */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.02) 100%);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 20px;
        box-shadow: 
            0 8px 32px 0 rgba(31, 38, 135, 0.37),
            inset 0 0 0 1px rgba(255, 255, 255, 0.1);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    [data-testid="metric-container"]::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--accent-cyan), transparent);
        animation: scan 3s linear infinite;
    }
    
    @keyframes scan {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    [data-testid="metric-container"]:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 
            0 12px 40px 0 rgba(31, 38, 135, 0.5),
            inset 0 0 20px rgba(255, 255, 255, 0.1);
        border-color: var(--accent-cyan);
    }
    
    /* Metric Labels */
    [data-testid="metric-container"] label {
        font-size: 12px;
        font-weight: 600;
        letter-spacing: 1px;
        text-transform: uppercase;
        color: var(--text-secondary);
    }
    
    [data-testid="metric-container"] > div > div {
        font-size: 32px;
        font-weight: 800;
        background: linear-gradient(135deg, #ffffff 0%, var(--accent-cyan) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(26, 26, 37, 0.95) 0%, rgba(18, 18, 26, 0.95) 100%);
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    section[data-testid="stSidebar"] .stSelectbox label,
    section[data-testid="stSidebar"] .stMultiselect label {
        color: var(--text-primary);
        font-weight: 600;
        font-size: 13px;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        margin-bottom: 8px;
    }
    
    /* Select Boxes */
    .stSelectbox > div > div,
    .stMultiselect > div > div {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 12px;
        color: white;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stSelectbox > div > div:hover,
    .stMultiselect > div > div:hover {
        border-color: var(--accent-cyan);
        box-shadow: 0 0 20px rgba(0, 255, 255, 0.3);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 16px;
        padding: 8px;
        gap: 8px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: var(--text-secondary);
        border-radius: 12px;
        padding: 12px 24px;
        font-weight: 600;
        font-size: 14px;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
        border: 1px solid transparent;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(255, 255, 255, 0.05);
        color: var(--text-primary);
        border-color: rgba(255, 255, 255, 0.1);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(0, 255, 255, 0.2) 0%, rgba(183, 148, 246, 0.2) 100%);
        color: var(--text-primary);
        border: 1px solid rgba(0, 255, 255, 0.5);
        box-shadow: 0 0 20px rgba(0, 255, 255, 0.2);
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--accent-cyan) 0%, var(--accent-purple) 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 24px;
        font-weight: 600;
        font-size: 14px;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 255, 255, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 255, 255, 0.5);
    }
    
    /* Download Buttons */
    .stDownloadButton > button {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: var(--accent-cyan);
        transition: all 0.3s ease;
    }
    
    .stDownloadButton > button:hover {
        background: rgba(0, 255, 255, 0.1);
        border-color: var(--accent-cyan);
        box-shadow: 0 0 20px rgba(0, 255, 255, 0.3);
    }
    
    /* DataFrames */
    .dataframe {
        border: none !important;
        background: rgba(255, 255, 255, 0.02);
        border-radius: 12px;
        overflow: hidden;
    }
    
    /* Dividers */
    .stDivider {
        border-color: rgba(255, 255, 255, 0.1);
    }
    
    /* Info boxes */
    .stAlert {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        backdrop-filter: blur(10px);
    }
    
    /* Spinner */
    .stSpinner {
        color: var(--accent-cyan) !important;
    }
    
    /* File Uploader */
    .stFileUploadDropzone {
        background: rgba(255, 255, 255, 0.03);
        border: 2px dashed rgba(0, 255, 255, 0.3);
        border-radius: 12px;
        transition: all 0.3s ease;
    }
    
    .stFileUploadDropzone:hover {
        background: rgba(0, 255, 255, 0.05);
        border-color: var(--accent-cyan);
        box-shadow: 0 0 20px rgba(0, 255, 255, 0.2);
    }
    
    /* Custom card class */
    .custom-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.02) 100%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 24px;
        margin: 16px 0;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.2);
    }
    
    /* Glowing text effect */
    .glow-text {
        text-shadow: 0 0 20px rgba(0, 255, 255, 0.5);
    }
    </style>
    """, unsafe_allow_html=True)

# Load data function
@st.cache_data
def load_data(sociedades_file, agencias_file):
    sociedades = pd.read_excel(sociedades_file)
    agencias = pd.read_excel(agencias_file)
    
    # Add tipo column
    sociedades['tipo'] = 'Sociedad'
    agencias['tipo'] = 'Agencia'
    
    # Combine datasets
    combined = pd.concat([sociedades, agencias], ignore_index=True)
    
    # Convert fecha to datetime
    for df in [sociedades, agencias, combined]:
        df['fecha'] = pd.to_datetime(df['fecha'])
    
    return sociedades, agencias, combined

# Calculate quarterly metrics
def calculate_quarterly_metrics(df, entity):
    entity_data = df[df['entidad'] == entity].sort_values('fecha')
    
    if len(entity_data) < 2:
        return None
    
    metrics = []
    for i in range(len(entity_data)):
        row = entity_data.iloc[i]
        metrics_dict = {
            'periodo': row['periodo'],
            'fecha': row['fecha'],
            'fondos_propios': row['fondos_propios'],
            'activos_totales': row['activos_totales'],
            'comisiones_percibidas': row['comisiones_percibidas'],
            'comisiones_netas': row['comisiones_netas'],
            'margen_bruto': row['margen_bruto'],
            'gastos_explotacion': row['gastos_explotacion'],
            'resultados_antes_impuestos': row['resultados_antes_impuestos'],
            'ROA': (row['resultados_antes_impuestos'] / row['activos_totales'] * 100) if row['activos_totales'] > 0 else 0,
            'ROE': (row['resultados_antes_impuestos'] / row['fondos_propios'] * 100) if row['fondos_propios'] > 0 else 0,
            'efficiency_ratio': (row['gastos_explotacion'] / row['margen_bruto'] * 100) if row['margen_bruto'] > 0 else 0,
            'net_margin': (row['resultados_antes_impuestos'] / row['comisiones_percibidas'] * 100) if row['comisiones_percibidas'] > 0 else 0,
            'leverage': (row['activos_totales'] / row['fondos_propios']) if row['fondos_propios'] > 0 else 0
        }
        
        # Calculate quarter-over-quarter changes
        if i > 0:
            prev_row = entity_data.iloc[i-1]
            metrics_dict['qoq_assets'] = ((row['activos_totales'] - prev_row['activos_totales']) / prev_row['activos_totales'] * 100) if prev_row['activos_totales'] > 0 else 0
            metrics_dict['qoq_revenue'] = ((row['comisiones_percibidas'] - prev_row['comisiones_percibidas']) / prev_row['comisiones_percibidas'] * 100) if prev_row['comisiones_percibidas'] > 0 else 0
            metrics_dict['qoq_profit'] = ((row['resultados_antes_impuestos'] - prev_row['resultados_antes_impuestos']) / abs(prev_row['resultados_antes_impuestos']) * 100) if prev_row['resultados_antes_impuestos'] != 0 else 0
        else:
            metrics_dict['qoq_assets'] = 0
            metrics_dict['qoq_revenue'] = 0
            metrics_dict['qoq_profit'] = 0
        
        metrics.append(metrics_dict)
    
    return pd.DataFrame(metrics)

# Ultra-modern plotly theme
ultra_modern_theme = {
    'layout': {
        'paper_bgcolor': 'rgba(10, 10, 15, 0)',
        'plot_bgcolor': 'rgba(18, 18, 26, 0.5)',
        'font': {'color': '#ffffff', 'family': 'Inter, sans-serif'},
        'xaxis': {
            'gridcolor': 'rgba(255, 255, 255, 0.05)',
            'linecolor': 'rgba(255, 255, 255, 0.1)',
            'tickfont': {'color': '#a0aec0'},
            'title': {'font': {'color': '#ffffff'}}
        },
        'yaxis': {
            'gridcolor': 'rgba(255, 255, 255, 0.05)',
            'linecolor': 'rgba(255, 255, 255, 0.1)',
            'tickfont': {'color': '#a0aec0'},
            'title': {'font': {'color': '#ffffff'}}
        },
        'colorway': ['#00ffff', '#b794f6', '#f687b3', '#4299e1', '#48bb78', '#ed8936', '#9f7aea'],
        'hovermode': 'x unified',
        'hoverlabel': {
            'bgcolor': 'rgba(26, 26, 37, 0.95)',
            'bordercolor': '#00ffff',
            'font': {'color': '#ffffff'}
        }
    }
}

# Main app
def main():
    # Header with animation
    st.markdown('<h1 class="main-header">Quantum Financial Analytics</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Advanced Quarter-by-Quarter Company Analysis</p>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #4a5568; font-size: 12px; margin-bottom: 30px;">by @Gsnchez | bquantfinance.com</p>', unsafe_allow_html=True)
    
    # File uploaders with custom styling
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.markdown("### 💎 Data Import Portal")
    col1, col2 = st.columns(2)
    
    with col1:
        sociedades_file = st.file_uploader(
            "Upload Sociedades Dataset",
            type=['xlsx', 'xls'],
            key="sociedades",
            help="Upload sociedades_estructurado.xlsx"
        )
    
    with col2:
        agencias_file = st.file_uploader(
            "Upload Agencias Dataset", 
            type=['xlsx', 'xls'],
            key="agencias",
            help="Upload agencias_estructurado.xlsx"
        )
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Check if both files are uploaded
    if not sociedades_file or not agencias_file:
        st.info("⚡ Upload both datasets to unlock the analytics dashboard")
        
        # Display sample dashboard preview
        st.markdown("""
        <div class="custom-card" style="margin-top: 40px;">
            <h3 style="color: #00ffff; margin-bottom: 20px;">🚀 Features Preview</h3>
            <ul style="color: #a0aec0; line-height: 2;">
                <li>📊 <strong>Quarter-by-Quarter Analysis:</strong> Track individual company performance across periods</li>
                <li>📈 <strong>Growth Metrics:</strong> QoQ revenue, assets, and profitability changes</li>
                <li>🎯 <strong>Efficiency Indicators:</strong> ROA, ROE, leverage, and operational efficiency</li>
                <li>🔍 <strong>Peer Comparison:</strong> Benchmark against sector averages</li>
                <li>📉 <strong>Trend Analysis:</strong> Identify seasonal patterns and growth trajectories</li>
                <li>⚡ <strong>Financial Health Score:</strong> Composite rating based on multiple metrics</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Load data
    with st.spinner('🔄 Processing financial data...'):
        try:
            sociedades, agencias, combined = load_data(sociedades_file, agencias_file)
            st.success("✨ Data loaded successfully!")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.stop()
    
    # Sidebar configuration
    with st.sidebar:
        st.markdown("## ⚙️ Analysis Configuration")
        
        # Company selector with search
        st.markdown("### 🏢 Company Selection")
        all_entities = sorted(combined['entidad'].unique())
        
        # Primary company selection
        selected_company = st.selectbox(
            "Primary Company",
            all_entities,
            help="Select the main company for detailed analysis",
            index=0
        )
        
        # Comparison companies
        comparison_companies = st.multiselect(
            "Comparison Companies",
            [e for e in all_entities if e != selected_company],
            default=[e for e in all_entities if e != selected_company][:3],
            help="Select companies for benchmarking"
        )
        
        st.divider()
        
        # Time period filter
        st.markdown("### 📅 Time Period")
        available_periods = sorted(combined['periodo'].unique())
        selected_periods = st.multiselect(
            "Select Quarters",
            available_periods,
            default=available_periods,
            help="Choose quarters to include in analysis"
        )
        
        st.divider()
        
        # Analysis options
        st.markdown("### 🎯 Analysis Focus")
        analysis_focus = st.radio(
            "Select Focus Area",
            ["📊 Overall Performance", "💰 Revenue Analysis", "📈 Growth Metrics", "⚡ Efficiency Analysis", "🏆 Peer Comparison"],
            index=0
        )
        
        # Metric preferences
        st.markdown("### 📉 Metric Preferences")
        primary_metric = st.selectbox(
            "Primary KPI",
            ['comisiones_percibidas', 'resultados_antes_impuestos', 'activos_totales', 'fondos_propios'],
            format_func=lambda x: x.replace('_', ' ').title(),
            index=0
        )
        
        show_trends = st.checkbox("Show Trend Lines", value=True)
        show_forecasts = st.checkbox("Show Projections", value=False)
    
    # Filter data
    company_data = combined[(combined['entidad'] == selected_company) & 
                           (combined['periodo'].isin(selected_periods))].sort_values('fecha')
    
    comparison_data = combined[(combined['entidad'].isin(comparison_companies)) & 
                               (combined['periodo'].isin(selected_periods))]
    
    # Main content area
    if not company_data.empty:
        # Company name and type badge
        company_type = company_data.iloc[0]['tipo']
        type_color = "#00ffff" if company_type == "Agencia" else "#b794f6"
        
        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 30px;">
            <h2 style="color: white; font-size: 32px; font-weight: 800; margin-bottom: 10px;">{selected_company}</h2>
            <span style="background: linear-gradient(135deg, {type_color} 0%, {type_color}88 100%); 
                         color: white; padding: 6px 16px; border-radius: 20px; font-size: 12px; 
                         font-weight: 600; letter-spacing: 1px;">{company_type.upper()}</span>
        </div>
        """, unsafe_allow_html=True)
        
        # Calculate quarterly metrics
        quarterly_metrics = calculate_quarterly_metrics(combined, selected_company)
        
        if quarterly_metrics is not None and not quarterly_metrics.empty:
            # Latest quarter KPIs
            latest = quarterly_metrics.iloc[-1]
            prev = quarterly_metrics.iloc[-2] if len(quarterly_metrics) > 1 else latest
            
            # KPI Cards
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    label="💰 Revenue (Commissions)",
                    value=f"€{latest['comisiones_percibidas']:,.0f}K",
                    delta=f"{latest['qoq_revenue']:.1f}% QoQ",
                    delta_color="normal"
                )
            
            with col2:
                st.metric(
                    label="📊 Profit Before Tax",
                    value=f"€{latest['resultados_antes_impuestos']:,.0f}K",
                    delta=f"{latest['qoq_profit']:.1f}% QoQ",
                    delta_color="normal"
                )
            
            with col3:
                st.metric(
                    label="⚡ ROE",
                    value=f"{latest['ROE']:.1f}%",
                    delta=f"{latest['ROE'] - prev['ROE']:.1f}pp",
                    delta_color="normal"
                )
            
            with col4:
                st.metric(
                    label="🎯 Efficiency Ratio",
                    value=f"{latest['efficiency_ratio']:.1f}%",
                    delta=f"{latest['efficiency_ratio'] - prev['efficiency_ratio']:.1f}pp",
                    delta_color="inverse"
                )
            
            # Tabs for different views
            tab1, tab2, tab3, tab4, tab5 = st.tabs([
                "📊 Quarterly Performance", 
                "📈 Growth Analysis", 
                "⚡ Efficiency Metrics",
                "🏆 Peer Comparison",
                "📉 Financial Health"
            ])
            
            with tab1:
                st.markdown("### 📊 Quarter-by-Quarter Performance Breakdown")
                
                # Create comprehensive performance chart
                fig = make_subplots(
                    rows=2, cols=2,
                    subplot_titles=("Revenue & Profit Evolution", "Assets & Equity Growth", 
                                   "Quarter-over-Quarter Growth Rates", "Margin Analysis"),
                    vertical_spacing=0.12,
                    horizontal_spacing=0.10,
                    specs=[[{'secondary_y': True}, {'secondary_y': True}],
                           [{'secondary_y': False}, {'secondary_y': False}]]
                )
                
                # Revenue & Profit
                fig.add_trace(
                    go.Bar(x=quarterly_metrics['periodo'], y=quarterly_metrics['comisiones_percibidas'],
                          name='Revenue', marker_color='#00ffff', opacity=0.7,
                          text=quarterly_metrics['comisiones_percibidas'].round(0),
                          textposition='outside', textfont=dict(size=10)),
                    row=1, col=1, secondary_y=False
                )
                fig.add_trace(
                    go.Scatter(x=quarterly_metrics['periodo'], y=quarterly_metrics['resultados_antes_impuestos'],
                              name='Profit', line=dict(color='#f687b3', width=3),
                              mode='lines+markers', marker=dict(size=10)),
                    row=1, col=1, secondary_y=True
                )
                
                # Assets & Equity
                fig.add_trace(
                    go.Bar(x=quarterly_metrics['periodo'], y=quarterly_metrics['activos_totales'],
                          name='Assets', marker_color='#4299e1', opacity=0.7),
                    row=1, col=2, secondary_y=False
                )
                fig.add_trace(
                    go.Scatter(x=quarterly_metrics['periodo'], y=quarterly_metrics['fondos_propios'],
                              name='Equity', line=dict(color='#48bb78', width=3),
                              mode='lines+markers', marker=dict(size=10)),
                    row=1, col=2, secondary_y=True
                )
                
                # QoQ Growth Rates
                fig.add_trace(
                    go.Scatter(x=quarterly_metrics['periodo'][1:], y=quarterly_metrics['qoq_revenue'][1:],
                              name='Revenue Growth', line=dict(color='#00ffff', width=2),
                              mode='lines+markers', marker=dict(size=8)),
                    row=2, col=1
                )
                fig.add_trace(
                    go.Scatter(x=quarterly_metrics['periodo'][1:], y=quarterly_metrics['qoq_assets'][1:],
                              name='Assets Growth', line=dict(color='#b794f6', width=2),
                              mode='lines+markers', marker=dict(size=8)),
                    row=2, col=1
                )
                
                # Margins
                fig.add_trace(
                    go.Scatter(x=quarterly_metrics['periodo'], y=quarterly_metrics['net_margin'],
                              name='Net Margin', line=dict(color='#ed8936', width=2),
                              mode='lines+markers', fill='tozeroy', opacity=0.3),
                    row=2, col=2
                )
                
                # Update layout
                fig.update_layout(
                    **ultra_modern_theme['layout'],
                    height=700,
                    showlegend=True,
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=-0.15,
                        xanchor="center",
                        x=0.5,
                        bgcolor='rgba(26, 26, 37, 0.8)',
                        bordercolor='rgba(255, 255, 255, 0.1)',
                        borderwidth=1
                    )
                )
                
                # Update axes
                fig.update_yaxes(title_text="Amount (€K)", row=1, col=1, secondary_y=False)
                fig.update_yaxes(title_text="Profit (€K)", row=1, col=1, secondary_y=True)
                fig.update_yaxes(title_text="Amount (€K)", row=1, col=2, secondary_y=False)
                fig.update_yaxes(title_text="Equity (€K)", row=1, col=2, secondary_y=True)
                fig.update_yaxes(title_text="Growth Rate (%)", row=2, col=1)
                fig.update_yaxes(title_text="Margin (%)", row=2, col=2)
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Performance Summary Table
                st.markdown("### 📋 Quarterly Performance Summary")
                summary_df = quarterly_metrics[['periodo', 'comisiones_percibidas', 'resultados_antes_impuestos', 
                                               'ROA', 'ROE', 'efficiency_ratio']].round(2)
                summary_df.columns = ['Quarter', 'Revenue (€K)', 'PBT (€K)', 'ROA (%)', 'ROE (%)', 'Efficiency (%)']
                st.dataframe(
                    summary_df.style.background_gradient(cmap='RdYlGn', subset=['ROA (%)', 'ROE (%)'])
                                   .background_gradient(cmap='RdYlGn_r', subset=['Efficiency (%)']),
                    use_container_width=True
                )
            
            with tab2:
                st.markdown("### 📈 Growth Trajectory Analysis")
                
                # Growth metrics visualization
                fig_growth = make_subplots(
                    rows=2, cols=2,
                    subplot_titles=("Cumulative Revenue Growth", "Indexed Performance (Base 100)",
                                   "Moving Averages", "Growth Momentum"),
                    vertical_spacing=0.12,
                    horizontal_spacing=0.10
                )
                
                # Cumulative growth
                quarterly_metrics['cum_revenue'] = quarterly_metrics['comisiones_percibidas'].cumsum()
                quarterly_metrics['cum_profit'] = quarterly_metrics['resultados_antes_impuestos'].cumsum()
                
                fig_growth.add_trace(
                    go.Scatter(x=quarterly_metrics['periodo'], y=quarterly_metrics['cum_revenue'],
                              name='Cumulative Revenue', line=dict(color='#00ffff', width=3),
                              mode='lines+markers', fill='tonexty', marker=dict(size=10)),
                    row=1, col=1
                )
                
                fig_growth.add_trace(
                    go.Scatter(x=quarterly_metrics['periodo'], y=quarterly_metrics['cum_profit'],
                              name='Cumulative Profit', line=dict(color='#f687b3', width=3),
                              mode='lines+markers', fill='tozeroy', marker=dict(size=10)),
                    row=1, col=1
                )
                
                # Indexed performance
                base_revenue = quarterly_metrics['comisiones_percibidas'].iloc[0]
                base_assets = quarterly_metrics['activos_totales'].iloc[0]
                
                quarterly_metrics['indexed_revenue'] = (quarterly_metrics['comisiones_percibidas'] / base_revenue * 100)
                quarterly_metrics['indexed_assets'] = (quarterly_metrics['activos_totales'] / base_assets * 100)
                
                fig_growth.add_trace(
                    go.Scatter(x=quarterly_metrics['periodo'], y=quarterly_metrics['indexed_revenue'],
                              name='Revenue Index', line=dict(color='#00ffff', width=2, dash='solid'),
                              mode='lines+markers'),
                    row=1, col=2
                )
                
                fig_growth.add_trace(
                    go.Scatter(x=quarterly_metrics['periodo'], y=quarterly_metrics['indexed_assets'],
                              name='Assets Index', line=dict(color='#4299e1', width=2, dash='dash'),
                              mode='lines+markers'),
                    row=1, col=2
                )
                
                # Add 100 baseline
                fig_growth.add_hline(y=100, line_width=1, line_dash="dot", line_color="gray", row=1, col=2)
                
                # Moving averages (if enough data)
                if len(quarterly_metrics) >= 3:
                    quarterly_metrics['ma_revenue'] = quarterly_metrics['comisiones_percibidas'].rolling(window=3, center=True).mean()
                    
                    fig_growth.add_trace(
                        go.Scatter(x=quarterly_metrics['periodo'], y=quarterly_metrics['comisiones_percibidas'],
                                  name='Actual Revenue', line=dict(color='#00ffff', width=2),
                                  mode='lines+markers', opacity=0.5),
                        row=2, col=1
                    )
                    
                    fig_growth.add_trace(
                        go.Scatter(x=quarterly_metrics['periodo'], y=quarterly_metrics['ma_revenue'],
                                  name='3Q Moving Avg', line=dict(color='#b794f6', width=3),
                                  mode='lines'),
                        row=2, col=1
                    )
                
                # Growth momentum
                if len(quarterly_metrics) > 2:
                    quarterly_metrics['growth_acceleration'] = quarterly_metrics['qoq_revenue'].diff()
                    
                    colors = ['#48bb78' if x > 0 else '#ff3366' for x in quarterly_metrics['growth_acceleration'][2:]]
                    
                    fig_growth.add_trace(
                        go.Bar(x=quarterly_metrics['periodo'][2:], y=quarterly_metrics['growth_acceleration'][2:],
                              name='Growth Acceleration', marker_color=colors, opacity=0.7),
                        row=2, col=2
                    )
                
                fig_growth.update_layout(**ultra_modern_theme['layout'], height=700, showlegend=True)
                st.plotly_chart(fig_growth, use_container_width=True)
                
                # Growth Statistics
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    avg_growth = quarterly_metrics['qoq_revenue'][1:].mean()
                    st.markdown(f"""
                    <div class="custom-card">
                        <h4 style="color: #00ffff;">Average QoQ Growth</h4>
                        <p style="font-size: 32px; font-weight: 800; color: white;">{avg_growth:.1f}%</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    volatility = quarterly_metrics['qoq_revenue'][1:].std()
                    st.markdown(f"""
                    <div class="custom-card">
                        <h4 style="color: #b794f6;">Growth Volatility</h4>
                        <p style="font-size: 32px; font-weight: 800; color: white;">{volatility:.1f}%</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    total_growth = ((quarterly_metrics['comisiones_percibidas'].iloc[-1] / 
                                   quarterly_metrics['comisiones_percibidas'].iloc[0] - 1) * 100)
                    st.markdown(f"""
                    <div class="custom-card">
                        <h4 style="color: #f687b3;">Total Period Growth</h4>
                        <p style="font-size: 32px; font-weight: 800; color: white;">{total_growth:.1f}%</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            with tab3:
                st.markdown("### ⚡ Operational Efficiency Deep Dive")
                
                # Efficiency metrics
                fig_eff = make_subplots(
                    rows=2, cols=2,
                    subplot_titles=("ROA vs ROE Evolution", "Cost-Income Ratio", 
                                   "Leverage Analysis", "Operational Efficiency Score"),
                    vertical_spacing=0.12,
                    horizontal_spacing=0.10
                )
                
                # ROA vs ROE
                fig_eff.add_trace(
                    go.Scatter(x=quarterly_metrics['periodo'], y=quarterly_metrics['ROA'],
                              name='ROA', line=dict(color='#00ffff', width=3),
                              mode='lines+markers', marker=dict(size=10)),
                    row=1, col=1
                )
                fig_eff.add_trace(
                    go.Scatter(x=quarterly_metrics['periodo'], y=quarterly_metrics['ROE'],
                              name='ROE', line=dict(color='#f687b3', width=3),
                              mode='lines+markers', marker=dict(size=10)),
                    row=1, col=1
                )
                
                # Cost-Income Ratio
                fig_eff.add_trace(
                    go.Bar(x=quarterly_metrics['periodo'], y=quarterly_metrics['efficiency_ratio'],
                          name='Cost/Income', marker_color='#ed8936', opacity=0.7,
                          text=quarterly_metrics['efficiency_ratio'].round(1),
                          textposition='outside'),
                    row=1, col=2
                )
                
                # Leverage
                fig_eff.add_trace(
                    go.Scatter(x=quarterly_metrics['periodo'], y=quarterly_metrics['leverage'],
                              name='Leverage', line=dict(color='#9f7aea', width=3),
                              mode='lines+markers', fill='tozeroy', opacity=0.3),
                    row=2, col=1
                )
                
                # Efficiency Score (composite)
                # Normalize metrics for scoring
                quarterly_metrics['eff_score'] = (
                    (100 - quarterly_metrics['efficiency_ratio']) * 0.4 +  # Lower is better
                    quarterly_metrics['ROE'] * 0.3 +
                    quarterly_metrics['ROA'] * 0.3
                )
                
                fig_eff.add_trace(
                    go.Scatter(x=quarterly_metrics['periodo'], y=quarterly_metrics['eff_score'],
                              name='Efficiency Score', line=dict(color='#48bb78', width=3),
                              mode='lines+markers', marker=dict(size=12),
                              fill='tozeroy', opacity=0.3),
                    row=2, col=2
                )
                
                fig_eff.update_layout(**ultra_modern_theme['layout'], height=700, showlegend=True)
                st.plotly_chart(fig_eff, use_container_width=True)
                
                # Efficiency Benchmarks
                st.markdown("### 🎯 Efficiency Benchmarks")
                
                # Calculate percentiles for benchmarking
                all_companies_metrics = []
                for entity in all_entities:
                    entity_metrics = calculate_quarterly_metrics(combined, entity)
                    if entity_metrics is not None and not entity_metrics.empty:
                        all_companies_metrics.append(entity_metrics)
                
                if all_companies_metrics:
                    all_metrics_df = pd.concat(all_companies_metrics)
                    
                    # Calculate percentiles
                    percentiles = all_metrics_df[['ROA', 'ROE', 'efficiency_ratio']].describe(percentiles=[.25, .5, .75])
                    
                    # Compare with percentiles
                    latest_metrics = quarterly_metrics.iloc[-1]
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        roa_percentile = (all_metrics_df['ROA'] < latest_metrics['ROA']).mean() * 100
                        color = "#48bb78" if roa_percentile > 50 else "#ff3366"
                        st.markdown(f"""
                        <div class="custom-card">
                            <h4 style="color: {color};">ROA Percentile</h4>
                            <p style="font-size: 32px; font-weight: 800; color: white;">{roa_percentile:.0f}th</p>
                            <p style="color: #a0aec0; font-size: 12px;">Better than {roa_percentile:.0f}% of peers</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        roe_percentile = (all_metrics_df['ROE'] < latest_metrics['ROE']).mean() * 100
                        color = "#48bb78" if roe_percentile > 50 else "#ff3366"
                        st.markdown(f"""
                        <div class="custom-card">
                            <h4 style="color: {color};">ROE Percentile</h4>
                            <p style="font-size: 32px; font-weight: 800; color: white;">{roe_percentile:.0f}th</p>
                            <p style="color: #a0aec0; font-size: 12px;">Better than {roe_percentile:.0f}% of peers</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col3:
                        eff_percentile = (all_metrics_df['efficiency_ratio'] > latest_metrics['efficiency_ratio']).mean() * 100
                        color = "#48bb78" if eff_percentile > 50 else "#ff3366"
                        st.markdown(f"""
                        <div class="custom-card">
                            <h4 style="color: {color};">Efficiency Percentile</h4>
                            <p style="font-size: 32px; font-weight: 800; color: white;">{eff_percentile:.0f}th</p>
                            <p style="color: #a0aec0; font-size: 12px;">More efficient than {eff_percentile:.0f}% of peers</p>
                        </div>
                        """, unsafe_allow_html=True)
            
            with tab4:
                st.markdown("### 🏆 Peer Comparison Analysis")
                
                if not comparison_data.empty:
                    # Prepare comparison data
                    peer_metrics = []
                    for comp in comparison_companies:
                        comp_metrics = calculate_quarterly_metrics(combined, comp)
                        if comp_metrics is not None and not comp_metrics.empty:
                            latest_comp = comp_metrics.iloc[-1]
                            peer_metrics.append({
                                'Company': comp,
                                'Revenue': latest_comp['comisiones_percibidas'],
                                'Profit': latest_comp['resultados_antes_impuestos'],
                                'ROA': latest_comp['ROA'],
                                'ROE': latest_comp['ROE'],
                                'Efficiency': latest_comp['efficiency_ratio']
                            })
                    
                    # Add selected company
                    peer_metrics.append({
                        'Company': selected_company,
                        'Revenue': latest['comisiones_percibidas'],
                        'Profit': latest['resultados_antes_impuestos'],
                        'ROA': latest['ROA'],
                        'ROE': latest['ROE'],
                        'Efficiency': latest['efficiency_ratio']
                    })
                    
                    peer_df = pd.DataFrame(peer_metrics)
                    
                    # Radar chart for comparison
                    categories_radar = ['Revenue', 'Profit', 'ROA', 'ROE', '100-Efficiency']
                    
                    fig_radar = go.Figure()
                    
                    # Normalize data for radar chart
                    peer_df_norm = peer_df.copy()
                    for col in ['Revenue', 'Profit', 'ROA', 'ROE']:
                        max_val = peer_df[col].max()
                        if max_val > 0:
                            peer_df_norm[col] = peer_df[col] / max_val * 100
                    peer_df_norm['100-Efficiency'] = 100 - peer_df['Efficiency']
                    
                    # Add traces for each company
                    colors = ['#00ffff', '#b794f6', '#f687b3', '#4299e1', '#48bb78']
                    for idx, row in peer_df_norm.iterrows():
                        if row['Company'] == selected_company:
                            line_width = 4
                            opacity = 1
                            fill = 'toself'
                        else:
                            line_width = 2
                            opacity = 0.6
                            fill = None
                        
                        fig_radar.add_trace(go.Scatterpolar(
                            r=[row['Revenue'], row['Profit'], row['ROA'], row['ROE'], row['100-Efficiency']],
                            theta=categories_radar,
                            fill=fill,
                            name=row['Company'][:20],
                            line=dict(color=colors[idx % len(colors)], width=line_width),
                            opacity=opacity
                        ))
                    
                    fig_radar.update_layout(
                        polar=dict(
                            radialaxis=dict(
                                visible=True,
                                range=[0, 100],
                                gridcolor='rgba(255, 255, 255, 0.1)',
                                tickfont=dict(color='#a0aec0')
                            ),
                            angularaxis=dict(gridcolor='rgba(255, 255, 255, 0.1)')
                        ),
                        **ultra_modern_theme['layout'],
                        height=500,
                        title="Multi-Dimensional Peer Comparison (Normalized)"
                    )
                    
                    st.plotly_chart(fig_radar, use_container_width=True)
                    
                    # Ranking table
                    st.markdown("### 📊 Peer Ranking Table")
                    
                    peer_df_display = peer_df.round(2)
                    peer_df_display = peer_df_display.sort_values('ROE', ascending=False)
                    
                    # Highlight selected company
                    def highlight_selected(row):
                        if row['Company'] == selected_company:
                            return ['background-color: rgba(0, 255, 255, 0.2)'] * len(row)
                        return [''] * len(row)
                    
                    st.dataframe(
                        peer_df_display.style.apply(highlight_selected, axis=1)
                                            .background_gradient(cmap='RdYlGn', subset=['ROA', 'ROE'])
                                            .background_gradient(cmap='RdYlGn_r', subset=['Efficiency']),
                        use_container_width=True
                    )
            
            with tab5:
                st.markdown("### 📉 Financial Health Assessment")
                
                # Calculate health score components
                health_metrics = {
                    'Profitability': (latest['ROE'] / 20 * 100),  # Normalize to 100
                    'Asset Quality': (latest['ROA'] / 10 * 100),
                    'Operational Efficiency': (100 - latest['efficiency_ratio']),
                    'Growth Momentum': min(100, max(0, latest['qoq_revenue'] + 50)),
                    'Leverage Health': min(100, 100 / latest['leverage']) if latest['leverage'] > 0 else 100
                }
                
                # Overall health score
                overall_health = sum(health_metrics.values()) / len(health_metrics)
                
                # Health gauge chart
                fig_health = go.Figure(go.Indicator(
                    mode = "gauge+number+delta",
                    value = overall_health,
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "Overall Financial Health Score", 'font': {'size': 24, 'color': 'white'}},
                    delta = {'reference': 70, 'increasing': {'color': "#48bb78"}},
                    gauge = {
                        'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "white"},
                        'bar': {'color': "#00ffff"},
                        'bgcolor': "rgba(255, 255, 255, 0.1)",
                        'borderwidth': 2,
                        'bordercolor': "rgba(255, 255, 255, 0.2)",
                        'steps': [
                            {'range': [0, 25], 'color': '#ff3366'},
                            {'range': [25, 50], 'color': '#ed8936'},
                            {'range': [50, 75], 'color': '#ecc94b'},
                            {'range': [75, 100], 'color': '#48bb78'}
                        ],
                        'threshold': {
                            'line': {'color': "white", 'width': 4},
                            'thickness': 0.75,
                            'value': overall_health
                        }
                    }
                ))
                
                fig_health.update_layout(**ultra_modern_theme['layout'], height=400)
                st.plotly_chart(fig_health, use_container_width=True)
                
                # Health components breakdown
                st.markdown("### 🎯 Health Score Components")
                
                cols = st.columns(5)
                for idx, (component, score) in enumerate(health_metrics.items()):
                    with cols[idx]:
                        color = "#48bb78" if score >= 70 else "#ed8936" if score >= 40 else "#ff3366"
                        st.markdown(f"""
                        <div class="custom-card" style="text-align: center;">
                            <h5 style="color: {color}; font-size: 14px; margin-bottom: 10px;">{component}</h5>
                            <p style="font-size: 28px; font-weight: 800; color: white; margin: 0;">{score:.0f}</p>
                            <div style="background: rgba(255, 255, 255, 0.1); border-radius: 10px; height: 8px; margin-top: 10px;">
                                <div style="background: {color}; border-radius: 10px; height: 8px; width: {score}%;"></div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                
                # Trend Analysis
                st.markdown("### 📈 Health Trend Analysis")
                
                # Calculate health score for all quarters
                quarterly_health = []
                for i in range(len(quarterly_metrics)):
                    q_data = quarterly_metrics.iloc[i]
                    q_health = {
                        'Quarter': q_data['periodo'],
                        'Health Score': (
                            (q_data['ROE'] / 20 * 100 * 0.2) +
                            (q_data['ROA'] / 10 * 100 * 0.2) +
                            ((100 - q_data['efficiency_ratio']) * 0.2) +
                            (min(100, max(0, q_data['qoq_revenue'] + 50)) * 0.2) +
                            (min(100, 100 / q_data['leverage']) * 0.2) if q_data['leverage'] > 0 else 20
                        )
                    }
                    quarterly_health.append(q_health)
                
                health_df = pd.DataFrame(quarterly_health)
                
                fig_trend = go.Figure()
                fig_trend.add_trace(go.Scatter(
                    x=health_df['Quarter'],
                    y=health_df['Health Score'],
                    mode='lines+markers',
                    line=dict(color='#00ffff', width=3),
                    marker=dict(size=12, color='#00ffff', line=dict(color='white', width=2)),
                    fill='tonexty',
                    name='Health Score'
                ))
                
                # Add threshold lines
                fig_trend.add_hline(y=70, line_width=1, line_dash="dash", line_color="#48bb78", 
                                   annotation_text="Good Health", annotation_position="right")
                fig_trend.add_hline(y=40, line_width=1, line_dash="dash", line_color="#ed8936",
                                   annotation_text="Moderate Health", annotation_position="right")
                
                fig_trend.update_layout(
                    **ultra_modern_theme['layout'],
                    height=400,
                    title="Financial Health Evolution",
                    yaxis_title="Health Score",
                    xaxis_title="Quarter"
                )
                
                st.plotly_chart(fig_trend, use_container_width=True)
        
        # Export Options
        st.divider()
        st.markdown("### 💾 Export Options")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Export quarterly metrics
            csv = quarterly_metrics.to_csv(index=False)
            st.download_button(
                label="📊 Download Quarterly Metrics",
                data=csv,
                file_name=f"{selected_company.replace(' ', '_')}_quarterly_metrics_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col2:
            # Generate executive summary
            summary = f"""
EXECUTIVE SUMMARY - {selected_company}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
Analysis by: @Gsnchez | bquantfinance.com

COMPANY OVERVIEW
================
Entity: {selected_company}
Type: {company_type}
Periods Analyzed: {len(quarterly_metrics)} quarters

LATEST QUARTER PERFORMANCE ({latest['periodo']})
===========================================
Revenue: €{latest['comisiones_percibidas']:,.0f}K (QoQ: {latest['qoq_revenue']:.1f}%)
Profit Before Tax: €{latest['resultados_antes_impuestos']:,.0f}K (QoQ: {latest['qoq_profit']:.1f}%)
Total Assets: €{latest['activos_totales']:,.0f}K
Shareholders' Equity: €{latest['fondos_propios']:,.0f}K

KEY PERFORMANCE INDICATORS
==========================
ROA: {latest['ROA']:.2f}%
ROE: {latest['ROE']:.2f}%
Efficiency Ratio: {latest['efficiency_ratio']:.2f}%
Net Margin: {latest['net_margin']:.2f}%
Leverage: {latest['leverage']:.2f}x

FINANCIAL HEALTH ASSESSMENT
===========================
Overall Health Score: {overall_health:.1f}/100
Rating: {'Excellent' if overall_health >= 75 else 'Good' if overall_health >= 50 else 'Moderate' if overall_health >= 25 else 'Needs Improvement'}

GROWTH METRICS
==============
Average QoQ Revenue Growth: {quarterly_metrics['qoq_revenue'][1:].mean():.1f}%
Revenue Volatility: {quarterly_metrics['qoq_revenue'][1:].std():.1f}%
Total Period Growth: {((latest['comisiones_percibidas'] / quarterly_metrics.iloc[0]['comisiones_percibidas'] - 1) * 100):.1f}%
            """
            
            st.download_button(
                label="📄 Download Executive Summary",
                data=summary,
                file_name=f"{selected_company.replace(' ', '_')}_executive_summary_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain",
                use_container_width=True
            )
        
        with col3:
            # Export all data
            all_data = company_data.to_csv(index=False)
            st.download_button(
                label="📁 Download Raw Data",
                data=all_data,
                file_name=f"{selected_company.replace(' ', '_')}_raw_data_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )
    
    # Footer
    st.divider()
    st.markdown("""
        <div style='text-align: center; padding: 40px 20px; background: linear-gradient(135deg, rgba(255, 255, 255, 0.03) 0%, rgba(255, 255, 255, 0.01) 100%); 
                    border-radius: 20px; border: 1px solid rgba(255, 255, 255, 0.1); margin-top: 40px;'>
            <p style='color: #00ffff; font-size: 18px; font-weight: 700; margin-bottom: 10px;'>Quantum Financial Analytics v2.0</p>
            <p style='color: #a0aec0; font-size: 14px; margin-bottom: 20px;'>Powered by Advanced Quantitative Analysis</p>
            <p style='color: white; font-size: 16px;'>Created with 💎 by <strong style='color: #b794f6;'>@Gsnchez</strong></p>
            <p style='color: #4a5568; font-size: 12px; margin-top: 10px;'>bquantfinance.com | Next-Generation Financial Intelligence</p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
