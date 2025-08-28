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
    page_title="Análisis Financiero - ESIs y AVs",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional CSS styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    /* Variables de color */
    :root {
        --primary-bg: #0a0a0f;
        --secondary-bg: #12121a;
        --card-bg: #1a1a25;
        --glass-bg: rgba(26, 26, 37, 0.7);
        --accent-cyan: #00d4ff;
        --accent-purple: #b794f6;
        --accent-pink: #f687b3;
        --accent-blue: #4299e1;
        --accent-green: #48bb78;
        --text-primary: #ffffff;
        --text-secondary: #a0aec0;
        --border-color: rgba(255, 255, 255, 0.1);
        --gradient-1: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --gradient-2: linear-gradient(135deg, #00d4ff 0%, #b794f6 100%);
    }
    
    /* Fondo principal */
    .stApp {
        background: 
            radial-gradient(circle at 20% 50%, rgba(120, 119, 198, 0.15) 0%, transparent 50%),
            radial-gradient(circle at 80% 80%, rgba(255, 119, 198, 0.15) 0%, transparent 50%),
            linear-gradient(180deg, #0a0a0f 0%, #12121a 100%);
        background-attachment: fixed;
    }
    
    /* Encabezado principal */
    .main-header {
        background: linear-gradient(135deg, #00d4ff 0%, #b794f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 48px;
        font-weight: 800;
        text-align: center;
        margin-bottom: 5px;
        font-family: 'Inter', sans-serif;
        letter-spacing: -1px;
        line-height: 1.1;
    }
    
    .sub-header {
        text-align: center;
        color: #a0aec0;
        font-size: 14px;
        font-weight: 500;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 30px;
    }
    
    /* Tarjetas de métricas */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.02) 100%);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.2);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    [data-testid="metric-container"]:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 40px 0 rgba(31, 38, 135, 0.3);
        border-color: rgba(0, 212, 255, 0.3);
    }
    
    /* Etiquetas de métricas */
    [data-testid="metric-container"] label {
        font-size: 12px;
        font-weight: 600;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        color: var(--text-secondary);
    }
    
    [data-testid="metric-container"] > div > div {
        font-size: 28px;
        font-weight: 700;
        color: #ffffff;
    }
    
    /* Barra lateral */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(26, 26, 37, 0.95) 0%, rgba(18, 18, 26, 0.95) 100%);
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Selectores */
    .stSelectbox > div > div,
    .stMultiselect > div > div {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 10px;
        color: white;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stSelectbox > div > div:hover,
    .stMultiselect > div > div:hover {
        border-color: var(--accent-cyan);
        box-shadow: 0 0 15px rgba(0, 212, 255, 0.2);
    }
    
    /* Pestañas */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 12px;
        padding: 6px;
        gap: 6px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: var(--text-secondary);
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 600;
        font-size: 14px;
        transition: all 0.3s ease;
        border: 1px solid transparent;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(255, 255, 255, 0.05);
        color: var(--text-primary);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(0, 212, 255, 0.15) 0%, rgba(183, 148, 246, 0.15) 100%);
        color: var(--text-primary);
        border: 1px solid rgba(0, 212, 255, 0.3);
    }
    
    /* Botones */
    .stButton > button {
        background: linear-gradient(135deg, #00d4ff 0%, #b794f6 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 600;
        font-size: 14px;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 212, 255, 0.3);
    }
    
    /* Botones de descarga */
    .stDownloadButton > button {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: var(--accent-cyan);
        transition: all 0.3s ease;
    }
    
    .stDownloadButton > button:hover {
        background: rgba(0, 212, 255, 0.1);
        border-color: var(--accent-cyan);
    }
    
    /* Tarjeta personalizada */
    .custom-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.02) 100%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 20px;
        margin: 16px 0;
        backdrop-filter: blur(10px);
    }
    
    /* Divisor de tipo */
    .type-badge-sociedad {
        background: linear-gradient(135deg, #b794f6 0%, #9f7aea 100%);
        color: white;
        padding: 4px 12px;
        border-radius: 16px;
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.5px;
        display: inline-block;
    }
    
    .type-badge-agencia {
        background: linear-gradient(135deg, #00d4ff 0%, #0091ff 100%);
        color: white;
        padding: 4px 12px;
        border-radius: 16px;
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.5px;
        display: inline-block;
    }
    </style>
    """, unsafe_allow_html=True)

# Función para cargar datos
@st.cache_data
def load_data():
    try:
        sociedades = pd.read_excel('sociedades_estructurado.xlsx')
        agencias = pd.read_excel('agencias_estructurado.xlsx')
    except FileNotFoundError:
        # Try alternative paths if files are in a different location
        try:
            sociedades = pd.read_excel('./sociedades_estructurado.xlsx')
            agencias = pd.read_excel('./agencias_estructurado.xlsx')
        except:
            st.error("❌ No se encontraron los archivos de datos. Asegúrese de que 'sociedades_estructurado.xlsx' y 'agencias_estructurado.xlsx' estén en el directorio del proyecto.")
            st.stop()
    
    # Añadir columna tipo
    sociedades['tipo'] = 'Sociedad'
    agencias['tipo'] = 'Agencia'
    
    # Combinar datasets
    combined = pd.concat([sociedades, agencias], ignore_index=True)
    
    # Convertir fecha a datetime
    for df in [sociedades, agencias, combined]:
        df['fecha'] = pd.to_datetime(df['fecha'])
    
    return sociedades, agencias, combined

# Calcular métricas trimestrales
def calculate_quarterly_metrics(df, entity):
    entity_data = df[df['entidad'] == entity].sort_values('fecha')
    
    if len(entity_data) < 1:
        return None
    
    metrics = []
    for i in range(len(entity_data)):
        row = entity_data.iloc[i]
        metrics_dict = {
            'periodo': row['periodo'],
            'fecha': row['fecha'],
            'tipo': row['tipo'],
            'fondos_propios': row['fondos_propios'],
            'activos_totales': row['activos_totales'],
            'comisiones_percibidas': row['comisiones_percibidas'],
            'comisiones_netas': row['comisiones_netas'],
            'margen_bruto': row['margen_bruto'],
            'gastos_explotacion': row['gastos_explotacion'],
            'resultados_antes_impuestos': row['resultados_antes_impuestos'],
            'ROA': (row['resultados_antes_impuestos'] / row['activos_totales'] * 100) if row['activos_totales'] > 0 else 0,
            'ROE': (row['resultados_antes_impuestos'] / row['fondos_propios'] * 100) if row['fondos_propios'] > 0 else 0,
            'ratio_eficiencia': (row['gastos_explotacion'] / row['margen_bruto'] * 100) if row['margen_bruto'] > 0 else 0,
            'margen_neto': (row['resultados_antes_impuestos'] / row['comisiones_percibidas'] * 100) if row['comisiones_percibidas'] > 0 else 0,
            'apalancamiento': (row['activos_totales'] / row['fondos_propios']) if row['fondos_propios'] > 0 else 0
        }
        
        # Calcular cambios trimestre a trimestre
        if i > 0:
            prev_row = entity_data.iloc[i-1]
            metrics_dict['var_activos'] = ((row['activos_totales'] - prev_row['activos_totales']) / prev_row['activos_totales'] * 100) if prev_row['activos_totales'] > 0 else 0
            metrics_dict['var_ingresos'] = ((row['comisiones_percibidas'] - prev_row['comisiones_percibidas']) / prev_row['comisiones_percibidas'] * 100) if prev_row['comisiones_percibidas'] > 0 else 0
            metrics_dict['var_beneficio'] = ((row['resultados_antes_impuestos'] - prev_row['resultados_antes_impuestos']) / abs(prev_row['resultados_antes_impuestos']) * 100) if prev_row['resultados_antes_impuestos'] != 0 else 0
        else:
            metrics_dict['var_activos'] = 0
            metrics_dict['var_ingresos'] = 0
            metrics_dict['var_beneficio'] = 0
        
        metrics.append(metrics_dict)
    
    return pd.DataFrame(metrics)

# Tema oscuro profesional para plotly
professional_theme = {
    'layout': {
        'paper_bgcolor': 'rgba(10, 10, 15, 0)',
        'plot_bgcolor': 'rgba(18, 18, 26, 0.3)',
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
        'colorway': ['#00d4ff', '#b794f6', '#f687b3', '#4299e1', '#48bb78', '#ed8936'],
        'hovermode': 'x unified',
        'hoverlabel': {
            'bgcolor': 'rgba(26, 26, 37, 0.95)',
            'bordercolor': '#00d4ff',
            'font': {'color': '#ffffff'}
        }
    }
}

# Aplicación principal
def main():
    # Encabezado
    st.markdown('<h1 class="main-header">Panel de Análisis Financiero</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Sociedades de Valores y Agencias de Valores - Análisis Trimestral</p>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #4a5568; font-size: 12px; margin-bottom: 30px;">Desarrollado por @Gsnchez | bquantfinance.com</p>', unsafe_allow_html=True)
    
    # Cargar datos directamente
    with st.spinner('⏳ Cargando datos financieros...'):
        try:
            sociedades, agencias, combined = load_data()
            
            # Mostrar información de datos cargados
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(
                    label="📊 Total Registros",
                    value=f"{len(combined):,}",
                    delta=None
                )
            with col2:
                st.metric(
                    label="🏢 Sociedades",
                    value=f"{sociedades['entidad'].nunique()}",
                    delta=None
                )
            with col3:
                st.metric(
                    label="🏦 Agencias",
                    value=f"{agencias['entidad'].nunique()}",
                    delta=None
                )
            
        except Exception as e:
            st.error(f"❌ Error al cargar los datos: {str(e)}")
            st.info("""
            ### 📁 Archivos Requeridos
            
            Asegúrese de que los siguientes archivos estén en el directorio del proyecto:
            - **sociedades_estructurado.xlsx**: Datos de Sociedades de Valores
            - **agencias_estructurado.xlsx**: Datos de Agencias de Valores
            
            Los archivos deben contener las siguientes columnas:
            - entidad, periodo, fecha, año, mes
            - fondos_propios, activos_totales
            - comisiones_percibidas, comisiones_netas
            - margen_bruto, gastos_explotacion
            - resultados_antes_impuestos
            """)
            st.stop()
    
    # Configuración en barra lateral
    with st.sidebar:
        st.markdown("## ⚙️ Configuración del Análisis")
        
        # Filtro por tipo de entidad
        st.markdown("### 🏢 Tipo de Entidad")
        tipo_entidad = st.radio(
            "Seleccionar tipo",
            ["Ambos Tipos", "Sociedades de Valores", "Agencias de Valores"],
            help="Filtrar por tipo de entidad financiera"
        )
        
        # Filtrar datos según tipo seleccionado
        if tipo_entidad == "Sociedades de Valores":
            filtered_combined = combined[combined['tipo'] == 'Sociedad']
        elif tipo_entidad == "Agencias de Valores":
            filtered_combined = combined[combined['tipo'] == 'Agencia']
        else:
            filtered_combined = combined
        
        st.divider()
        
        # Selector de empresa
        st.markdown("### 🏢 Selección de Empresa")
        all_entities = sorted(filtered_combined['entidad'].unique())
        
        # Empresa principal
        selected_company = st.selectbox(
            "Empresa Principal",
            all_entities,
            help="Seleccione la empresa para análisis detallado",
            index=0 if len(all_entities) > 0 else None
        )
        
        # Obtener tipo de la empresa seleccionada
        company_type = filtered_combined[filtered_combined['entidad'] == selected_company]['tipo'].iloc[0] if selected_company else None
        
        # Empresas de comparación (filtrar por mismo tipo)
        if company_type:
            comparison_entities = filtered_combined[filtered_combined['tipo'] == company_type]['entidad'].unique()
            comparison_entities = [e for e in comparison_entities if e != selected_company]
        else:
            comparison_entities = [e for e in all_entities if e != selected_company]
        
        comparison_companies = st.multiselect(
            "Empresas de Comparación",
            comparison_entities,
            default=comparison_entities[:3] if len(comparison_entities) >= 3 else comparison_entities,
            help="Seleccione empresas para comparación"
        )
        
        st.divider()
        
        # Filtro de período
        st.markdown("### 📅 Período de Análisis")
        available_periods = sorted(combined['periodo'].unique())
        selected_periods = st.multiselect(
            "Seleccionar Trimestres",
            available_periods,
            default=available_periods,
            help="Elija los trimestres a incluir"
        )
        
        st.divider()
        
        # Opciones de análisis
        st.markdown("### 📈 Configuración de Métricas")
        primary_metric = st.selectbox(
            "Métrica Principal",
            ['comisiones_percibidas', 'resultados_antes_impuestos', 'activos_totales', 'fondos_propios'],
            format_func=lambda x: {
                'comisiones_percibidas': 'Comisiones Percibidas',
                'resultados_antes_impuestos': 'Resultado antes de Impuestos',
                'activos_totales': 'Activos Totales',
                'fondos_propios': 'Fondos Propios'
            }[x],
            index=0
        )
        
        show_comparison = st.checkbox("Mostrar Comparación Sociedades vs Agencias", value=True)
        show_trends = st.checkbox("Mostrar Líneas de Tendencia", value=True)
    
    # Filtrar datos
    company_data = combined[(combined['entidad'] == selected_company) & 
                           (combined['periodo'].isin(selected_periods))].sort_values('fecha')
    
    comparison_data = combined[(combined['entidad'].isin(comparison_companies)) & 
                               (combined['periodo'].isin(selected_periods))]
    
    # Contenido principal
    if not company_data.empty:
        # Nombre de empresa y tipo
        company_type = company_data.iloc[0]['tipo']
        badge_class = "type-badge-sociedad" if company_type == "Sociedad" else "type-badge-agencia"
        type_label = "SOCIEDAD DE VALORES" if company_type == "Sociedad" else "AGENCIA DE VALORES"
        
        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 30px;">
            <h2 style="color: white; font-size: 28px; font-weight: 700; margin-bottom: 10px;">{selected_company}</h2>
            <span class="{badge_class}">{type_label}</span>
        </div>
        """, unsafe_allow_html=True)
        
        # Calcular métricas trimestrales
        quarterly_metrics = calculate_quarterly_metrics(combined, selected_company)
        
        if quarterly_metrics is not None and not quarterly_metrics.empty:
            # KPIs del último trimestre
            latest = quarterly_metrics.iloc[-1]
            prev = quarterly_metrics.iloc[-2] if len(quarterly_metrics) > 1 else latest
            
            # Tarjetas de KPI
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    label="💰 Comisiones Percibidas",
                    value=f"€{latest['comisiones_percibidas']:,.0f}K",
                    delta=f"{latest['var_ingresos']:.1f}% vs trim. anterior" if len(quarterly_metrics) > 1 else None,
                    delta_color="normal"
                )
            
            with col2:
                st.metric(
                    label="📊 Resultado antes Impuestos",
                    value=f"€{latest['resultados_antes_impuestos']:,.0f}K",
                    delta=f"{latest['var_beneficio']:.1f}% vs trim. anterior" if len(quarterly_metrics) > 1 else None,
                    delta_color="normal"
                )
            
            with col3:
                st.metric(
                    label="📈 ROE",
                    value=f"{latest['ROE']:.1f}%",
                    delta=f"{latest['ROE'] - prev['ROE']:.1f}pp" if len(quarterly_metrics) > 1 else None,
                    delta_color="normal"
                )
            
            with col4:
                st.metric(
                    label="⚡ Ratio de Eficiencia",
                    value=f"{latest['ratio_eficiencia']:.1f}%",
                    delta=f"{latest['ratio_eficiencia'] - prev['ratio_eficiencia']:.1f}pp" if len(quarterly_metrics) > 1 else None,
                    delta_color="inverse"
                )
            
            # Pestañas para diferentes vistas
            tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
                "📊 Rendimiento Trimestral", 
                "📈 Análisis de Crecimiento", 
                "⚡ Métricas de Eficiencia",
                "🏆 Comparación con Competidores",
                "⚖️ Sociedades vs Agencias",
                "📉 Salud Financiera"
            ])
            
            with tab1:
                st.markdown("### 📊 Desglose del Rendimiento Trimestre a Trimestre")
                
                # Gráfico integral de rendimiento
                fig = make_subplots(
                    rows=2, cols=2,
                    subplot_titles=("Evolución de Ingresos y Beneficio", "Crecimiento de Activos y Patrimonio", 
                                   "Tasas de Crecimiento Intertrimestral", "Análisis de Márgenes"),
                    vertical_spacing=0.12,
                    horizontal_spacing=0.10,
                    specs=[[{'secondary_y': True}, {'secondary_y': True}],
                           [{'secondary_y': False}, {'secondary_y': False}]]
                )
                
                # Ingresos y Beneficio
                fig.add_trace(
                    go.Bar(x=quarterly_metrics['periodo'], y=quarterly_metrics['comisiones_percibidas'],
                          name='Comisiones', marker_color='#00d4ff', opacity=0.7,
                          text=quarterly_metrics['comisiones_percibidas'].round(0),
                          textposition='outside', textfont=dict(size=10)),
                    row=1, col=1, secondary_y=False
                )
                fig.add_trace(
                    go.Scatter(x=quarterly_metrics['periodo'], y=quarterly_metrics['resultados_antes_impuestos'],
                              name='Beneficio', line=dict(color='#f687b3', width=3),
                              mode='lines+markers', marker=dict(size=10)),
                    row=1, col=1, secondary_y=True
                )
                
                # Activos y Patrimonio
                fig.add_trace(
                    go.Bar(x=quarterly_metrics['periodo'], y=quarterly_metrics['activos_totales'],
                          name='Activos', marker_color='#4299e1', opacity=0.7),
                    row=1, col=2, secondary_y=False
                )
                fig.add_trace(
                    go.Scatter(x=quarterly_metrics['periodo'], y=quarterly_metrics['fondos_propios'],
                              name='Patrimonio', line=dict(color='#48bb78', width=3),
                              mode='lines+markers', marker=dict(size=10)),
                    row=1, col=2, secondary_y=True
                )
                
                # Tasas de crecimiento
                if len(quarterly_metrics) > 1:
                    fig.add_trace(
                        go.Scatter(x=quarterly_metrics['periodo'][1:], y=quarterly_metrics['var_ingresos'][1:],
                                  name='Crec. Ingresos', line=dict(color='#00d4ff', width=2),
                                  mode='lines+markers', marker=dict(size=8)),
                        row=2, col=1
                    )
                    fig.add_trace(
                        go.Scatter(x=quarterly_metrics['periodo'][1:], y=quarterly_metrics['var_activos'][1:],
                                  name='Crec. Activos', line=dict(color='#b794f6', width=2),
                                  mode='lines+markers', marker=dict(size=8)),
                        row=2, col=1
                    )
                
                # Márgenes
                fig.add_trace(
                    go.Scatter(x=quarterly_metrics['periodo'], y=quarterly_metrics['margen_neto'],
                              name='Margen Neto', line=dict(color='#ed8936', width=2),
                              mode='lines+markers', fill='tozeroy', opacity=0.3),
                    row=2, col=2
                )
                
                # Actualizar diseño
                fig.update_layout(
                    **professional_theme['layout'],
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
                
                # Actualizar ejes
                fig.update_yaxes(title_text="Importe (€K)", row=1, col=1, secondary_y=False)
                fig.update_yaxes(title_text="Beneficio (€K)", row=1, col=1, secondary_y=True)
                fig.update_yaxes(title_text="Importe (€K)", row=1, col=2, secondary_y=False)
                fig.update_yaxes(title_text="Patrimonio (€K)", row=1, col=2, secondary_y=True)
                fig.update_yaxes(title_text="Tasa de Crecimiento (%)", row=2, col=1)
                fig.update_yaxes(title_text="Margen (%)", row=2, col=2)
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Tabla resumen
                st.markdown("### 📋 Resumen de Rendimiento Trimestral")
                summary_df = quarterly_metrics[['periodo', 'comisiones_percibidas', 'resultados_antes_impuestos', 
                                               'ROA', 'ROE', 'ratio_eficiencia']].round(2)
                summary_df.columns = ['Trimestre', 'Comisiones (€K)', 'RAI (€K)', 'ROA (%)', 'ROE (%)', 'Eficiencia (%)']
                st.dataframe(
                    summary_df.style.background_gradient(cmap='RdYlGn', subset=['ROA (%)', 'ROE (%)'])
                                   .background_gradient(cmap='RdYlGn_r', subset=['Eficiencia (%)']),
                    use_container_width=True
                )
            
            with tab2:
                st.markdown("### 📈 Análisis de Trayectoria de Crecimiento")
                
                # Visualización de métricas de crecimiento
                fig_growth = make_subplots(
                    rows=2, cols=2,
                    subplot_titles=("Crecimiento Acumulado de Ingresos", "Rendimiento Indexado (Base 100)",
                                   "Promedios Móviles", "Momentum de Crecimiento"),
                    vertical_spacing=0.12,
                    horizontal_spacing=0.10
                )
                
                # Crecimiento acumulado
                quarterly_metrics['cum_ingresos'] = quarterly_metrics['comisiones_percibidas'].cumsum()
                quarterly_metrics['cum_beneficio'] = quarterly_metrics['resultados_antes_impuestos'].cumsum()
                
                fig_growth.add_trace(
                    go.Scatter(x=quarterly_metrics['periodo'], y=quarterly_metrics['cum_ingresos'],
                              name='Ingresos Acum.', line=dict(color='#00d4ff', width=3),
                              mode='lines+markers', fill='tonexty', marker=dict(size=10)),
                    row=1, col=1
                )
                
                fig_growth.add_trace(
                    go.Scatter(x=quarterly_metrics['periodo'], y=quarterly_metrics['cum_beneficio'],
                              name='Beneficio Acum.', line=dict(color='#f687b3', width=3),
                              mode='lines+markers', fill='tozeroy', marker=dict(size=10)),
                    row=1, col=1
                )
                
                # Rendimiento indexado
                if len(quarterly_metrics) > 0:
                    base_revenue = quarterly_metrics['comisiones_percibidas'].iloc[0]
                    base_assets = quarterly_metrics['activos_totales'].iloc[0]
                    
                    quarterly_metrics['indice_ingresos'] = (quarterly_metrics['comisiones_percibidas'] / base_revenue * 100) if base_revenue > 0 else 100
                    quarterly_metrics['indice_activos'] = (quarterly_metrics['activos_totales'] / base_assets * 100) if base_assets > 0 else 100
                    
                    fig_growth.add_trace(
                        go.Scatter(x=quarterly_metrics['periodo'], y=quarterly_metrics['indice_ingresos'],
                                  name='Índice Ingresos', line=dict(color='#00d4ff', width=2, dash='solid'),
                                  mode='lines+markers'),
                        row=1, col=2
                    )
                    
                    fig_growth.add_trace(
                        go.Scatter(x=quarterly_metrics['periodo'], y=quarterly_metrics['indice_activos'],
                                  name='Índice Activos', line=dict(color='#4299e1', width=2, dash='dash'),
                                  mode='lines+markers'),
                        row=1, col=2
                    )
                    
                    # Línea base 100
                    fig_growth.add_hline(y=100, line_width=1, line_dash="dot", line_color="gray", row=1, col=2)
                
                # Promedios móviles
                if len(quarterly_metrics) >= 3:
                    quarterly_metrics['ma_ingresos'] = quarterly_metrics['comisiones_percibidas'].rolling(window=3, center=True).mean()
                    
                    fig_growth.add_trace(
                        go.Scatter(x=quarterly_metrics['periodo'], y=quarterly_metrics['comisiones_percibidas'],
                                  name='Ingresos Reales', line=dict(color='#00d4ff', width=2),
                                  mode='lines+markers', opacity=0.5),
                        row=2, col=1
                    )
                    
                    fig_growth.add_trace(
                        go.Scatter(x=quarterly_metrics['periodo'], y=quarterly_metrics['ma_ingresos'],
                                  name='Media Móvil 3T', line=dict(color='#b794f6', width=3),
                                  mode='lines'),
                        row=2, col=1
                    )
                
                # Momentum de crecimiento
                if len(quarterly_metrics) > 2:
                    quarterly_metrics['aceleracion_crec'] = quarterly_metrics['var_ingresos'].diff()
                    
                    colors = ['#48bb78' if x > 0 else '#ff3366' for x in quarterly_metrics['aceleracion_crec'][2:]]
                    
                    fig_growth.add_trace(
                        go.Bar(x=quarterly_metrics['periodo'][2:], y=quarterly_metrics['aceleracion_crec'][2:],
                              name='Aceleración', marker_color=colors, opacity=0.7),
                        row=2, col=2
                    )
                
                fig_growth.update_layout(**professional_theme['layout'], height=700, showlegend=True)
                st.plotly_chart(fig_growth, use_container_width=True)
                
                # Estadísticas de crecimiento
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    avg_growth = quarterly_metrics['var_ingresos'][1:].mean() if len(quarterly_metrics) > 1 else 0
                    st.markdown(f"""
                    <div class="custom-card">
                        <h4 style="color: #00d4ff;">Crecimiento Promedio</h4>
                        <p style="font-size: 28px; font-weight: 700; color: white;">{avg_growth:.1f}%</p>
                        <p style="color: #a0aec0; font-size: 12px;">Trimestre a trimestre</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    volatility = quarterly_metrics['var_ingresos'][1:].std() if len(quarterly_metrics) > 1 else 0
                    st.markdown(f"""
                    <div class="custom-card">
                        <h4 style="color: #b794f6;">Volatilidad del Crecimiento</h4>
                        <p style="font-size: 28px; font-weight: 700; color: white;">{volatility:.1f}%</p>
                        <p style="color: #a0aec0; font-size: 12px;">Desviación estándar</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    if len(quarterly_metrics) > 0:
                        total_growth = ((quarterly_metrics['comisiones_percibidas'].iloc[-1] / 
                                       quarterly_metrics['comisiones_percibidas'].iloc[0] - 1) * 100) if quarterly_metrics['comisiones_percibidas'].iloc[0] > 0 else 0
                    else:
                        total_growth = 0
                    st.markdown(f"""
                    <div class="custom-card">
                        <h4 style="color: #f687b3;">Crecimiento Total</h4>
                        <p style="font-size: 28px; font-weight: 700; color: white;">{total_growth:.1f}%</p>
                        <p style="color: #a0aec0; font-size: 12px;">Período completo</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            with tab3:
                st.markdown("### ⚡ Análisis Detallado de Eficiencia Operativa")
                
                # Métricas de eficiencia
                fig_eff = make_subplots(
                    rows=2, cols=2,
                    subplot_titles=("Evolución ROA vs ROE", "Ratio Coste-Ingreso", 
                                   "Análisis de Apalancamiento", "Puntuación de Eficiencia"),
                    vertical_spacing=0.12,
                    horizontal_spacing=0.10
                )
                
                # ROA vs ROE
                fig_eff.add_trace(
                    go.Scatter(x=quarterly_metrics['periodo'], y=quarterly_metrics['ROA'],
                              name='ROA', line=dict(color='#00d4ff', width=3),
                              mode='lines+markers', marker=dict(size=10)),
                    row=1, col=1
                )
                fig_eff.add_trace(
                    go.Scatter(x=quarterly_metrics['periodo'], y=quarterly_metrics['ROE'],
                              name='ROE', line=dict(color='#f687b3', width=3),
                              mode='lines+markers', marker=dict(size=10)),
                    row=1, col=1
                )
                
                # Ratio Coste-Ingreso
                fig_eff.add_trace(
                    go.Bar(x=quarterly_metrics['periodo'], y=quarterly_metrics['ratio_eficiencia'],
                          name='Coste/Ingreso', marker_color='#ed8936', opacity=0.7,
                          text=quarterly_metrics['ratio_eficiencia'].round(1),
                          textposition='outside'),
                    row=1, col=2
                )
                
                # Apalancamiento
                fig_eff.add_trace(
                    go.Scatter(x=quarterly_metrics['periodo'], y=quarterly_metrics['apalancamiento'],
                              name='Apalancamiento', line=dict(color='#9f7aea', width=3),
                              mode='lines+markers', fill='tozeroy', opacity=0.3),
                    row=2, col=1
                )
                
                # Puntuación de eficiencia (compuesto)
                quarterly_metrics['punt_eficiencia'] = (
                    (100 - quarterly_metrics['ratio_eficiencia']) * 0.4 +
                    quarterly_metrics['ROE'] * 0.3 +
                    quarterly_metrics['ROA'] * 0.3
                )
                
                fig_eff.add_trace(
                    go.Scatter(x=quarterly_metrics['periodo'], y=quarterly_metrics['punt_eficiencia'],
                              name='Punt. Eficiencia', line=dict(color='#48bb78', width=3),
                              mode='lines+markers', marker=dict(size=12),
                              fill='tozeroy', opacity=0.3),
                    row=2, col=2
                )
                
                fig_eff.update_layout(**professional_theme['layout'], height=700, showlegend=True)
                st.plotly_chart(fig_eff, use_container_width=True)
                
                # Benchmarks de eficiencia
                st.markdown("### 🎯 Benchmarks de Eficiencia")
                
                # Calcular percentiles para benchmarking
                all_companies_metrics = []
                for entity in all_entities:
                    entity_metrics = calculate_quarterly_metrics(combined, entity)
                    if entity_metrics is not None and not entity_metrics.empty:
                        all_companies_metrics.append(entity_metrics)
                
                if all_companies_metrics:
                    all_metrics_df = pd.concat(all_companies_metrics)
                    
                    # Comparar con percentiles
                    latest_metrics = quarterly_metrics.iloc[-1]
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        roa_percentile = (all_metrics_df['ROA'] < latest_metrics['ROA']).mean() * 100
                        color = "#48bb78" if roa_percentile > 50 else "#ff3366"
                        st.markdown(f"""
                        <div class="custom-card">
                            <h4 style="color: {color};">Percentil ROA</h4>
                            <p style="font-size: 28px; font-weight: 700; color: white;">{roa_percentile:.0f}º</p>
                            <p style="color: #a0aec0; font-size: 12px;">Mejor que el {roa_percentile:.0f}% del sector</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        roe_percentile = (all_metrics_df['ROE'] < latest_metrics['ROE']).mean() * 100
                        color = "#48bb78" if roe_percentile > 50 else "#ff3366"
                        st.markdown(f"""
                        <div class="custom-card">
                            <h4 style="color: {color};">Percentil ROE</h4>
                            <p style="font-size: 28px; font-weight: 700; color: white;">{roe_percentile:.0f}º</p>
                            <p style="color: #a0aec0; font-size: 12px;">Mejor que el {roe_percentile:.0f}% del sector</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col3:
                        eff_percentile = (all_metrics_df['ratio_eficiencia'] > latest_metrics['ratio_eficiencia']).mean() * 100
                        color = "#48bb78" if eff_percentile > 50 else "#ff3366"
                        st.markdown(f"""
                        <div class="custom-card">
                            <h4 style="color: {color};">Percentil Eficiencia</h4>
                            <p style="font-size: 28px; font-weight: 700; color: white;">{eff_percentile:.0f}º</p>
                            <p style="color: #a0aec0; font-size: 12px;">Más eficiente que el {eff_percentile:.0f}%</p>
                        </div>
                        """, unsafe_allow_html=True)
            
            with tab4:
                st.markdown("### 🏆 Análisis Comparativo con Empresas Similares")
                
                if not comparison_data.empty:
                    # Preparar datos de comparación
                    peer_metrics = []
                    for comp in comparison_companies:
                        comp_metrics = calculate_quarterly_metrics(combined, comp)
                        if comp_metrics is not None and not comp_metrics.empty:
                            latest_comp = comp_metrics.iloc[-1]
                            peer_metrics.append({
                                'Empresa': comp,
                                'Tipo': latest_comp['tipo'],
                                'Ingresos': latest_comp['comisiones_percibidas'],
                                'Beneficio': latest_comp['resultados_antes_impuestos'],
                                'ROA': latest_comp['ROA'],
                                'ROE': latest_comp['ROE'],
                                'Eficiencia': latest_comp['ratio_eficiencia']
                            })
                    
                    # Añadir empresa seleccionada
                    peer_metrics.append({
                        'Empresa': selected_company,
                        'Tipo': latest['tipo'],
                        'Ingresos': latest['comisiones_percibidas'],
                        'Beneficio': latest['resultados_antes_impuestos'],
                        'ROA': latest['ROA'],
                        'ROE': latest['ROE'],
                        'Eficiencia': latest['ratio_eficiencia']
                    })
                    
                    peer_df = pd.DataFrame(peer_metrics)
                    
                    # Gráfico radar para comparación
                    categories_radar = ['Ingresos', 'Beneficio', 'ROA', 'ROE', '100-Eficiencia']
                    
                    fig_radar = go.Figure()
                    
                    # Normalizar datos para gráfico radar
                    peer_df_norm = peer_df.copy()
                    for col in ['Ingresos', 'Beneficio', 'ROA', 'ROE']:
                        max_val = peer_df[col].max()
                        if max_val > 0:
                            peer_df_norm[col] = peer_df[col] / max_val * 100
                    peer_df_norm['100-Eficiencia'] = 100 - peer_df['Eficiencia']
                    
                    # Añadir trazos para cada empresa
                    colors = ['#00d4ff', '#b794f6', '#f687b3', '#4299e1', '#48bb78']
                    for idx, row in peer_df_norm.iterrows():
                        if row['Empresa'] == selected_company:
                            line_width = 4
                            opacity = 1
                            fill = 'toself'
                        else:
                            line_width = 2
                            opacity = 0.6
                            fill = None
                        
                        fig_radar.add_trace(go.Scatterpolar(
                            r=[row['Ingresos'], row['Beneficio'], row['ROA'], row['ROE'], row['100-Eficiencia']],
                            theta=categories_radar,
                            fill=fill,
                            name=row['Empresa'][:25],
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
                        **professional_theme['layout'],
                        height=500,
                        title="Comparación Multidimensional (Normalizado)"
                    )
                    
                    st.plotly_chart(fig_radar, use_container_width=True)
                    
                    # Tabla de ranking
                    st.markdown("### 📊 Tabla de Ranking")
                    
                    peer_df_display = peer_df.round(2)
                    peer_df_display = peer_df_display.sort_values('ROE', ascending=False)
                    
                    # Resaltar empresa seleccionada
                    def highlight_selected(row):
                        if row['Empresa'] == selected_company:
                            return ['background-color: rgba(0, 212, 255, 0.2)'] * len(row)
                        return [''] * len(row)
                    
                    st.dataframe(
                        peer_df_display.style.apply(highlight_selected, axis=1)
                                            .background_gradient(cmap='RdYlGn', subset=['ROA', 'ROE'])
                                            .background_gradient(cmap='RdYlGn_r', subset=['Eficiencia']),
                        use_container_width=True
                    )
            
            with tab5:
                if show_comparison:
                    st.markdown("### ⚖️ Comparación entre Sociedades y Agencias de Valores")
                    
                    # Separar datos por tipo
                    sociedades_data = combined[combined['tipo'] == 'Sociedad']
                    agencias_data = combined[combined['tipo'] == 'Agencia']
                    
                    # Calcular métricas promedio por tipo y período
                    sociedades_avg = sociedades_data.groupby('periodo').agg({
                        'comisiones_percibidas': 'mean',
                        'resultados_antes_impuestos': 'mean',
                        'activos_totales': 'mean',
                        'fondos_propios': 'mean',
                        'gastos_explotacion': 'mean',
                        'margen_bruto': 'mean'
                    }).round(0)
                    
                    agencias_avg = agencias_data.groupby('periodo').agg({
                        'comisiones_percibidas': 'mean',
                        'resultados_antes_impuestos': 'mean',
                        'activos_totales': 'mean',
                        'fondos_propios': 'mean',
                        'gastos_explotacion': 'mean',
                        'margen_bruto': 'mean'
                    }).round(0)
                    
                    # Gráfico comparativo
                    fig_comp = make_subplots(
                        rows=2, cols=2,
                        subplot_titles=("Ingresos Promedio por Tipo", "Rentabilidad Promedio", 
                                       "Tamaño Promedio (Activos)", "Eficiencia Operativa"),
                        vertical_spacing=0.12,
                        horizontal_spacing=0.10
                    )
                    
                    # Ingresos promedio
                    fig_comp.add_trace(
                        go.Scatter(x=sociedades_avg.index, y=sociedades_avg['comisiones_percibidas'],
                                  name='Sociedades', line=dict(color='#b794f6', width=3),
                                  mode='lines+markers', marker=dict(size=10)),
                        row=1, col=1
                    )
                    fig_comp.add_trace(
                        go.Scatter(x=agencias_avg.index, y=agencias_avg['comisiones_percibidas'],
                                  name='Agencias', line=dict(color='#00d4ff', width=3),
                                  mode='lines+markers', marker=dict(size=10)),
                        row=1, col=1
                    )
                    
                    # Rentabilidad
                    fig_comp.add_trace(
                        go.Bar(x=sociedades_avg.index, y=sociedades_avg['resultados_antes_impuestos'],
                              name='Sociedades', marker_color='#b794f6', opacity=0.7),
                        row=1, col=2
                    )
                    fig_comp.add_trace(
                        go.Bar(x=agencias_avg.index, y=agencias_avg['resultados_antes_impuestos'],
                              name='Agencias', marker_color='#00d4ff', opacity=0.7),
                        row=1, col=2
                    )
                    
                    # Activos
                    fig_comp.add_trace(
                        go.Scatter(x=sociedades_avg.index, y=sociedades_avg['activos_totales'],
                                  name='Sociedades', line=dict(color='#b794f6', width=3),
                                  mode='lines+markers', fill='tonexty'),
                        row=2, col=1
                    )
                    fig_comp.add_trace(
                        go.Scatter(x=agencias_avg.index, y=agencias_avg['activos_totales'],
                                  name='Agencias', line=dict(color='#00d4ff', width=3),
                                  mode='lines+markers', fill='tozeroy'),
                        row=2, col=1
                    )
                    
                    # Eficiencia (ratio gastos/ingresos)
                    sociedades_avg['eficiencia'] = (sociedades_avg['gastos_explotacion'] / 
                                                   sociedades_avg['margen_bruto'] * 100)
                    agencias_avg['eficiencia'] = (agencias_avg['gastos_explotacion'] / 
                                                 agencias_avg['margen_bruto'] * 100)
                    
                    fig_comp.add_trace(
                        go.Bar(x=sociedades_avg.index, y=sociedades_avg['eficiencia'],
                              name='Sociedades', marker_color='#b794f6', opacity=0.7),
                        row=2, col=2
                    )
                    fig_comp.add_trace(
                        go.Bar(x=agencias_avg.index, y=agencias_avg['eficiencia'],
                              name='Agencias', marker_color='#00d4ff', opacity=0.7),
                        row=2, col=2
                    )
                    
                    fig_comp.update_layout(**professional_theme['layout'], height=700, showlegend=True)
                    fig_comp.update_yaxes(title_text="Comisiones (€K)", row=1, col=1)
                    fig_comp.update_yaxes(title_text="RAI (€K)", row=1, col=2)
                    fig_comp.update_yaxes(title_text="Activos (€K)", row=2, col=1)
                    fig_comp.update_yaxes(title_text="Ratio (%)", row=2, col=2)
                    
                    st.plotly_chart(fig_comp, use_container_width=True)
                    
                    # Estadísticas comparativas
                    st.markdown("### 📊 Estadísticas Comparativas: Sociedades vs Agencias")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("##### 📈 Sociedades de Valores")
                        esi_stats = {
                            'Número de Entidades': sociedades_data['entidad'].nunique(),
                            'Comisiones Promedio': f"€{sociedades_data['comisiones_percibidas'].mean():,.0f}K",
                            'Activos Promedio': f"€{sociedades_data['activos_totales'].mean():,.0f}K",
                            'ROE Promedio': f"{(sociedades_data['resultados_antes_impuestos'].sum() / sociedades_data['fondos_propios'].sum() * 100):.1f}%",
                            'Ratio Eficiencia': f"{(sociedades_data['gastos_explotacion'].sum() / sociedades_data['margen_bruto'].sum() * 100):.1f}%"
                        }
                        for key, value in esi_stats.items():
                            st.markdown(f"**{key}:** {value}")
                    
                    with col2:
                        st.markdown("##### 🏢 Agencias de Valores")
                        av_stats = {
                            'Número de Entidades': agencias_data['entidad'].nunique(),
                            'Comisiones Promedio': f"€{agencias_data['comisiones_percibidas'].mean():,.0f}K",
                            'Activos Promedio': f"€{agencias_data['activos_totales'].mean():,.0f}K",
                            'ROE Promedio': f"{(agencias_data['resultados_antes_impuestos'].sum() / agencias_data['fondos_propios'].sum() * 100):.1f}%",
                            'Ratio Eficiencia': f"{(agencias_data['gastos_explotacion'].sum() / agencias_data['margen_bruto'].sum() * 100):.1f}%"
                        }
                        for key, value in av_stats.items():
                            st.markdown(f"**{key}:** {value}")
            
            with tab6:
                st.markdown("### 📉 Evaluación de Salud Financiera")
                
                # Calcular componentes de salud
                health_metrics = {
                    'Rentabilidad': min(100, (latest['ROE'] / 20 * 100)),
                    'Calidad Activos': min(100, (latest['ROA'] / 10 * 100)),
                    'Eficiencia Operativa': max(0, (100 - latest['ratio_eficiencia'])),
                    'Momentum Crecimiento': min(100, max(0, latest['var_ingresos'] + 50)) if len(quarterly_metrics) > 1 else 50,
                    'Salud Apalancamiento': min(100, 100 / latest['apalancamiento']) if latest['apalancamiento'] > 0 else 100
                }
                
                # Puntuación general de salud
                overall_health = sum(health_metrics.values()) / len(health_metrics)
                
                # Indicador de salud
                fig_health = go.Figure(go.Indicator(
                    mode = "gauge+number+delta",
                    value = overall_health,
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "Puntuación de Salud Financiera", 'font': {'size': 20, 'color': 'white'}},
                    delta = {'reference': 70, 'increasing': {'color': "#48bb78"}},
                    gauge = {
                        'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "white"},
                        'bar': {'color': "#00d4ff"},
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
                
                fig_health.update_layout(**professional_theme['layout'], height=400)
                st.plotly_chart(fig_health, use_container_width=True)
                
                # Componentes de salud
                st.markdown("### 🎯 Componentes de la Puntuación")
                
                cols = st.columns(5)
                for idx, (component, score) in enumerate(health_metrics.items()):
                    with cols[idx]:
                        color = "#48bb78" if score >= 70 else "#ed8936" if score >= 40 else "#ff3366"
                        st.markdown(f"""
                        <div class="custom-card" style="text-align: center;">
                            <h5 style="color: {color}; font-size: 13px; margin-bottom: 10px;">{component}</h5>
                            <p style="font-size: 24px; font-weight: 700; color: white; margin: 0;">{score:.0f}</p>
                            <div style="background: rgba(255, 255, 255, 0.1); border-radius: 8px; height: 6px; margin-top: 10px;">
                                <div style="background: {color}; border-radius: 8px; height: 6px; width: {score}%;"></div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
        
        # Opciones de exportación
        st.divider()
        st.markdown("### 💾 Opciones de Exportación")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Exportar métricas trimestrales
            csv = quarterly_metrics.to_csv(index=False)
            st.download_button(
                label="📊 Descargar Métricas Trimestrales",
                data=csv,
                file_name=f"{selected_company.replace(' ', '_')}_metricas_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col2:
            # Generar resumen ejecutivo
            tipo_label = "Sociedad de Valores" if company_type == "Sociedad" else "Agencia de Valores"
            summary = f"""
INFORME EJECUTIVO - {selected_company}
Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}
Elaborado por: @Gsnchez | bquantfinance.com

INFORMACIÓN DE LA ENTIDAD
=========================
Nombre: {selected_company}
Tipo: {tipo_label}
Trimestres Analizados: {len(quarterly_metrics)}

RESULTADOS ÚLTIMO TRIMESTRE ({latest['periodo']})
=================================================
Comisiones Percibidas: €{latest['comisiones_percibidas']:,.0f}K (Variación: {latest['var_ingresos']:.1f}%)
Resultado antes de Impuestos: €{latest['resultados_antes_impuestos']:,.0f}K (Variación: {latest['var_beneficio']:.1f}%)
Activos Totales: €{latest['activos_totales']:,.0f}K
Fondos Propios: €{latest['fondos_propios']:,.0f}K

INDICADORES FINANCIEROS CLAVE
=============================
Rentabilidad sobre Activos (ROA): {latest['ROA']:.2f}%
Rentabilidad sobre Patrimonio (ROE): {latest['ROE']:.2f}%
Ratio de Eficiencia: {latest['ratio_eficiencia']:.2f}%
Margen Neto: {latest['margen_neto']:.2f}%
Apalancamiento Financiero: {latest['apalancamiento']:.2f}x

EVALUACIÓN DE SALUD FINANCIERA
==============================
Puntuación Global: {overall_health:.1f}/100
Estado: {'Excelente' if overall_health >= 75 else 'Bueno' if overall_health >= 50 else 'Regular' if overall_health >= 25 else 'Requiere Mejora'}

MÉTRICAS DE CRECIMIENTO
======================
Crecimiento Promedio Trimestral: {quarterly_metrics['var_ingresos'][1:].mean():.1f}% (en comisiones)
Volatilidad del Crecimiento: {quarterly_metrics['var_ingresos'][1:].std():.1f}%
Crecimiento Total del Período: {((latest['comisiones_percibidas'] / quarterly_metrics.iloc[0]['comisiones_percibidas'] - 1) * 100):.1f}%
            """
            
            st.download_button(
                label="📄 Descargar Resumen Ejecutivo",
                data=summary,
                file_name=f"{selected_company.replace(' ', '_')}_resumen_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain",
                use_container_width=True
            )
        
        with col3:
            # Exportar todos los datos
            all_data = company_data.to_csv(index=False)
            st.download_button(
                label="📁 Descargar Datos Completos",
                data=all_data,
                file_name=f"{selected_company.replace(' ', '_')}_datos_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )
    
    # Pie de página
    st.divider()
    st.markdown("""
        <div style='text-align: center; padding: 30px 20px; background: linear-gradient(135deg, rgba(255, 255, 255, 0.03) 0%, rgba(255, 255, 255, 0.01) 100%); 
                    border-radius: 16px; border: 1px solid rgba(255, 255, 255, 0.1); margin-top: 30px;'>
            <p style='color: #00d4ff; font-size: 16px; font-weight: 600; margin-bottom: 8px;'>Panel de Análisis Financiero v2.0</p>
            <p style='color: #a0aec0; font-size: 13px; margin-bottom: 16px;'>Análisis Profesional para Sociedades y Agencias de Valores</p>
            <p style='color: white; font-size: 14px;'>Desarrollado por <strong style='color: #b794f6;'>@Gsnchez</strong></p>
            <p style='color: #4a5568; font-size: 11px; margin-top: 8px;'>bquantfinance.com | Soluciones Financieras Profesionales</p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
