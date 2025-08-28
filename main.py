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
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #00d4ff 0%, #00a8cc 100%);
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# Load data function
@st.cache_data
def load_data():
    sociedades = pd.read_excel('sociedades_estructurado.xlsx')
    agencias = pd.read_excel('agencias_estructurado.xlsx')
    
    # Add tipo column
    sociedades['tipo'] = 'Sociedad'
    agencias['tipo'] = 'Agencia'
    
    # Combine datasets
    combined = pd.concat([sociedades, agencias], ignore_index=True)
    
    # Convert fecha to datetime
    for df in [sociedades, agencias, combined]:
        df['fecha'] = pd.to_datetime(df['fecha'])
    
    return sociedades, agencias, combined

# Dark theme for plotly
plotly_dark_template = {
    'layout': {
        'paper_bgcolor': '#0e1117',
        'plot_bgcolor': '#1a1d24',
        'font': {'color': '#e8e8ea'},
        'xaxis': {
            'gridcolor': '#262730',
            'linecolor': '#262730',
            'tickfont': {'color': '#b0b3b8'}
        },
        'yaxis': {
            'gridcolor': '#262730',
            'linecolor': '#262730',
            'tickfont': {'color': '#b0b3b8'}
        },
        'colorway': ['#00d4ff', '#00ff88', '#ffaa00', '#ff3366', '#aa66ff', '#66ffff']
    }
}

# Main app
def main():
    # Header
    st.markdown('<h1 class="custom-header">Financial Analytics Dashboard</h1>', unsafe_allow_html=True)
    st.markdown('<p class="custom-subheader">by @Gsnchez | bquantfinance.com</p>', unsafe_allow_html=True)
    
    # Load data
    with st.spinner('Loading data...'):
        sociedades, agencias, combined = load_data()
    
    # Sidebar
    with st.sidebar:
        st.markdown("## 🎛️ Control Panel")
        
        # Data type selector
        data_type = st.selectbox(
            "📊 Select Data Type",
            ["Combined", "Sociedades", "Agencias"],
            help="Choose which dataset to analyze"
        )
        
        # Period selector
        available_periods = sorted(combined['periodo'].unique())
        selected_periods = st.multiselect(
            "📅 Select Periods",
            available_periods,
            default=available_periods[-2:] if len(available_periods) >= 2 else available_periods
        )
        
        # Entity selector
        if data_type == "Combined":
            df_filtered = combined[combined['periodo'].isin(selected_periods)]
        elif data_type == "Sociedades":
            df_filtered = sociedades[sociedades['periodo'].isin(selected_periods)]
        else:
            df_filtered = agencias[agencias['periodo'].isin(selected_periods)]
        
        available_entities = sorted(df_filtered['entidad'].unique())
        selected_entities = st.multiselect(
            "🏢 Select Entities",
            available_entities,
            default=available_entities[:5] if len(available_entities) >= 5 else available_entities
        )
        
        st.divider()
        st.markdown("### 📈 Metrics Settings")
        
        # Metric selector
        metric_columns = ['fondos_propios', 'activos_totales', 'comisiones_percibidas', 
                         'comisiones_netas', 'margen_bruto', 'gastos_explotacion', 
                         'resultados_antes_impuestos']
        
        primary_metric = st.selectbox(
            "Primary Metric",
            metric_columns,
            index=2
        )
        
        secondary_metric = st.selectbox(
            "Secondary Metric",
            metric_columns,
            index=6
        )
    
    # Filter data
    if selected_entities:
        df_filtered = df_filtered[df_filtered['entidad'].isin(selected_entities)]
    
    # Main content - Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Overview", "📈 Time Analysis", "🏢 Entity Analysis", "🔍 Comparative", "📋 Data Tables"])
    
    with tab1:
        # KPI Metrics
        col1, col2, col3, col4 = st.columns(4)
        
        if not df_filtered.empty:
            with col1:
                total_assets = df_filtered['activos_totales'].sum()
                st.metric(
                    label="Total Assets",
                    value=f"€{total_assets:,.0f}K",
                    delta=f"{((df_filtered['activos_totales'].mean() / df_filtered['activos_totales'].std()) * 100):.1f}% CV" if df_filtered['activos_totales'].std() > 0 else "0%"
                )
            
            with col2:
                total_equity = df_filtered['fondos_propios'].sum()
                st.metric(
                    label="Total Equity",
                    value=f"€{total_equity:,.0f}K",
                    delta=f"{(total_equity/total_assets*100):.1f}% of assets" if total_assets > 0 else "0%"
                )
            
            with col3:
                total_commissions = df_filtered['comisiones_percibidas'].sum()
                st.metric(
                    label="Total Commissions",
                    value=f"€{total_commissions:,.0f}K",
                    delta=f"{((df_filtered['comisiones_netas'].sum()/total_commissions)*100):.1f}% net" if total_commissions > 0 else "0%"
                )
            
            with col4:
                total_results = df_filtered['resultados_antes_impuestos'].sum()
                st.metric(
                    label="Results Before Tax",
                    value=f"€{total_results:,.0f}K",
                    delta=f"{(total_results/df_filtered['margen_bruto'].sum()*100):.1f}% margin" if df_filtered['margen_bruto'].sum() > 0 else "0%",
                    delta_color="normal" if total_results > 0 else "inverse"
                )
            
            # Distribution charts
            col1, col2 = st.columns(2)
            
            with col1:
                # Donut chart for entity distribution
                entity_dist = df_filtered.groupby('entidad')[primary_metric].sum().reset_index()
                entity_dist = entity_dist.nlargest(10, primary_metric)
                
                fig_donut = go.Figure(data=[go.Pie(
                    labels=entity_dist['entidad'],
                    values=entity_dist[primary_metric],
                    hole=.6,
                    marker=dict(colors=plotly_dark_template['layout']['colorway']),
                    textfont=dict(color='white')
                )])
                fig_donut.update_layout(
                    title=f"Top 10 Entities by {primary_metric.replace('_', ' ').title()}",
                    **plotly_dark_template['layout'],
                    height=400,
                    showlegend=False
                )
                st.plotly_chart(fig_donut, use_container_width=True)
            
            with col2:
                # Scatter plot efficiency
                fig_scatter = px.scatter(
                    df_filtered,
                    x='gastos_explotacion',
                    y='comisiones_percibidas',
                    size='activos_totales',
                    color='tipo' if 'tipo' in df_filtered.columns else None,
                    hover_data=['entidad', 'periodo'],
                    title="Operational Efficiency Analysis",
                    labels={'gastos_explotacion': 'Operating Expenses', 
                           'comisiones_percibidas': 'Commissions Received'}
                )
                fig_scatter.update_layout(**plotly_dark_template['layout'], height=400)
                fig_scatter.update_traces(marker=dict(line=dict(width=1, color='white')))
                st.plotly_chart(fig_scatter, use_container_width=True)
    
    with tab2:
        st.markdown("### 📈 Time Series Analysis")
        
        if not df_filtered.empty:
            # Time series chart
            time_data = df_filtered.groupby(['fecha', 'tipo'] if 'tipo' in df_filtered.columns else 'fecha')[
                [primary_metric, secondary_metric]].sum().reset_index()
            
            # Create subplot figure
            fig_time = make_subplots(
                rows=2, cols=1,
                subplot_titles=(f"{primary_metric.replace('_', ' ').title()} Over Time",
                              f"{secondary_metric.replace('_', ' ').title()} Over Time"),
                vertical_spacing=0.1
            )
            
            if 'tipo' in time_data.columns:
                for tipo in time_data['tipo'].unique():
                    tipo_data = time_data[time_data['tipo'] == tipo]
                    fig_time.add_trace(
                        go.Scatter(x=tipo_data['fecha'], y=tipo_data[primary_metric],
                                 name=f"{tipo} - {primary_metric.replace('_', ' ')}",
                                 mode='lines+markers',
                                 line=dict(width=3)),
                        row=1, col=1
                    )
                    fig_time.add_trace(
                        go.Scatter(x=tipo_data['fecha'], y=tipo_data[secondary_metric],
                                 name=f"{tipo} - {secondary_metric.replace('_', ' ')}",
                                 mode='lines+markers',
                                 line=dict(width=3)),
                        row=2, col=1
                    )
            else:
                fig_time.add_trace(
                    go.Scatter(x=time_data['fecha'], y=time_data[primary_metric],
                             name=primary_metric.replace('_', ' ').title(),
                             mode='lines+markers',
                             line=dict(width=3, color='#00d4ff')),
                    row=1, col=1
                )
                fig_time.add_trace(
                    go.Scatter(x=time_data['fecha'], y=time_data[secondary_metric],
                             name=secondary_metric.replace('_', ' ').title(),
                             mode='lines+markers',
                             line=dict(width=3, color='#00ff88')),
                    row=2, col=1
                )
            
            fig_time.update_layout(**plotly_dark_template['layout'], height=700, showlegend=True)
            st.plotly_chart(fig_time, use_container_width=True)
            
            # Growth metrics
            col1, col2, col3 = st.columns(3)
            
            periods_sorted = sorted(df_filtered['fecha'].unique())
            if len(periods_sorted) > 1:
                latest_period = df_filtered[df_filtered['fecha'] == periods_sorted[-1]]
                previous_period = df_filtered[df_filtered['fecha'] == periods_sorted[-2]]
                
                with col1:
                    growth_assets = ((latest_period['activos_totales'].sum() - previous_period['activos_totales'].sum()) / 
                                   previous_period['activos_totales'].sum() * 100) if previous_period['activos_totales'].sum() > 0 else 0
                    st.metric("Assets Growth", f"{growth_assets:.1f}%", delta=f"Period-over-Period")
                
                with col2:
                    growth_comm = ((latest_period['comisiones_percibidas'].sum() - previous_period['comisiones_percibidas'].sum()) / 
                                 previous_period['comisiones_percibidas'].sum() * 100) if previous_period['comisiones_percibidas'].sum() > 0 else 0
                    st.metric("Commissions Growth", f"{growth_comm:.1f}%", delta=f"Period-over-Period")
                
                with col3:
                    efficiency_latest = (latest_period['resultados_antes_impuestos'].sum() / 
                                       latest_period['margen_bruto'].sum() * 100) if latest_period['margen_bruto'].sum() > 0 else 0
                    efficiency_previous = (previous_period['resultados_antes_impuestos'].sum() / 
                                         previous_period['margen_bruto'].sum() * 100) if previous_period['margen_bruto'].sum() > 0 else 0
                    efficiency_change = efficiency_latest - efficiency_previous
                    st.metric("Profit Margin", f"{efficiency_latest:.1f}%", delta=f"{efficiency_change:.1f}pp")
    
    with tab3:
        st.markdown("### 🏢 Entity Performance Analysis")
        
        if not df_filtered.empty:
            # Entity ranking
            entity_summary = df_filtered.groupby('entidad').agg({
                'fondos_propios': 'mean',
                'activos_totales': 'mean',
                'comisiones_percibidas': 'sum',
                'resultados_antes_impuestos': 'sum'
            }).round(0)
            
            # Calculate ROA
            entity_summary['ROA'] = (entity_summary['resultados_antes_impuestos'] / 
                                    entity_summary['activos_totales'] * 100)
            entity_summary = entity_summary.sort_values('comisiones_percibidas', ascending=False)
            
            # Top performers heatmap
            top_10 = entity_summary.head(10)
            
            # Normalize data for heatmap
            heatmap_data = top_10[['fondos_propios', 'activos_totales', 'comisiones_percibidas', 'ROA']]
            heatmap_normalized = (heatmap_data - heatmap_data.min()) / (heatmap_data.max() - heatmap_data.min())
            
            fig_heatmap = go.Figure(data=go.Heatmap(
                z=heatmap_normalized.T.values,
                x=heatmap_normalized.index,
                y=['Equity', 'Assets', 'Commissions', 'ROA'],
                colorscale='Viridis',
                text=heatmap_data.T.round(1).values,
                texttemplate='%{text}',
                textfont={"size": 10},
                hoverongaps=False
            ))
            
            fig_heatmap.update_layout(
                title="Top 10 Entities Performance Heatmap (Normalized)",
                **plotly_dark_template['layout'],
                height=400,
                xaxis={'tickangle': -45}
            )
            st.plotly_chart(fig_heatmap, use_container_width=True)
            
            # Performance metrics
            col1, col2 = st.columns(2)
            
            with col1:
                # ROA distribution
                fig_roa = px.histogram(
                    entity_summary,
                    x='ROA',
                    nbins=20,
                    title="Return on Assets Distribution",
                    labels={'ROA': 'ROA (%)', 'count': 'Number of Entities'}
                )
                fig_roa.update_layout(**plotly_dark_template['layout'], height=350)
                fig_roa.update_traces(marker_color='#00ff88')
                st.plotly_chart(fig_roa, use_container_width=True)
            
            with col2:
                # Efficiency ratio
                entity_summary['efficiency_ratio'] = (entity_summary['comisiones_percibidas'] / 
                                                     entity_summary['activos_totales'] * 100)
                
                fig_eff = px.box(
                    entity_summary.reset_index(),
                    y='efficiency_ratio',
                    title="Commission Efficiency Distribution",
                    labels={'efficiency_ratio': 'Commission/Assets Ratio (%)'}
                )
                fig_eff.update_layout(**plotly_dark_template['layout'], height=350)
                fig_eff.update_traces(marker_color='#ffaa00')
                st.plotly_chart(fig_eff, use_container_width=True)
    
    with tab4:
        st.markdown("### 🔍 Comparative Analysis")
        
        if not df_filtered.empty and 'tipo' in df_filtered.columns:
            # Comparison by type
            type_comparison = df_filtered.groupby('tipo')[metric_columns].mean().round(0)
            
            # Radar chart
            categories = ['Equity', 'Assets', 'Commissions', 'Net Comm.', 'Gross Margin', 'Op. Expenses', 'PBT']
            
            fig_radar = go.Figure()
            
            for tipo in type_comparison.index:
                values = type_comparison.loc[tipo].values
                # Normalize values for better visualization
                max_vals = type_comparison.max().values
                normalized_values = [(v/m*100) if m > 0 else 0 for v, m in zip(values, max_vals)]
                
                fig_radar.add_trace(go.Scatterpolar(
                    r=normalized_values,
                    theta=categories,
                    fill='toself',
                    name=tipo
                ))
            
            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 100],
                        gridcolor='#262730',
                        tickfont=dict(color='#b0b3b8')
                    ),
                    angularaxis=dict(gridcolor='#262730')
                ),
                title="Sociedades vs Agencias Comparison (Normalized)",
                **plotly_dark_template['layout'],
                height=500
            )
            st.plotly_chart(fig_radar, use_container_width=True)
            
            # Statistical comparison
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("##### 📊 Average Metrics by Type")
                comparison_df = type_comparison[['fondos_propios', 'activos_totales', 
                                                'comisiones_percibidas', 'resultados_antes_impuestos']]
                comparison_df.columns = ['Equity', 'Assets', 'Commissions', 'Results']
                st.dataframe(
                    comparison_df.style.format("{:,.0f}").background_gradient(cmap='Blues'),
                    use_container_width=True
                )
            
            with col2:
                st.markdown("##### 📈 Efficiency Metrics")
                efficiency_comp = pd.DataFrame({
                    'ROA (%)': (df_filtered.groupby('tipo')['resultados_antes_impuestos'].sum() / 
                              df_filtered.groupby('tipo')['activos_totales'].sum() * 100),
                    'Profit Margin (%)': (df_filtered.groupby('tipo')['resultados_antes_impuestos'].sum() / 
                                        df_filtered.groupby('tipo')['margen_bruto'].sum() * 100),
                    'Cost/Income (%)': (df_filtered.groupby('tipo')['gastos_explotacion'].sum() / 
                                       df_filtered.groupby('tipo')['margen_bruto'].sum() * 100)
                })
                st.dataframe(
                    efficiency_comp.style.format("{:.2f}").background_gradient(cmap='Greens'),
                    use_container_width=True
                )
    
    with tab5:
        st.markdown("### 📋 Detailed Data Tables")
        
        # Summary statistics
        st.markdown("##### 📊 Summary Statistics")
        summary_stats = df_filtered[metric_columns].describe().round(0)
        st.dataframe(
            summary_stats.style.format("{:,.0f}").background_gradient(cmap='RdYlGn'),
            use_container_width=True
        )
        
        # Raw data with filters
        st.markdown("##### 🔍 Filtered Raw Data")
        
        # Column selector
        display_columns = st.multiselect(
            "Select columns to display:",
            df_filtered.columns.tolist(),
            default=['entidad', 'periodo', 'fondos_propios', 'activos_totales', 
                    'comisiones_percibidas', 'resultados_antes_impuestos']
        )
        
        if display_columns:
            st.dataframe(
                df_filtered[display_columns].style.format({
                    col: "{:,.0f}" for col in display_columns 
                    if col in metric_columns
                }),
                use_container_width=True,
                height=400
            )
        
        # Download buttons
        col1, col2, col3 = st.columns(3)
        
        with col1:
            csv = df_filtered.to_csv(index=False)
            st.download_button(
                label="📥 Download Filtered Data (CSV)",
                data=csv,
                file_name=f"financial_data_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col2:
            # Create summary report
            summary_report = f"""
Financial Analysis Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
Created by: @Gsnchez | bquantfinance.com

SUMMARY METRICS
===============
Total Entities: {df_filtered['entidad'].nunique()}
Total Records: {len(df_filtered)}
Periods Analyzed: {', '.join(selected_periods)}

KEY FINANCIALS
==============
Total Assets: €{df_filtered['activos_totales'].sum():,.0f}K
Total Equity: €{df_filtered['fondos_propios'].sum():,.0f}K
Total Commissions: €{df_filtered['comisiones_percibidas'].sum():,.0f}K
Total Results (PBT): €{df_filtered['resultados_antes_impuestos'].sum():,.0f}K

PERFORMANCE INDICATORS
=====================
Average ROA: {(df_filtered['resultados_antes_impuestos'].sum() / df_filtered['activos_totales'].sum() * 100):.2f}%
Profit Margin: {(df_filtered['resultados_antes_impuestos'].sum() / df_filtered['margen_bruto'].sum() * 100):.2f}%
Cost/Income Ratio: {(df_filtered['gastos_explotacion'].sum() / df_filtered['margen_bruto'].sum() * 100):.2f}%
            """
            st.download_button(
                label="📄 Download Summary Report",
                data=summary_report,
                file_name=f"financial_report_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain",
                use_container_width=True
            )
        
        with col3:
            # Entity ranking
            ranking = df_filtered.groupby('entidad')[primary_metric].sum().sort_values(ascending=False)
            ranking_text = f"Top Entities by {primary_metric.replace('_', ' ').title()}\n" + "="*50 + "\n"
            for i, (entity, value) in enumerate(ranking.head(20).items(), 1):
                ranking_text += f"{i}. {entity}: €{value:,.0f}K\n"
            
            st.download_button(
                label="🏆 Download Rankings",
                data=ranking_text,
                file_name=f"entity_rankings_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain",
                use_container_width=True
            )
    
    # Footer
    st.divider()
    st.markdown("""
        <div style='text-align: center; color: #666; padding: 20px;'>
            <p>Financial Analytics Dashboard v1.0 | Created with ❤️ by <strong>@Gsnchez</strong></p>
            <p style='font-size: 12px;'>bquantfinance.com | Advanced Quantitative Finance Solutions</p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
