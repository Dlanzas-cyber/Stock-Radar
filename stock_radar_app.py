"""
Stock Radar - Análisis Inteligente de Inversiones
Aplicación Streamlit para Swing Trading y Análisis de Cartera
"""

import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import io
from fpdf import FPDF
import anthropic
import os

# ═══════════════════════════════════════════════════════════
# CONFIGURACIÓN DE LA PÁGINA
# ═══════════════════════════════════════════════════════════

st.set_page_config(
    page_title="Stock Radar",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS personalizado
st.markdown("""
<style>
    .main-title {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .disclaimer-box {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 4px;
    }
    .stButton>button {
        width: 100%;
        height: 60px;
        font-size: 1.1rem;
        font-weight: 600;
        border-radius: 8px;
    }
    .section-header {
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #667eea;
    }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# FUNCIONES AUXILIARES
# ═══════════════════════════════════════════════════════════

def get_api_key():
    """Obtener API key de Anthropic"""
    # Primero intentar desde secrets de Streamlit
    try:
        return st.secrets["ANTHROPIC_API_KEY"]
    except:
        # Si no, desde variables de entorno
        return os.getenv("ANTHROPIC_API_KEY")

def download_etf_holdings(etf_ticker):
    """
    Descargar holdings de ETF desde iShares
    
    Args:
        etf_ticker: IWM, IWC, IJR, etc.
    
    Returns:
        DataFrame con holdings o None si falla
    """
    
    urls = {
        'IWM': 'https://www.ishares.com/us/products/239710/ishares-russell-2000-etf/1467271812596.ajax?fileType=csv&fileName=IWM_holdings&dataType=fund',
        'IWC': 'https://www.ishares.com/us/products/239382/ishares-microcap-etf/1467271812596.ajax?fileType=csv&fileName=IWC_holdings&dataType=fund',
        'IJR': 'https://www.ishares.com/us/products/239774/ishares-core-sp-smallcap-etf/1467271812596.ajax?fileType=csv&fileName=IJR_holdings&dataType=fund'
    }
    
    if etf_ticker not in urls:
        return None
    
    try:
        df = pd.read_csv(urls[etf_ticker], skiprows=10)
        # Filtrar por peso >0.1%
        df = df[df['Weight (%)'] > 0.1]
        return df
    except Exception as e:
        st.error(f"Error descargando {etf_ticker}: {str(e)}")
        return None

def get_stooq_data(ticker, days=200):
    """
    Obtener datos de Stooq
    
    Args:
        ticker: Ticker de la acción
        days: Días de histórico
    
    Returns:
        DataFrame con OHLCV o None si falla
    """
    
    url = f"https://stooq.com/q/d/?s={ticker}.us&i=d"
    
    try:
        df = pd.read_csv(url)
        df = df.tail(days)
        return df
    except:
        return None

def execute_swing_analysis(api_key, capital=1000):
    """
    Ejecutar análisis swing trading usando Claude API
    
    Args:
        api_key: API key de Anthropic
        capital: Capital disponible en €
    
    Returns:
        dict con resultados del análisis
    """
    
    # Cargar prompt V3.1
    with open('prompts/prompt_swing_v3_1.txt', 'r', encoding='utf-8') as f:
        prompt_template = f.read()
    
    # Personalizar prompt
    prompt = prompt_template.replace('[INSERTAR FECHA ACTUAL]', datetime.now().strftime('%Y-%m-%d'))
    prompt = prompt.replace('[INSERTAR €XXX]', f'€{capital}')
    
    # Llamar a Claude API
    try:
        client = anthropic.Anthropic(api_key=api_key)
        
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=8000,
            temperature=0.3,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        response_text = message.content[0].text
        
        # Parsear respuesta (simplificado)
        result = {
            'fecha': datetime.now().strftime('%Y-%m-%d'),
            'capital': capital,
            'analisis_completo': response_text,
            'top_3': extract_top3(response_text)  # Función auxiliar
        }
        
        return result
        
    except Exception as e:
        st.error(f"Error en análisis: {str(e)}")
        return None

def execute_portfolio_analysis(api_key, df_portfolio):
    """
    Ejecutar análisis de cartera usando Claude API
    
    Args:
        api_key: API key de Anthropic
        df_portfolio: DataFrame con cartera
    
    Returns:
        dict con resultados del análisis
    """
    
    # Cargar prompt de análisis de cartera (a crear)
    prompt = f"""
    Analiza esta cartera de inversiones y propón las mejores oportunidades
    para ampliar posiciones existentes.
    
    Cartera:
    {df_portfolio.to_string()}
    
    Proporciona:
    1. Análisis de posiciones actuales
    2. TOP 3 posiciones para ampliar (de las existentes)
    3. Justificación basada en fundamentales y técnicos
    4. Plan de compra con cantidades específicas
    """
    
    try:
        client = anthropic.Anthropic(api_key=api_key)
        
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=6000,
            temperature=0.3,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        response_text = message.content[0].text
        
        result = {
            'fecha': datetime.now().strftime('%Y-%m-%d'),
            'analisis_completo': response_text,
            'recomendaciones': extract_recommendations(response_text)
        }
        
        return result
        
    except Exception as e:
        st.error(f"Error en análisis: {str(e)}")
        return None

def extract_top3(response_text):
    """Extraer TOP 3 del texto de respuesta"""
    # Implementación simplificada - parsear el texto
    # En producción, usar regex o parsing más robusto
    top3 = []
    # TODO: Implementar parsing real
    return top3

def extract_recommendations(response_text):
    """Extraer recomendaciones del texto"""
    # TODO: Implementar parsing
    return []

def generate_pdf(analysis_result):
    """
    Generar PDF del análisis usando FPDF
    
    Args:
        analysis_result: dict con resultados
    
    Returns:
        BytesIO con PDF
    """
    
    class PDF(FPDF):
        def header(self):
            self.set_font('Arial', 'B', 20)
            self.set_text_color(102, 126, 234)  # #667eea
            self.cell(0, 10, 'Stock Radar - Analisis de Inversiones', 0, 1, 'C')
            self.ln(5)
        
        def footer(self):
            self.set_y(-15)
            self.set_font('Arial', 'I', 8)
            self.set_text_color(128, 128, 128)
            self.cell(0, 10, f'Pagina {self.page_no()}', 0, 0, 'C')
    
    # Crear PDF
    pdf = PDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Fecha
    pdf.set_font('Arial', '', 10)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, f"Fecha: {analysis_result['fecha']}", 0, 1)
    pdf.cell(0, 10, f"Capital: €{analysis_result['capital']}", 0, 1)
    pdf.ln(5)
    
    # Contenido
    pdf.set_font('Arial', '', 9)
    
    # Dividir texto en líneas para evitar overflow
    text = analysis_result['analisis_completo']
    
    # Reemplazar caracteres problemáticos
    text = text.replace('—', '-')
    text = text.replace('–', '-')
    text = text.replace('"', '"')
    text = text.replace('"', '"')
    text = text.replace(''', "'")
    text = text.replace(''', "'")
    text = text.replace('█', '#')
    text = text.replace('═', '=')
    text = text.replace('│', '|')
    text = text.replace('├', '+')
    text = text.replace('└', '+')
    text = text.encode('latin-1', 'replace').decode('latin-1')
    
    # Escribir texto
    lines = text.split('\n')
    for line in lines:
        if line.strip():
            # Detectar títulos (líneas cortas con ### o en mayúsculas)
            if line.startswith('###') or (len(line) < 50 and line.isupper()):
                pdf.set_font('Arial', 'B', 11)
                pdf.multi_cell(0, 5, line.replace('###', '').strip())
                pdf.set_font('Arial', '', 9)
            elif line.startswith('#'):
                pdf.set_font('Arial', 'B', 10)
                pdf.multi_cell(0, 5, line.replace('#', '').strip())
                pdf.set_font('Arial', '', 9)
            else:
                pdf.multi_cell(0, 5, line)
        else:
            pdf.ln(2)
    
    # Guardar en BytesIO
    buffer = io.BytesIO()
    pdf_output = pdf.output(dest='S').encode('latin-1')
    buffer.write(pdf_output)
    buffer.seek(0)
    
    return buffer

def send_to_telegram(message, bot_token, chat_id):
    """
    Enviar mensaje a Telegram
    
    Args:
        message: Texto a enviar
        bot_token: Token del bot
        chat_id: ID del chat
    
    Returns:
        bool: True si éxito
    """
    
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'Markdown'
    }
    
    try:
        response = requests.post(url, json=payload)
        return response.status_code == 200
    except Exception as e:
        st.error(f"Error enviando a Telegram: {str(e)}")
        return False

# ═══════════════════════════════════════════════════════════
# INTERFAZ PRINCIPAL
# ═══════════════════════════════════════════════════════════

def main():
    
    # ─────────────────────────────────────────────────────────
    # HEADER
    # ─────────────────────────────────────────────────────────
    
    st.markdown('<h1 class="main-title">📡 STOCK RADAR</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Sistema Inteligente de Análisis de Inversiones</p>', unsafe_allow_html=True)
    
    # ─────────────────────────────────────────────────────────
    # DISCLAIMER
    # ─────────────────────────────────────────────────────────
    
    st.markdown("""
    <div class="disclaimer-box">
        <strong>⚠️ DISCLAIMER:</strong> Esta herramienta proporciona análisis basado en datos públicos 
        y no constituye asesoramiento financiero. Las decisiones de inversión son responsabilidad 
        del usuario. Invierte solo capital que puedas permitirte perder. Los rendimientos pasados 
        no garantizan resultados futuros.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ─────────────────────────────────────────────────────────
    # DOS COLUMNAS PRINCIPALES
    # ─────────────────────────────────────────────────────────
    
    col_left, col_right = st.columns(2, gap="large")
    
    # ═════════════════════════════════════════════════════════
    # COLUMNA IZQUIERDA: SWING TRADING
    # ═════════════════════════════════════════════════════════
    
    with col_left:
        st.markdown('<p class="section-header">🎯 Análisis Swing Trading</p>', unsafe_allow_html=True)
        
        st.markdown("""
        Análisis automático de **TOP 3 mejores oportunidades** swing trading en small/mid caps.
        
        **Incluye:**
        - Score multi-criterio (0-150 pts)
        - Probabilidad de éxito (30-85%)
        - Entradas, stops y targets específicos
        - Plan de compra con cantidades
        """)
        
        # Parámetros
        capital_swing = st.number_input(
            "💰 Capital disponible (€)",
            min_value=100,
            max_value=10000,
            value=1000,
            step=100,
            key="capital_swing"
        )
        
        st.markdown("")
        
        # Botón ejecutar
        if st.button("🚀 EJECUTAR ANÁLISIS SWING", key="btn_swing", type="primary"):
            
            api_key = get_api_key()
            
            if not api_key:
                st.error("❌ No se encontró API key de Anthropic. Configura ANTHROPIC_API_KEY en secrets.")
            else:
                with st.spinner("🔍 Analizando mercado... (puede tardar 30-60 segundos)"):
                    
                    # Ejecutar análisis
                    result = execute_swing_analysis(api_key, capital_swing)
                    
                    if result:
                        st.success("✅ Análisis completado!")
                        
                        # Mostrar resultados
                        st.markdown("### 📊 Resultados")
                        
                        # Mostrar análisis completo en expander
                        with st.expander("📄 Ver análisis completo", expanded=True):
                            st.markdown(result['analisis_completo'])
                        
                        st.markdown("---")
                        
                        # Opciones de exportación
                        st.markdown("### 📤 Exportar Resultados")
                        
                        export_col1, export_col2 = st.columns(2)
                        
                        with export_col1:
                            # Generar PDF
                            pdf_buffer = generate_pdf(result)
                            
                            st.download_button(
                                label="📥 Descargar PDF",
                                data=pdf_buffer,
                                file_name=f"stock_radar_swing_{result['fecha']}.pdf",
                                mime="application/pdf",
                                key="download_pdf_swing"
                            )
                        
                        with export_col2:
                            # Telegram
                            if st.button("📱 Enviar a Telegram", key="send_telegram_swing"):
                                # Mostrar inputs para Telegram
                                with st.form("telegram_form_swing"):
                                    bot_token = st.text_input("Bot Token", type="password")
                                    chat_id = st.text_input("Chat ID")
                                    
                                    if st.form_submit_button("Enviar"):
                                        if bot_token and chat_id:
                                            # Preparar mensaje resumido
                                            message = f"""
🎯 **STOCK RADAR - Análisis Swing Trading**
📅 {result['fecha']}
💰 Capital: €{result['capital']}

{result['analisis_completo'][:4000]}...

_Ver análisis completo en la app_
                                            """
                                            
                                            if send_to_telegram(message, bot_token, chat_id):
                                                st.success("✅ Enviado a Telegram!")
                                            else:
                                                st.error("❌ Error enviando a Telegram")
                                        else:
                                            st.warning("⚠️ Completa ambos campos")
    
    # ═════════════════════════════════════════════════════════
    # COLUMNA DERECHA: ANÁLISIS CARTERA
    # ═════════════════════════════════════════════════════════
    
    with col_right:
        st.markdown('<p class="section-header">📊 Análisis de Cartera</p>', unsafe_allow_html=True)
        
        st.markdown("""
        Analiza tu cartera actual y recibe recomendaciones para **ampliar posiciones existentes**.
        
        **Incluye:**
        - Análisis de cada posición
        - TOP 3 posiciones para ampliar
        - Justificación fundamentada
        - Plan de compra específico
        """)
        
        # Upload CSV
        uploaded_file = st.file_uploader(
            "📂 Subir cartera (CSV)",
            type=['csv'],
            help="CSV con columnas: Ticker, Acciones, Precio_Compra, Valor_Actual",
            key="upload_portfolio"
        )
        
        if uploaded_file is not None:
            # Leer CSV
            try:
                df_portfolio = pd.read_csv(uploaded_file)
                
                # Mostrar preview
                st.markdown("#### Vista previa:")
                st.dataframe(df_portfolio.head(), use_container_width=True)
                
                st.markdown("")
                
                # Botón analizar
                if st.button("🔬 ANALIZAR CARTERA", key="btn_portfolio", type="primary"):
                    
                    api_key = get_api_key()
                    
                    if not api_key:
                        st.error("❌ No se encontró API key de Anthropic.")
                    else:
                        with st.spinner("🔍 Analizando cartera..."):
                            
                            # Ejecutar análisis
                            result = execute_portfolio_analysis(api_key, df_portfolio)
                            
                            if result:
                                st.success("✅ Análisis completado!")
                                
                                # Mostrar resultados
                                st.markdown("### 📊 Resultados")
                                
                                with st.expander("📄 Ver análisis completo", expanded=True):
                                    st.markdown(result['analisis_completo'])
                                
                                st.markdown("---")
                                
                                # Opciones exportación
                                st.markdown("### 📤 Exportar Resultados")
                                
                                export_col1, export_col2 = st.columns(2)
                                
                                with export_col1:
                                    pdf_buffer = generate_pdf(result)
                                    
                                    st.download_button(
                                        label="📥 Descargar PDF",
                                        data=pdf_buffer,
                                        file_name=f"stock_radar_cartera_{result['fecha']}.pdf",
                                        mime="application/pdf",
                                        key="download_pdf_portfolio"
                                    )
                                
                                with export_col2:
                                    if st.button("📱 Enviar a Telegram", key="send_telegram_portfolio"):
                                        with st.form("telegram_form_portfolio"):
                                            bot_token = st.text_input("Bot Token", type="password")
                                            chat_id = st.text_input("Chat ID")
                                            
                                            if st.form_submit_button("Enviar"):
                                                if bot_token and chat_id:
                                                    message = f"""
📊 **STOCK RADAR - Análisis de Cartera**
📅 {result['fecha']}

{result['analisis_completo'][:4000]}...

_Ver análisis completo en la app_
                                                    """
                                                    
                                                    if send_to_telegram(message, bot_token, chat_id):
                                                        st.success("✅ Enviado a Telegram!")
                                                    else:
                                                        st.error("❌ Error enviando")
                                                else:
                                                    st.warning("⚠️ Completa ambos campos")
            
            except Exception as e:
                st.error(f"❌ Error leyendo CSV: {str(e)}")
                st.info("Asegúrate que el CSV tenga las columnas correctas")
        
        else:
            st.info("👆 Sube un archivo CSV con tu cartera para comenzar")
    
    # ─────────────────────────────────────────────────────────
    # FOOTER
    # ─────────────────────────────────────────────────────────
    
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 1rem;'>
        <p><strong>Stock Radar v1.0</strong> | Powered by Claude Sonnet 4 & Streamlit</p>
        <p style='font-size: 0.9rem;'>Datos de Stooq.com (EOD) y iShares ETF Holdings (públicos)</p>
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# EJECUCIÓN
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    main()
