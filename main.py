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

# Professional CSS styling (unchanged)
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

# Function to clean and standardize entity names
def clean_entity_name(name):
    """Clean and standardize entity names to avoid duplicates"""
    if pd.isna(name):
        return None
    # Convert to string and strip spaces
    name = str(name).strip()
    # Remove multiple spaces
    name = ' '.join(name.split())
    # Standardize common abbreviations
    name = name.replace('S.V.', 'S.V.')
    name = name.replace('A.V.', 'A.V.')
    name = name.replace('S.A.', 'S.A.')
    # Remove trailing dots and commas
    name = name.rstrip('.,')
    return name

# Function to detect and merge duplicate entities
def merge_duplicate_entities(df):
    """Detect and merge entities that are likely duplicates"""
    if df.empty:
        return df
    
    # Group entities and calculate their data quality
    entity_quality = df.groupby('entidad').agg({
        'comisiones_percibidas': ['sum', 'count', 'max'],
        'activos_totales': ['sum', 'max'],
        'fondos_propios': ['sum', 'max']
    }).reset_index()
    
    # Flatten column names
    entity_quality.columns = ['entidad'] + ['_'.join(col).strip() if col[0] != 'entidad' else col for col in entity_quality.columns[1:]]
    
    # Calculate a quality score
    entity_quality['quality_score'] = (
        (entity_quality['comisiones_percibidas_sum'].abs() > 0).astype(int) * 10 +
        (entity_quality['activos_totales_sum'] > 0).astype(int) * 5 +
        entity_quality['comisiones_percibidas_count'] * 2
    )
    
    # Sort by entity name to group similar names together
    entity_quality = entity_quality.sort_values('entidad')
    
    # Dictionary to map duplicates to the best version
    entity_mapping = {}
    processed = set()
    
    entities = entity_quality['entidad'].tolist()
    
    for i, entity1 in enumerate(entities):
        if entity1 in processed:
            continue
            
        # Check for potential duplicates
        potential_duplicates = []
        entity1_upper = entity1.upper().replace('.', '').replace(',', '').replace(' ', '')
        
        for j, entity2 in enumerate(entities):
            if i == j or entity2 in processed:
                continue
                
            entity2_upper = entity2.upper().replace('.', '').replace(',', '').replace(' ', '')
            
            # Check if one is contained in the other or they're very similar
            if (entity1_upper in entity2_upper or 
                entity2_upper in entity1_upper or
                entity1_upper.startswith(entity2_upper[:min(10, len(entity2_upper))]) or
                entity2_upper.startswith(entity1_upper[:min(10, len(entity1_upper))])):
                
                potential_duplicates.append(entity2)
        
        if potential_duplicates:
            # Include the original entity in the list
            all_versions = [entity1] + potential_duplicates
            
            # Get quality scores for all versions
            versions_with_scores = []
            for version in all_versions:
                score = entity_quality[entity_quality['entidad'] == version]['quality_score'].values
                if len(score) > 0:
                    versions_with_scores.append((version, score[0]))
            
            # Sort by quality score (descending) and then by name length (longer is usually more complete)
            versions_with_scores.sort(key=lambda x: (-x[1], -len(x[0])))
            
            # The best version is the one with highest score
            best_version = versions_with_scores[0][0]
            
            # Map all versions to the best one
            for version, _ in versions_with_scores:
                if version != best_version:
                    entity_mapping[version] = best_version
                processed.add(version)
    
    # Apply the mapping
    if entity_mapping:
        df['entidad'] = df['entidad'].replace(entity_mapping)
    
    # After merging names, consolidate the data
    # For duplicate entity-period combinations, keep the row with most data
    df['data_completeness'] = (
        (df['comisiones_percibidas'].abs() > 0).astype(int) * 3 +
        (df['activos_totales'] > 0).astype(int) * 2 +
        (df['fondos_propios'] != 0).astype(int)
    )
    
    df = df.sort_values(['entidad', 'periodo', 'data_completeness'], ascending=[True, True, False])
    df = df.drop_duplicates(subset=['entidad', 'periodo'], keep='first')
    df = df.drop('data_completeness', axis=1)
    
    return df

# Function to convert YTD (Year-to-Date) accumulated data to quarterly
def accumulated_to_quarterly(df):
    """Convert YTD accumulated data to quarterly data
    
    The data comes in YTD format:
    - MARZO: Q1 data (3 months: Jan-Mar)
    - JUNIO: YTD through Q2 (6 months: Jan-Jun)
    - SEPTIEMBRE: YTD through Q3 (9 months: Jan-Sep)
    - DICIEMBRE: YTD through Q4 (12 months: Jan-Dec)
    
    We need to convert to individual quarterly data.
    """
    # First, clean entity names
    df['Denominación'] = df['Denominación'].apply(clean_entity_name)
    
    # Remove rows where entity name is None
    df = df[df['Denominación'].notna()]
    
    df = df.sort_values(['Denominación', 'Año', 'Fecha'])
    
    quarterly_data = []
    
    for entity in df['Denominación'].unique():
        if not entity:  # Skip empty entity names
            continue
            
        entity_data = df[df['Denominación'] == entity].copy()
        
        for year in entity_data['Año'].unique():
            year_data = entity_data[entity_data['Año'] == year].sort_values('Fecha')
            
            if len(year_data) == 0:
                continue
            
            # Income statement columns that are accumulated YTD (need conversion)
            ytd_cols = [
                'Comisiones_Percibidas_Miles_EUR',
                'Comisiones_Netas_Miles_EUR',
                'Margen_Bruto_Miles_EUR',
                'Gastos_Explotación_Miles_EUR',
                'Resultados_Antes_Impuestos_Miles_EUR'
            ]
            
            # Balance sheet columns (point-in-time, not accumulated)
            balance_cols = [
                'Fondos_Propios_Miles_EUR',
                'Activos_Totales_Miles_EUR'
            ]
            
            # Create a dictionary to store YTD values by month for easy access
            ytd_values = {}
            for _, row in year_data.iterrows():
                ytd_values[row['Mes']] = row
            
            # Process each quarter
            for mes in ['MARZO', 'JUNIO', 'SEPTIEMBRE', 'DICIEMBRE']:
                if mes not in ytd_values:
                    continue
                    
                row = ytd_values[mes]
                quarterly_row = row.copy()
                
                # Determine quarter and calculate quarterly values
                if mes == 'MARZO':
                    quarter = 'Q1'
                    # Q1 values are already quarterly (first 3 months)
                    for col in ytd_cols:
                        quarterly_row[col] = row[col]
                        
                elif mes == 'JUNIO':
                    quarter = 'Q2'
                    # Q2 = YTD June (6 months) - YTD March (3 months)
                    if 'MARZO' in ytd_values:
                        for col in ytd_cols:
                            quarterly_row[col] = row[col] - ytd_values['MARZO'][col]
                    else:
                        # If no March data, June YTD represents Q1+Q2
                        # We can't accurately separate, so we'll use half as estimate
                        for col in ytd_cols:
                            quarterly_row[col] = row[col] / 2
                            
                elif mes == 'SEPTIEMBRE':
                    quarter = 'Q3'
                    # Q3 = YTD September (9 months) - YTD June (6 months)
                    if 'JUNIO' in ytd_values:
                        for col in ytd_cols:
                            quarterly_row[col] = row[col] - ytd_values['JUNIO'][col]
                    else:
                        # Fallback: estimate Q3 as 1/3 of YTD September
                        for col in ytd_cols:
                            quarterly_row[col] = row[col] / 3
                            
                elif mes == 'DICIEMBRE':
                    quarter = 'Q4'
                    # Q4 = YTD December (12 months) - YTD September (9 months)
                    if 'SEPTIEMBRE' in ytd_values:
                        for col in ytd_cols:
                            quarterly_row[col] = row[col] - ytd_values['SEPTIEMBRE'][col]
                    elif 'JUNIO' in ytd_values:
                        # If no September, use June: Q4+Q3 = Dec - June
                        for col in ytd_cols:
                            quarterly_row[col] = (row[col] - ytd_values['JUNIO'][col]) / 2
                    elif 'MARZO' in ytd_values:
                        # If only March available: Q4+Q3+Q2 = Dec - March
                        for col in ytd_cols:
                            quarterly_row[col] = (row[col] - ytd_values['MARZO'][col]) / 3
                    else:
                        # Only December data: estimate Q4 as 1/4 of total
                        for col in ytd_cols:
                            quarterly_row[col] = row[col] / 4
                
                # Balance sheet items remain as-is (point in time values)
                for col in balance_cols:
                    quarterly_row[col] = row[col]
                
                quarterly_row['Quarter'] = quarter
                quarterly_row['Periodo_Quarterly'] = f"{year} {quarter}"
                quarterly_data.append(quarterly_row)
    
    return pd.DataFrame(quarterly_data)

# Function to load and process data
@st.cache_data
def load_data():
    try:
        # Load the new files with updated names
        sociedades_raw = pd.read_excel('sociedades_de_valores_parsed.xlsx')
        agencias_raw = pd.read_excel('agencias_de_valores_parsed.xlsx')
    except FileNotFoundError:
        try:
            sociedades_raw = pd.read_excel('./sociedades_de_valores_parsed.xlsx')
            agencias_raw = pd.read_excel('./agencias_de_valores_parsed.xlsx')
        except:
            st.error("No se encontraron los archivos de datos.")
            st.stop()
    
    # Convert accumulated data to quarterly
    sociedades = accumulated_to_quarterly(sociedades_raw)
    agencias = accumulated_to_quarterly(agencias_raw)
    
    # Rename columns to match the original app structure
    column_mapping = {
        'Denominación': 'entidad',
        'Fondos_Propios_Miles_EUR': 'fondos_propios',
        'Activos_Totales_Miles_EUR': 'activos_totales',
        'Comisiones_Percibidas_Miles_EUR': 'comisiones_percibidas',
        'Comisiones_Netas_Miles_EUR': 'comisiones_netas',
        'Margen_Bruto_Miles_EUR': 'margen_bruto',
        'Gastos_Explotación_Miles_EUR': 'gastos_explotacion',
        'Resultados_Antes_Impuestos_Miles_EUR': 'resultados_antes_impuestos',
        'Fecha': 'fecha',
        'Periodo_Quarterly': 'periodo'
    }
    
    sociedades = sociedades.rename(columns=column_mapping)
    agencias = agencias.rename(columns=column_mapping)
    
    # Clean entity names to avoid variations
    sociedades['entidad'] = sociedades['entidad'].apply(clean_entity_name)
    agencias['entidad'] = agencias['entidad'].apply(clean_entity_name)
    
    # Remove rows with null entity names
    sociedades = sociedades[sociedades['entidad'].notna()]
    agencias = agencias[agencias['entidad'].notna()]
    
    # Function to consolidate duplicate entities (keep the one with most data)
    def consolidate_duplicates(df):
        # Calculate a "data quality score" for each entity
        df['data_score'] = (
            (df['comisiones_percibidas'].abs() > 0).astype(int) * 3 +  # Revenue is most important
            (df['activos_totales'].abs() > 0).astype(int) * 2 +
            (df['fondos_propios'].abs() > 0).astype(int) +
            (df['resultados_antes_impuestos'].notna()).astype(int)
        )
        
        # For each entity-period combination, keep only the row with highest data score
        df = df.sort_values(['entidad', 'periodo', 'data_score'], ascending=[True, True, False])
        df = df.drop_duplicates(subset=['entidad', 'periodo'], keep='first')
        df = df.drop('data_score', axis=1)
        
        return df
    
    # Consolidate duplicates
    sociedades = consolidate_duplicates(sociedades)
    agencias = consolidate_duplicates(agencias)
    
    # Filter out entities with no meaningful data
    def filter_empty_entities(df):
        # Group by entity and check if they have any real activity
        entity_stats = df.groupby('entidad').agg({
            'comisiones_percibidas': ['sum', 'max', 'mean', 'count'],
            'activos_totales': ['sum', 'max', 'mean'],
            'fondos_propios': ['sum', 'max', 'mean'],
            'resultados_antes_impuestos': ['sum', 'count']
        })
        
        # Flatten column names
        entity_stats.columns = ['_'.join(col).strip() for col in entity_stats.columns.values]
        
        # Filter entities that have:
        # 1. Meaningful revenue at any point
        # 2. OR meaningful assets
        # 3. AND more than just one quarter of data
        # 4. AND not all zeros
        valid_entities = entity_stats[
            (
                (entity_stats['comisiones_percibidas_max'] > 10) |  # Has had at least 10K revenue
                (entity_stats['activos_totales_max'] > 100)         # Has at least 100K assets
            ) &
            (entity_stats['comisiones_percibidas_count'] >= 2) &    # At least 2 quarters
            (
                (entity_stats['comisiones_percibidas_sum'].abs() > 0) |
                (entity_stats['activos_totales_sum'] > 0) |
                (entity_stats['fondos_propios_sum'] != 0)
            )
        ]
        
        return df[df['entidad'].isin(valid_entities.index)]
    
    # Apply filtering
    sociedades = filter_empty_entities(sociedades)
    agencias = filter_empty_entities(agencias)
    
    # Merge duplicate entities (this handles variations like ACTIVOTRADE VALOR... and ACTIVOTRADE VALORES...)
    sociedades = merge_duplicate_entities(sociedades)
    agencias = merge_duplicate_entities(agencias)
    
    # Remove any remaining NaN or infinite values in key columns
    key_cols = ['comisiones_percibidas', 'activos_totales', 'fondos_propios', 
                'gastos_explotacion', 'resultados_antes_impuestos', 'margen_bruto', 'comisiones_netas']
    
    for col in key_cols:
        if col in sociedades.columns:
            sociedades[col] = sociedades[col].fillna(0)
            sociedades = sociedades[~sociedades[col].isin([float('inf'), float('-inf')])]
        if col in agencias.columns:
            agencias[col] = agencias[col].fillna(0)
            agencias = agencias[~agencias[col].isin([float('inf'), float('-inf')])]
    
    # Add type column
    sociedades['tipo'] = 'Sociedad'
    agencias['tipo'] = 'Agencia'
    
    # Ensure fecha is datetime
    sociedades['fecha'] = pd.to_datetime(sociedades['fecha'])
    agencias['fecha'] = pd.to_datetime(agencias['fecha'])
    
    # Combine datasets
    combined = pd.concat([sociedades, agencias], ignore_index=True)
    
    # Final check: remove any entity that appears with inconsistent type
    entity_types = combined.groupby('entidad')['tipo'].nunique()
    consistent_entities = entity_types[entity_types == 1].index
    combined = combined[combined['entidad'].isin(consistent_entities)]
    
    # Final duplicate check after combination
    combined = consolidate_duplicates(combined)
    
    return sociedades, agencias, combined

# Calculate quarterly metrics (same as original)
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
        
        # Calculate quarter-to-quarter changes
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

# Professional dark theme for plotly
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

# Main application
def main():
    # Header
    st.markdown('<h1 class="main-header">Panel de Análisis Financiero</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Sociedades de Valores y Agencias de Valores - Análisis Trimestral</p>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #4a5568; font-size: 12px; margin-bottom: 30px;">Desarrollado por @Gsnchez | bquantfinance.com</p>', unsafe_allow_html=True)
    
    # Load data
    with st.spinner('Cargando datos financieros...'):
        try:
            sociedades, agencias, combined = load_data()
            
            # Show loaded data info
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
    
    # Sidebar configuration
    with st.sidebar:
        st.markdown("### 🎯 Análisis de Empresa")
        
        # Type filter checkbox
        tipo_filter = st.checkbox("🔍 Filtrar por tipo", help="Filtrar empresas por tipo de entidad")
        
        # Show filter only if checkbox is selected
        if tipo_filter:
            tipo_filtro = st.radio(
                "Tipo de entidad:",
                ["Todas", "Sociedades", "Agencias"],
                horizontal=True,
                label_visibility="visible"
            )
            
            if tipo_filtro == "Sociedades":
                filtered_entities = sorted(combined[combined['tipo'] == 'Sociedad']['entidad'].unique())
            elif tipo_filtro == "Agencias":
                filtered_entities = sorted(combined[combined['tipo'] == 'Agencia']['entidad'].unique())
            else:
                filtered_entities = sorted(combined['entidad'].unique())
        else:
            filtered_entities = sorted(combined['entidad'].unique())
        
        # Company selector - now properly filtered
        selected_company = st.selectbox(
            "Empresa",
            filtered_entities,
            index=0 if len(filtered_entities) > 0 else None,
            label_visibility="collapsed"
        )
        
        # Get company type and show badge
        if selected_company:
            company_type = combined[combined['entidad'] == selected_company]['tipo'].iloc[0]
            if company_type == 'Sociedad':
                st.markdown(f"<span style='background: linear-gradient(135deg, #b794f6 0%, #9f7aea 100%); color: white; padding: 2px 8px; border-radius: 12px; font-size: 11px; font-weight: 600;'>SOCIEDAD DE VALORES</span>", unsafe_allow_html=True)
            else:
                st.markdown(f"<span style='background: linear-gradient(135deg, #00d4ff 0%, #0091ff 100%); color: white; padding: 2px 8px; border-radius: 12px; font-size: 11px; font-weight: 600;'>AGENCIA DE VALORES</span>", unsafe_allow_html=True)
        else:
            company_type = None
        
        st.markdown("---")
        
        # Period selector
        st.markdown("### 📅 Período de Análisis")
        available_periods = sorted(combined['periodo'].unique())
        
        period_mode = st.selectbox(
            "Seleccionar período",
            ["Último año (4 trim.)", "Último trimestre", "Todo el histórico", "Personalizado"],
            label_visibility="collapsed"
        )
        
        if period_mode == "Último año (4 trim.)":
            selected_periods = available_periods[-4:] if len(available_periods) >= 4 else available_periods
        elif period_mode == "Último trimestre":
            selected_periods = [available_periods[-1]] if available_periods else []
        elif period_mode == "Todo el histórico":
            selected_periods = available_periods
        else:  # Personalizado
            selected_periods = st.multiselect(
                "Seleccionar trimestres:",
                available_periods,
                default=available_periods[-4:] if len(available_periods) >= 4 else available_periods
            )
        
        st.caption(f"📊 {len(selected_periods)} trimestres seleccionados")
        
        st.markdown("---")
        
        # Comparison section - initialize comparison_companies first
        comparison_companies = []
        
        # Streamlined comparison with expander
        with st.expander("🔄 **Comparación con Competidores**", expanded=False):
            if company_type and selected_company:
                # Get entities of same type, excluding selected company
                same_type_entities = combined[
                    (combined['tipo'] == company_type) & 
                    (combined['entidad'] != selected_company)
                ]['entidad'].unique()
                
                if len(same_type_entities) > 0:
                    # Calculate similar companies by size
                    company_data = combined[combined['entidad'] == selected_company]
                    if not company_data.empty:
                        company_size = company_data['activos_totales'].mean()
                        
                        # Get size data for all companies of same type
                        size_data = []
                        for entity in same_type_entities:
                            entity_data = combined[combined['entidad'] == entity]
                            if not entity_data.empty:
                                avg_size = entity_data['activos_totales'].mean()
                                size_data.append({
                                    'entidad': entity,
                                    'size': avg_size,
                                    'diff': abs(avg_size - company_size)
                                })
                        
                        if size_data:
                            # Sort by similarity (smallest difference)
                            size_df = pd.DataFrame(size_data).sort_values('diff')
                            top3 = size_df.head(3)['entidad'].tolist()
                            
                            use_auto = st.checkbox("Usar Top 3 similares", value=True)
                            
                            if use_auto:
                                comparison_companies = top3
                                st.caption(f"Comparando con: {', '.join([c[:20] + '...' if len(c) > 20 else c for c in comparison_companies])}")
                            else:
                                comparison_companies = st.multiselect(
                                    "Seleccionar manualmente:",
                                    list(same_type_entities),
                                    max_selections=5
                                )
                        else:
                            st.warning("No hay suficientes datos para comparar")
                else:
                    st.warning("No hay otras empresas del mismo tipo")
            else:
                st.info("Selecciona una empresa para activar comparación")
        
        # Enable comparison flag
        enable_comparison = len(comparison_companies) > 0
        
        # Compact summary at bottom
        if selected_company:
            st.markdown("---")
            st.markdown(f"""
            <div style='background: rgba(255,255,255,0.05); padding: 10px; border-radius: 8px; font-size: 12px;'>
                <strong>{selected_company[:30]}{'...' if len(selected_company) > 30 else ''}</strong><br>
                <span style='color: #a0aec0;'>
                {len(selected_periods)} períodos | 
                {f'{len(comparison_companies)} competidores' if enable_comparison else 'Sin comparación'}
                </span>
            </div>
            """, unsafe_allow_html=True)
    
    # Filter data
    company_data = combined[
        (combined['entidad'] == selected_company) & 
        (combined['periodo'].isin(selected_periods))
    ].sort_values('fecha')
    
    comparison_data = combined[
        (combined['entidad'].isin(comparison_companies)) & 
        (combined['periodo'].isin(selected_periods))
    ]
    
    # Main content
    if not company_data.empty:
        # Company name and type
        company_type = company_data.iloc[0]['tipo']
        badge_class = "type-badge-sociedad" if company_type == "Sociedad" else "type-badge-agencia"
        type_label = "SOCIEDAD DE VALORES" if company_type == "Sociedad" else "AGENCIA DE VALORES"
        
        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 30px;">
            <h2 style="color: white; font-size: 28px; font-weight: 700; margin-bottom: 10px;">{selected_company}</h2>
            <span class="{badge_class}">{type_label}</span>
        </div>
        """, unsafe_allow_html=True)
        
        # Calculate quarterly metrics
        quarterly_metrics = calculate_quarterly_metrics(combined, selected_company)
        
        if quarterly_metrics is not None and not quarterly_metrics.empty:
            # KPIs from latest quarter
            latest = quarterly_metrics.iloc[-1]
            prev = quarterly_metrics.iloc[-2] if len(quarterly_metrics) > 1 else latest
            
            # KPI cards
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
            
            # Tabs for different views
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
                
                # Comprehensive performance chart
                fig = make_subplots(
                    rows=2, cols=2,
                    subplot_titles=("Evolución de Ingresos y Beneficio", "Crecimiento de Activos y Patrimonio", 
                                   "Tasas de Crecimiento Intertrimestral", "Análisis de Márgenes"),
                    vertical_spacing=0.12,
                    horizontal_spacing=0.10,
                    specs=[[{'secondary_y': True}, {'secondary_y': True}],
                           [{'secondary_y': False}, {'secondary_y': False}]]
                )
                
                # Income and Profit
                fig.add_trace(
                    go.Bar(x=quarterly_metrics['periodo'], y=quarterly_metrics['comisiones_percibidas'],
                          name='Comisiones', marker_color='#00d4ff', opacity=0.7,
                          text=quarterly_metrics['comisiones_percibidas'].round(0),
                          textposition='outside'),
                    row=1, col=1, secondary_y=False
                )
                fig.add_trace(
                    go.Scatter(x=quarterly_metrics['periodo'], y=quarterly_metrics['resultados_antes_impuestos'],
                              name='Beneficio', line=dict(color='#f687b3', width=3),
                              mode='lines+markers', marker=dict(size=10)),
                    row=1, col=1, secondary_y=True
                )
                
                # Assets and Equity
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
                
                # Growth rates
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
                
                # Margins
                fig.add_trace(
                    go.Scatter(x=quarterly_metrics['periodo'], y=quarterly_metrics['margen_neto'],
                              name='Margen Neto', line=dict(color='#ed8936', width=2),
                              mode='lines+markers', fill='tozeroy', opacity=0.3),
                    row=2, col=2
                )
                
                # Update layout
                fig.update_layout(**professional_theme['layout'], height=700, showlegend=True)
                fig.update_yaxes(title_text="Importe (€K)", row=1, col=1, secondary_y=False)
                fig.update_yaxes(title_text="Beneficio (€K)", row=1, col=1, secondary_y=True)
                fig.update_yaxes(title_text="Importe (€K)", row=1, col=2, secondary_y=False)
                fig.update_yaxes(title_text="Patrimonio (€K)", row=1, col=2, secondary_y=True)
                fig.update_yaxes(title_text="Tasa (%)", row=2, col=1)
                fig.update_yaxes(title_text="Margen (%)", row=2, col=2)
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Summary table
                st.markdown("### 📋 Resumen de Rendimiento")
                summary_df = quarterly_metrics[['periodo', 'comisiones_percibidas', 'resultados_antes_impuestos', 
                                               'ROA', 'ROE', 'ratio_eficiencia']].round(2)
                summary_df.columns = ['Trimestre', 'Comisiones (€K)', 'RAI (€K)', 'ROA (%)', 'ROE (%)', 'Eficiencia (%)']
                st.dataframe(summary_df, use_container_width=True)
            
            with tab2:
                st.markdown("### 📈 Análisis de Trayectoria de Crecimiento")
                
                fig_growth = make_subplots(
                    rows=2, cols=2,
                    subplot_titles=("Crecimiento Acumulado", "Rendimiento Indexado (Base 100)",
                                   "Evolución Trimestral", "Variación Porcentual"),
                    vertical_spacing=0.12,
                    horizontal_spacing=0.10
                )
                
                # Accumulated growth
                quarterly_metrics['cum_ingresos'] = quarterly_metrics['comisiones_percibidas'].cumsum()
                quarterly_metrics['cum_beneficio'] = quarterly_metrics['resultados_antes_impuestos'].cumsum()
                
                fig_growth.add_trace(
                    go.Scatter(x=quarterly_metrics['periodo'], y=quarterly_metrics['cum_ingresos'],
                              name='Ingresos Acum.', line=dict(color='#00d4ff', width=3),
                              mode='lines+markers', fill='tonexty'),
                    row=1, col=1
                )
                
                fig_growth.add_trace(
                    go.Scatter(x=quarterly_metrics['periodo'], y=quarterly_metrics['cum_beneficio'],
                              name='Beneficio Acum.', line=dict(color='#f687b3', width=3),
                              mode='lines+markers', fill='tozeroy'),
                    row=1, col=1
                )
                
                # Indexed performance
                if len(quarterly_metrics) > 0:
                    base_revenue = quarterly_metrics['comisiones_percibidas'].iloc[0]
                    base_assets = quarterly_metrics['activos_totales'].iloc[0]
                    
                    quarterly_metrics['indice_ingresos'] = (quarterly_metrics['comisiones_percibidas'] / base_revenue * 100) if base_revenue > 0 else 100
                    quarterly_metrics['indice_activos'] = (quarterly_metrics['activos_totales'] / base_assets * 100) if base_assets > 0 else 100
                    
                    fig_growth.add_trace(
                        go.Scatter(x=quarterly_metrics['periodo'], y=quarterly_metrics['indice_ingresos'],
                                  name='Índice Ingresos', line=dict(color='#00d4ff', width=2),
                                  mode='lines+markers'),
                        row=1, col=2
                    )
                    
                    fig_growth.add_trace(
                        go.Scatter(x=quarterly_metrics['periodo'], y=quarterly_metrics['indice_activos'],
                                  name='Índice Activos', line=dict(color='#4299e1', width=2, dash='dash'),
                                  mode='lines+markers'),
                        row=1, col=2
                    )
                    
                    # Base line 100
                    fig_growth.add_hline(y=100, line_width=1, line_dash="dot", line_color="gray", row=1, col=2)
                
                # Quarterly evolution
                fig_growth.add_trace(
                    go.Bar(x=quarterly_metrics['periodo'], y=quarterly_metrics['comisiones_percibidas'],
                          name='Comisiones', marker_color='#00d4ff', opacity=0.6),
                    row=2, col=1
                )
                
                # Percentage variation
                if len(quarterly_metrics) > 1:
                    colors = ['#48bb78' if x > 0 else '#ff3366' for x in quarterly_metrics['var_ingresos'][1:]]
                    
                    fig_growth.add_trace(
                        go.Bar(x=quarterly_metrics['periodo'][1:], y=quarterly_metrics['var_ingresos'][1:],
                              name='Var. Ingresos', marker_color=colors, opacity=0.7),
                        row=2, col=2
                    )
                
                fig_growth.update_layout(**professional_theme['layout'], height=700, showlegend=True)
                st.plotly_chart(fig_growth, use_container_width=True)
                
                # Growth metrics
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    avg_growth = quarterly_metrics['var_ingresos'][1:].mean() if len(quarterly_metrics) > 1 else 0
                    st.metric("Crecimiento Promedio", f"{avg_growth:.1f}%")
                
                with col2:
                    volatility = quarterly_metrics['var_ingresos'][1:].std() if len(quarterly_metrics) > 1 else 0
                    st.metric("Volatilidad", f"{volatility:.1f}%")
                
                with col3:
                    if len(quarterly_metrics) > 0:
                        total_growth = ((quarterly_metrics['comisiones_percibidas'].iloc[-1] / 
                                       quarterly_metrics['comisiones_percibidas'].iloc[0] - 1) * 100) if quarterly_metrics['comisiones_percibidas'].iloc[0] > 0 else 0
                    else:
                        total_growth = 0
                    st.metric("Crecimiento Total", f"{total_growth:.1f}%")
            
            with tab3:
                st.markdown("### ⚡ Análisis de Eficiencia Operativa")
                
                fig_eff = make_subplots(
                    rows=2, cols=2,
                    subplot_titles=("ROA vs ROE", "Ratio Coste-Ingreso", 
                                   "Apalancamiento", "Margen Neto"),
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
                
                # Cost-Income Ratio
                fig_eff.add_trace(
                    go.Bar(x=quarterly_metrics['periodo'], y=quarterly_metrics['ratio_eficiencia'],
                          name='Coste/Ingreso', marker_color='#ed8936', opacity=0.7,
                          text=quarterly_metrics['ratio_eficiencia'].round(1),
                          textposition='outside'),
                    row=1, col=2
                )
                
                # Leverage
                fig_eff.add_trace(
                    go.Scatter(x=quarterly_metrics['periodo'], y=quarterly_metrics['apalancamiento'],
                              name='Apalancamiento', line=dict(color='#9f7aea', width=3),
                              mode='lines+markers', fill='tozeroy', opacity=0.3),
                    row=2, col=1
                )
                
                # Net margin
                fig_eff.add_trace(
                    go.Scatter(x=quarterly_metrics['periodo'], y=quarterly_metrics['margen_neto'],
                              name='Margen Neto', line=dict(color='#48bb78', width=3),
                              mode='lines+markers', marker=dict(size=12),
                              fill='tozeroy', opacity=0.3),
                    row=2, col=2
                )
                
                fig_eff.update_layout(**professional_theme['layout'], height=700, showlegend=True)
                st.plotly_chart(fig_eff, use_container_width=True)
                
                # Key indicators
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("ROA Promedio", f"{quarterly_metrics['ROA'].mean():.2f}%")
                
                with col2:
                    st.metric("ROE Promedio", f"{quarterly_metrics['ROE'].mean():.2f}%")
                
                with col3:
                    st.metric("Eficiencia Promedio", f"{quarterly_metrics['ratio_eficiencia'].mean():.1f}%")
            
            with tab4:
                st.markdown("### 🏆 Análisis Comparativo con Competidores")
                
                if comparison_companies and not comparison_data.empty:
                    # Prepare comparison data
                    peer_metrics = []
                    for comp in comparison_companies:
                        comp_metrics = calculate_quarterly_metrics(combined, comp)
                        if comp_metrics is not None and not comp_metrics.empty:
                            latest_comp = comp_metrics.iloc[-1]
                            peer_metrics.append({
                                'Empresa': comp,
                                'Ingresos': latest_comp['comisiones_percibidas'],
                                'Beneficio': latest_comp['resultados_antes_impuestos'],
                                'ROA': latest_comp['ROA'],
                                'ROE': latest_comp['ROE'],
                                'Eficiencia': latest_comp['ratio_eficiencia']
                            })
                    
                    # Add selected company
                    peer_metrics.append({
                        'Empresa': selected_company,
                        'Ingresos': latest['comisiones_percibidas'],
                        'Beneficio': latest['resultados_antes_impuestos'],
                        'ROA': latest['ROA'],
                        'ROE': latest['ROE'],
                        'Eficiencia': latest['ratio_eficiencia']
                    })
                    
                    peer_df = pd.DataFrame(peer_metrics)
                    
                    # Comparative bar chart
                    fig_comp = go.Figure()
                    
                    metrics_to_plot = ['Ingresos', 'Beneficio', 'ROA', 'ROE']
                    for metric in metrics_to_plot:
                        colors = ['#00d4ff' if e == selected_company else '#b794f6' for e in peer_df['Empresa']]
                        fig_comp.add_trace(go.Bar(
                            name=metric,
                            x=peer_df['Empresa'],
                            y=peer_df[metric],
                            marker_color=colors[0] if metric == 'Ingresos' else None
                        ))
                    
                    fig_comp.update_layout(
                        **professional_theme['layout'],
                        height=500,
                        barmode='group',
                        title="Comparación con Competidores"
                    )
                    
                    st.plotly_chart(fig_comp, use_container_width=True)
                    
                    # Comparison table
                    st.markdown("### 📊 Tabla Comparativa")
                    peer_df_display = peer_df.round(2).sort_values('ROE', ascending=False)
                    st.dataframe(peer_df_display, use_container_width=True)
                else:
                    st.warning("Active la comparación en el panel lateral para ver este análisis")
            
            with tab5:
                st.markdown("### ⚖️ Comparación entre Sociedades y Agencias de Valores")
                
                # Separate data by type
                sociedades_data = combined[combined['tipo'] == 'Sociedad']
                agencias_data = combined[combined['tipo'] == 'Agencia']
                
                if len(sociedades_data) > 0 and len(agencias_data) > 0:
                    # Calculate average metrics by type and period
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
                    
                    # Comparative chart
                    fig_comp = make_subplots(
                        rows=2, cols=2,
                        subplot_titles=("Ingresos Promedio por Tipo", "Rentabilidad Promedio", 
                                       "Tamaño Promedio (Activos)", "Eficiencia Operativa"),
                        vertical_spacing=0.12,
                        horizontal_spacing=0.10
                    )
                    
                    # Average income
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
                    
                    # Profitability
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
                    
                    # Assets
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
                    
                    # Efficiency
                    if len(sociedades_avg) > 0:
                        sociedades_avg['eficiencia'] = (sociedades_avg['gastos_explotacion'] / 
                                                       sociedades_avg['margen_bruto'] * 100).fillna(0)
                    
                    if len(agencias_avg) > 0:
                        agencias_avg['eficiencia'] = (agencias_avg['gastos_explotacion'] / 
                                                     agencias_avg['margen_bruto'] * 100).fillna(0)
                    
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
                    
                    # Comparative statistics
                    st.markdown("### 📊 Estadísticas Comparativas: Sociedades vs Agencias")
                    
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
                    st.warning("No hay suficientes datos para comparar Sociedades y Agencias")
            
            with tab6:
                st.markdown("### 📉 Evaluación de Salud Financiera")
                
                # Calculate health components
                health_components = {
                    'Rentabilidad': min(100, (latest['ROE'] / 20 * 100)),
                    'Calidad de Activos': min(100, (latest['ROA'] / 10 * 100)),
                    'Eficiencia': max(0, (100 - latest['ratio_eficiencia'])),
                    'Margen': min(100, latest['margen_neto'] * 5) if latest['margen_neto'] > 0 else 0,
                    'Solvencia': min(100, 100 / latest['apalancamiento']) if latest['apalancamiento'] > 0 else 100
                }
                
                overall_health = sum(health_components.values()) / len(health_components)
                
                # Financial health gauge
                fig_health = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = overall_health,
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "Puntuación de Salud Financiera"},
                    gauge = {
                        'axis': {'range': [None, 100]},
                        'bar': {'color': "#00d4ff"},
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
                
                # Health components
                st.markdown("### 🎯 Componentes de la Puntuación")
                cols = st.columns(5)
                for idx, (component, score) in enumerate(health_components.items()):
                    with cols[idx]:
                        color = "#48bb78" if score >= 70 else "#ed8936" if score >= 40 else "#ff3366"
                        st.metric(component, f"{score:.0f}/100")
        
        # Export options
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
            summary_text = f"""
RESUMEN EJECUTIVO - {selected_company}
Fecha: {datetime.now().strftime('%d/%m/%Y')}

MÉTRICAS CLAVE (Último Trimestre)
==================================
Comisiones Percibidas: €{latest['comisiones_percibidas']:,.0f}K
Resultado antes de Impuestos: €{latest['resultados_antes_impuestos']:,.0f}K
ROA: {latest['ROA']:.2f}%
ROE: {latest['ROE']:.2f}%
Ratio de Eficiencia: {latest['ratio_eficiencia']:.2f}%

SALUD FINANCIERA
================
Puntuación Global: {overall_health:.1f}/100
            """ if quarterly_metrics is not None and not quarterly_metrics.empty else "No hay datos disponibles"
            
            st.download_button(
                label="📄 Descargar Resumen Ejecutivo",
                data=summary_text,
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
    
    # Footer
    st.divider()
    st.markdown("""
        <div style='text-align: center; padding: 20px;'>
            <p style='color: #00d4ff; font-size: 14px;'>Panel de Análisis Financiero v2.0</p>
            <p style='color: #a0aec0; font-size: 12px;'>Desarrollado por @Gsnchez | bquantfinance.com</p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
