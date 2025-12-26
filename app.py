#Bloque de Configuración y Herramientas (Setup)

import streamlit as st  #La base web
import pandas as pd     
import pickle           #Carga de modelo de ML
import re               #Limpiar el texto de entrada
import plotly.express as px #Gráficas interactivas 
import plotly.io as pio     #Configuración de temas

pio.templates.default = "plotly_dark"

st.set_page_config(
    page_title='Mining Analytics',
    layout='wide',
    initial_sidebar_state='expanded'
)

col_h1, col_h2, col_h3 = st.columns([1, 6, 1])
with col_h2:
    # Puedes cambiar esta URL por una imagen tuya si quieres
    st.image("images/web.gif", width=80)
    st.title("MINE-OS: Operational Command Center")
    st.markdown("Artificial Intelligence System for Real-Time Risk Monitoring")

st.markdown("""
<style>
    /* A. Fondo y fuentes * /"
    .stAPP {
        background-color: #000000;
            font-family: -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /*B. Eliminar elementos nativos molestos*/
    #MainMenu {visibility: hidden;}
    footer {visibility:heddine;}
    header {
        visibility:visible !important;
        background: transparent !important;
    }
    
    /*C. Tarjetas de Vidrio */
   .glass-card {
        background: rgba(20, 20, 20, 0.6); /* Más oscuro para contraste */
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 15px; /* Menos padding */
        margin-bottom: 20px;
        /* Flexbox para centrar contenido vertical y horizontalmente */
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        height: 100%; /* Llenar altura */
    }
    
    /* D. METRICAS ESTILIZADAS (Ajuste de fuentes) */
    .metric-value {
        font-size: 2rem; /* Un poco más chico para que quepan 5 */
        font-weight: 700;
        margin-top: 5px;
        color: white;
    }
    .metric-label {
        color: #aaaaaa;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 500;
    }
    /*E. Sidebar limpio */
    section[data_testid="stSidebar"]{
        background-color: #0a0a0a;
        border-right:1px solid #222;
    }
</style>
""", unsafe_allow_html=True)

#Bloque de Carga de Modelo

@st.cache_resource
def load_resources():
    #Usar en modo binario ('rb')
    model = pickle.load(open('mining_model.pkl','rb'))
    vectorizer = pickle.load(open('vectorizer.pkl','rb'))
    return model, vectorizer

try:
    model, vectorizer = load_resources()
except FileNotFoundError:
    st.error('Error crítico: No se encontrarón los archivos .pkl. Asgúrate de haberlos cargado correctamente')
    st.stop()

#Bloque de ETL Y Procesamiento (La fábrica)

#Crear función de ETL
def parse_and_process(load_file):
    """
    Recibe el .txt lo estructura predice categorías y extra la hora 
    """
    #Extraer los datos del .txt
    content = uploaded_file.read().decode("utf-8")
    lines = content.split('\n')

    data_list = []
    current_record = {}
    #Iterar por cada línea y revisar si hay datos o no
    for line in lines:
        line = line.strip()
        if not line:
            if current_record:
                data_list.append(current_record)
                current_record = {}
            continue
        #Si hay separarlos en un diccionario y guardalos en una lista
        if  ':' in line:
            key, value = line.split(':',1)
            current_record[key.strip()] =value.strip()    
    
    if current_record:
        data_list.append(current_record)
        
    #Convertir esa lista en pd
    df = pd.DataFrame(data_list)
    #Una sub-función de limpieza de texto
    def clean(text):
        return re.sub('r[^\w\s]','', str(text).lower())
    # Limpiar el texto
    df['clean_text'] = df['DA'].apply(clean)
    #Hacer las predicciones de categorías
    vectors = vectorizer.transform(df['clean_text'])
    df['categoria'] = model.predict(vectors)
    # Hacer una función de transformación de hora
    def extraer_hora(h_str):
        try:
            return int(str(h_str).split(':')[0])
        except:
            return 0
    #Transformar la hora
    if 'HO' in df.columns:
        df['Hora_nv'] = df['HO'].apply(extraer_hora)
    else:
        df['Hora_nv'] = 0
    
    return df

#Bloque de Visualización

# Barra lateral para la carga de archivos (Más limpio)
with st.sidebar:
    st.image("images/files.png", width=50) # Logo conceptual
    st.markdown("<h3 style='color: white;'>MINE-OS <span style='font-size:12px; color:#666;'>Pro</span></h3>", unsafe_allow_html=True)
    st.write("")
    uploaded_file = st.file_uploader("Drop Log File", type=['txt'])
    st.write("")
    st.info("System Status: Online")

if uploaded_file is not None:
    df = parse_and_process(uploaded_file)
    
    # 5.1 HEADER "APPLE STYLE"
    st.markdown("<h1 style='text-align: center; color: white; font-weight: 300; font-size: 3rem;'>Operations <span style='font-weight:700;'>Insight</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #666; margin-bottom: 40px;'>Real-time AI analysis of mining communications.</p>", unsafe_allow_html=True)

    # 5.2 KPI CARDS PERSONALIZADAS (HTML PURO)
    # Aquí rompemos la limitación de st.metric
    tot = len(df)
    seg = len(df[df['categoria']=='SEGURIDAD'])
    man = len(df[df['categoria']=='MANTENIMIENTO'])
    log = len(df[df['categoria']=='LOGISTICA'])
    opr = len(df[df['categoria']=='OPERACION'])

    col1, col2, col3, col4,col5 = st.columns(5)
    
    # Función para dibujar tarjeta
    def card_html(label, value, color_hex):
        return f"""
        <div class="glass-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value" style="color: {color_hex}; text-shadow: 0 0 10px {color_hex}44;">{value}</div>
        </div>
        """

    with col1: st.markdown(card_html("Total", tot, "#ffffff"), unsafe_allow_html=True)
    with col2: st.markdown(card_html("Seguridad", seg, "#FF453A"), unsafe_allow_html=True) 
    with col3: st.markdown(card_html("Mantenimiento", man, "#FFD60A"), unsafe_allow_html=True)
    with col4: st.markdown(card_html("Logística", log, "#0A84FF"), unsafe_allow_html=True)
    with col5: st.markdown(card_html("Operación", opr, "#30D158"), unsafe_allow_html=True)
    # 5.3 GRÁFICA PRINCIPAL (Minimalista)
    st.markdown("")
    col_main, col_detail = st.columns([2, 1])

    with col_main:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("<h4 style='color:white; margin-bottom:20px;'>Timeline Activity</h4>", unsafe_allow_html=True)
        
        df_timeline = df.groupby(['Hora_nv', 'categoria']).size().reset_index(name='CANTIDAD').sort_values('Hora_nv')
        
        # Colores Apple Interface
        APPLE_COLORS = {
            'SEGURIDAD': '#FF453A', 
            'MANTENIMIENTO': '#FFD60A', 
            'LOGISTICA': '#0A84FF', 
            'OPERACION': '#30D158'
        }
        
        fig = px.area(df_timeline, x='Hora_nv', y='CANTIDAD', color='categoria',
                      color_discrete_map=APPLE_COLORS)
        
        # "Steve Jobs Mode": Quitar TODO lo que no sea dato
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#888',
            showlegend=False,
            margin=dict(l=0, r=0, t=0, b=0),
            height=300,
            xaxis=dict(showgrid=False, showticklabels=True),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', showticklabels=True),
            # ESTO ARREGLA LOS TOOLTIPS FEOS:
            hoverlabel=dict(
                bgcolor="#111111", # Fondo negro
                font_size=12,
                font_family="-apple-system, sans-serif",
                bordercolor="#333333" # Borde sutil
            )
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_detail:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("<h4 style='color:white;'>Zone Focus</h4>", unsafe_allow_html=True)
        
        fig_pie = px.pie(df, names='categoria', color='categoria', 
                         color_discrete_map=APPLE_COLORS, hole=0.7)
        
        fig_pie.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            showlegend=False,
            margin=dict(l=0, r=0, t=0, b=0),
            height=300
        )
        # Texto en el centro de la dona
        fig_pie.add_annotation(text=f"{len(df)}", showarrow=False, font=dict(size=40, color="white"))
        
        st.plotly_chart(fig_pie, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True) 

    
    # 5.4 DRILL-DOWN (SUNBURST CHART BLINDADO)
    st.markdown("<h3 style='color: white; margin-top: 30px;'>Drill-Down Analysis</h3>", unsafe_allow_html=True)
    
    cols_necesarias = ['categoria', 'LS', 'UD']
    
    # Verificamos si existen las columnas
    if all(col in df.columns for col in cols_necesarias):
        
        # --- PASO CRÍTICO DE LIMPIEZA ---
        # 1. Creamos una copia para no ensuciar el dataframe original
        df_sun = df.copy()
        
        # 2. Rellenamos CUALQUIER valor nulo (NaN/None) con un texto placeholder
        # Esto evita el error "None entries cannot have children"
        df_sun['LS'] = df_sun['LS'].fillna('Desconocido').replace('', 'Desconocido')
        df_sun['UD'] = df_sun['UD'].fillna('General').replace('', 'General')
        df_sun['categoria'] = df_sun['categoria'].fillna('Sin Categoría')
        
        # 3. Generamos el gráfico con los datos limpios
        try:
            fig_sun = px.sunburst(
                df_sun, 
                path=['categoria', 'LS', 'UD'], 
                color='categoria',
                color_discrete_map=APPLE_COLORS
            )
            
            fig_sun.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(t=0, l=0, r=0, b=0),
                height=500,
                font=dict(family="-apple-system, sans-serif", size=14),
                hoverlabel=dict(bgcolor="#111111", bordercolor="#333")
            )
            
            st.plotly_chart(fig_sun, use_container_width=True)
            st.caption("Tip: Haz clic en el centro o en los aros para entrar y salir del nivel de detalle.")
            
        except Exception as e:
            st.error(f"Error al generar gráfico jerárquico: {e}")
            st.warning("Verifica que tu archivo .txt no tenga saltos de línea extraños o datos incompletos.")
        
    else:
        faltantes = [c for c in cols_necesarias if c not in df.columns]

        st.warning(f"No se puede generar el gráfico de detalle. Tu archivo .txt no tiene los campos: {faltantes}")


