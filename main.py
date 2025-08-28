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
        --accent-cyan: #00d4ff;
        --accent-purple: #b794f6;
        --accent-pink: #f687b3;
        --accent-blue: #4299e1;
        --accent-green: #48bb78;
        --text-primary: #ffffff;
        --text-secondary: #a0aec0;
        --border-color: rgba(255, 255, 255, 0.1);
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
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(0, 212, 255, 0.15) 0%, rgba(183, 148, 246, 0.15) 100%);
        color: var(--text-primary);
        border: 1px solid rgba(0, 212, 255, 0.3);
    }
    
    /* Botones de descarga */
    .stDownloadButton > button {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: var(--accent-cyan);
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
    
    /* Badges de tipo */
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
        try:
            sociedades = pd.read_excel('./sociedades_estructurado.xlsx')
            agencias = pd.read_excel('./agencias_estructurado.xlsx')
        except:
            st.error("No se encontraron los archivos de datos.")
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
            'tickfont': {'color': '#a0aec0'}
        },
        'yaxis': {
            'gridcolor': 'rgba(255, 255, 255, 0.05)',
            'linecolor': 'rgba(255, 255, 255, 0.1)',
            'tickfont': {'color': '#a0aec0'}
        },
        'colorway': ['#00d4ff', '#b794f6', '#f687b3', '#4299e1', '#48bb78', '#ed8936'],
        'hovermode': 'x unified'
    }
}

# Aplicación principal
def main():
    # Encabezado
    st.markdown('<h1 class="main-header">Panel de Análisis Financiero</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Sociedades de Valores y Agencias de Valores - Análisis Trimestral</p>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #4a5568; font-size: 12px; margin-bottom: 30px;">Desarrollado por @Gsnchez | bquantfinance.com</p>', unsafe_allow_html=True)
    
    # Cargar datos directamente
    with st.spinner('Cargando datos financieros...'):
        try:
            sociedades, agencias, combined = load_data()
            
            # Mostrar información de datos cargados
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(label="📊 Total Registros", value=f"{len(combined):,}")
            with col2:
                st.metric(label="🏢 Sociedades", value=f"{sociedades['entidad'].nunique()}")
            with col3:
                st.metric(label="🏦 Agencias", value=f"{agencias['entidad'].nunique()}")
            
        except Exception as e:
            st.error(f"Error al cargar los datos: {str(e)}")
            st.stop()
    
    # Configuración en barra lateral
    with st.sidebar:
        st.markdown("## ⚙️ Panel de Control")
        
        # Selector de empresa principal
        st.markdown("### 🏢 Selección de Empresa")
        
        # Filtro por tipo
        tipo_filtro = st.radio(
            "Filtrar por tipo:",
            ["📊 Todas", "📈 Sociedades", "🏦 Agencias"],
            horizontal=True
        )
        
        # Filtrar entidades según selección
        if tipo_filtro == "📈 Sociedades":
            filtered_combined = combined[combined['tipo'] == 'Sociedad']
        elif tipo_filtro == "🏦 Agencias":
            filtered_combined = combined[combined['tipo'] == 'Agencia']
        else:
            filtered_combined = combined
        
        all_entities = sorted(filtered_combined['entidad'].unique())
        
        # Empresa principal
        selected_company = st.selectbox(
            "Empresa a analizar:",
            all_entities,
            index=0 if len(all_entities) > 0 else None
        )
        
        # Obtener tipo de la empresa seleccionada
        if selected_company:
            company_type = filtered_combined[filtered_combined['entidad'] == selected_company]['tipo'].iloc[0]
        else:
            company_type = None
        
        st.divider()
        
        # Selector de período simplificado
        st.markdown("### 📅 Período")
        available_periods = sorted(combined['periodo'].unique())
        
        period_option = st.radio(
            "Seleccionar período:",
            ["📌 Último trimestre", "📊 Todos los trimestres", "🔧 Personalizado"]
        )
        
        if period_option == "📌 Último trimestre":
            selected_periods = [available_periods[-1]] if available_periods else []
        elif period_option == "📊 Todos los trimestres":
            selected_periods = available_periods
        else:
            selected_periods = st.multiselect(
                "Trimestres:",
                available_periods,
                default=available_periods[-2:] if len(available_periods) >= 2 else available_periods
            )
        
        st.divider()
        
        # Comparación simplificada
        st.markdown("### 🔄 Comparación")
        enable_comparison = st.checkbox("Activar comparación", value=False)
        
        comparison_companies = []
        if enable_comparison and company_type and selected_company:
            comparison_entities = list(filtered_combined[
                (filtered_combined['tipo'] == company_type) & 
                (filtered_combined['entidad'] != selected_company)
            ]['entidad'].unique())
            
            if len(comparison_entities) > 0:
                comparison_mode = st.radio(
                    "Modo:",
                    ["Top 3 similares", "Selección manual"]
                )
                
                if comparison_mode == "Top 3 similares":
                    # Seleccionar los 3 más similares en tamaño
                    company_size = filtered_combined[
                        filtered_combined['entidad'] == selected_company
                    ]['activos_totales'].mean()
                    
                    sizes = filtered_combined[
                        filtered_combined['entidad'].isin(comparison_entities)
                    ].groupby('entidad')['activos_totales'].mean().reset_index()
                    
                    sizes['diff'] = abs(sizes['activos_totales'] - company_size)
                    top3 = sizes.nsmallest(3, 'diff')['entidad'].tolist()
                    comparison_companies = top3
                else:
                    comparison_companies = st.multiselect(
                        "Seleccionar empresas:",
                        comparison_entities,
                        max_selections=5
                    )
        
        # Resumen
        st.divider()
        st.markdown("### 📊 Resumen")
        st.info(f"""
        **Empresa:** {selected_company if selected_company else 'No seleccionada'}
        **Tipo:** {company_type if company_type else '-'}
        **Períodos:** {len(selected_periods)}
        **Comparando:** {len(comparison_companies)} empresas
        """)
    
    # Filtrar datos
    company_data = combined[
        (combined['entidad'] == selected_company) & 
        (combined['periodo'].isin(selected_periods))
    ].sort_values('fecha')
    
    comparison_data = combined[
        (combined['entidad'].isin(comparison_companies)) & 
        (combined['periodo'].isin(selected_periods))
    ]
    
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
                    delta=f"{latest['var_ingresos']:.1f}% vs trim. anterior" if len(quarterly_metrics) > 1 else None
                )
            
            with col2:
                st.metric(
                    label="📊 Resultado antes Impuestos",
                    value=f"€{latest['resultados_antes_impuestos']:,.0f}K",
                    delta=f"{latest['var_beneficio']:.1f}% vs trim. anterior" if len(quarterly_metrics) > 1 else None
                )
            
            with col3:
                st.metric(
                    label="📈 ROE",
                    value=f"{latest['ROE']:.1f}%",
                    delta=f"{latest['ROE'] - prev['ROE']:.1f}pp" if len(quarterly_metrics) > 1 else None
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
                
                # Gráficos...
                fig.add_trace(
                    go.Bar(x=quarterly_metrics['periodo'], y=quarterly_metrics['comisiones_percibidas'],
                          name='Comisiones', marker_color='#00d4ff', opacity=0.7),
                    row=1, col=1, secondary_y=False
                )
                fig.add_trace(
                    go.Scatter(x=quarterly_metrics['periodo'], y=quarterly_metrics['resultados_antes_impuestos'],
                              name='Beneficio', line=dict(color='#f687b3', width=3),
                              mode='lines+markers'),
                    row=1, col=1, secondary_y=True
                )
                
                fig.update_layout(**professional_theme['layout'], height=700, showlegend=True)
                st.plotly_chart(fig, use_container_width=True)
            
            with tab2:
                st.markdown("### 📈 Análisis de Crecimiento")
                st.info("Análisis de tendencias y crecimiento trimestral")
            
            with tab3:
                st.markdown("### ⚡ Métricas de Eficiencia")
                st.info("ROA, ROE y ratios de eficiencia operativa")
            
            with tab4:
                st.markdown("### 🏆 Comparación con Competidores")
                if comparison_companies:
                    st.info(f"Comparando con {len(comparison_companies)} empresas del mismo tipo")
                else:
                    st.warning("Active la comparación en el panel lateral")
            
            with tab5:
                st.markdown("### ⚖️ Comparación entre Sociedades y Agencias de Valores")
                
                # Separar datos por tipo
                sociedades_data = combined[combined['tipo'] == 'Sociedad']
                agencias_data = combined[combined['tipo'] == 'Agencia']
                
                if len(sociedades_data) > 0 and len(agencias_data) > 0:
                    # Estadísticas comparativas
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("##### 📈 Sociedades de Valores")
                        st.metric("Número de Entidades", sociedades_data['entidad'].nunique())
                        st.metric("Comisiones Promedio", f"€{sociedades_data['comisiones_percibidas'].mean():,.0f}K")
                        st.metric("Activos Promedio", f"€{sociedades_data['activos_totales'].mean():,.0f}K")
                    
                    with col2:
                        st.markdown("##### 🏦 Agencias de Valores")
                        st.metric("Número de Entidades", agencias_data['entidad'].nunique())
                        st.metric("Comisiones Promedio", f"€{agencias_data['comisiones_percibidas'].mean():,.0f}K")
                        st.metric("Activos Promedio", f"€{agencias_data['activos_totales'].mean():,.0f}K")
                else:
                    st.warning("No hay suficientes datos para comparar")
            
            with tab6:
                st.markdown("### 📉 Evaluación de Salud Financiera")
                
                # Calcular componentes de salud
                health_score = min(100, (
                    (latest['ROE'] / 20 * 100) * 0.3 +
                    (latest['ROA'] / 10 * 100) * 0.3 +
                    (100 - latest['ratio_eficiencia']) * 0.4
                ))
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Puntuación Global", f"{health_score:.0f}/100")
                with col2:
                    st.metric("ROA", f"{latest['ROA']:.1f}%")
                with col3:
                    st.metric("ROE", f"{latest['ROE']:.1f}%")
        
        # Opciones de exportación
        st.divider()
        st.markdown("### 💾 Opciones de Exportación")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            csv = quarterly_metrics.to_csv(index=False) if quarterly_metrics is not None else ""
            st.download_button(
                label="📊 Descargar Métricas Trimestrales",
                data=csv,
                file_name=f"{selected_company}_metricas_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        
        with col2:
            st.download_button(
                label="📄 Descargar Resumen Ejecutivo",
                data="Resumen ejecutivo",
                file_name=f"{selected_company}_resumen_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain"
            )
        
        with col3:
            st.download_button(
                label="📁 Descargar Datos Completos",
                data=company_data.to_csv(index=False),
                file_name=f"{selected_company}_datos_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
    
    # Pie de página
    st.divider()
    st.markdown("""
        <div style='text-align: center; padding: 20px;'>
            <p style='color: #00d4ff; font-size: 14px;'>Panel de Análisis Financiero v2.0</p>
            <p style='color: #a0aec0; font-size: 12px;'>Desarrollado por @Gsnchez | bquantfinance.com</p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
