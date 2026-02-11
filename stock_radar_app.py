"""
Stock Radar - Análisis Inteligente de Inversiones
Aplicación Streamlit para Swing Trading y Análisis de Cartera
v1.0.2 - Prompts embebidos
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
# PROMPTS EMBEBIDOS
# ═══════════════════════════════════════════════════════════

PROMPT_SWING = """Eres un analista experto en swing trading. Analiza el mercado de small/mid caps USA y proporciona las TOP 3 mejores oportunidades.

FECHA: {fecha}
CAPITAL: €{capital}

TAREA:
1. Analiza entorno macro (VIX, small vs large caps)
2. Identifica TOP 3 oportunidades 
3. Para cada una: Score (0-150), Probabilidad (30-85%), Entrada/Stop/Targets, R/R >2.5

FORMATO:
- Resumen ejecutivo
- Contexto macro
- TOP 3 detallado (#1, #2, #3)
- Plan de compra con cantidades

Solo posiciones largas, accionable y conciso."""

PROMPT_PORTFOLIO = """Analiza esta cartera y proporciona TOP 3 posiciones para ampliar:

CARTERA:
{portfolio}

TAREA:
1. Analiza posiciones actuales
2. Identifica TOP 3 para ampliar
3. Justifica con fundamentales
4. Plan de compra específico

Sé específico y accionable."""

# ═══════════════════════════════════════════════════════════
# CONFIGURACIÓN
# ═══════════════════════════════════════════════════════════

st.set_page_config(
    page_title="Stock Radar",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
.main-title {
    font-size: 3.5rem; font-weight: 800;
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    text-align: center; margin-bottom: 0.5rem;
}
.subtitle { text-align: center; color: #666; font-size: 1.2rem; margin-bottom: 2rem; }
.disclaimer-box { background-color: #fff3cd; border-left: 4px solid #ffc107;
    padding: 1rem; margin: 1rem 0; border-radius: 4px; }
.stButton>button { width: 100%; height: 60px; font-size: 1.1rem;
    font-weight: 600; border-radius: 8px; }
.section-header { font-size: 1.8rem; font-weight: 700; margin-bottom: 1rem;
    padding-bottom: 0.5rem; border-bottom: 2px solid #667eea; }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# FUNCIONES
# ═══════════════════════════════════════════════════════════

def get_api_key():
    try:
        return st.secrets["ANTHROPIC_API_KEY"]
    except:
        return os.getenv("ANTHROPIC_API_KEY")

def analyze_with_claude(prompt, api_key, max_tokens=8000):
    try:
        client = anthropic.Anthropic(api_key=api_key)
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=max_tokens,
            temperature=0.3,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        return None

def generate_pdf(result):
    class PDF(FPDF):
        def header(self):
            self.set_font('Arial', 'B', 20)
            self.set_text_color(102, 126, 234)
            self.cell(0, 10, 'Stock Radar', 0, 1, 'C')
            self.ln(5)
        def footer(self):
            self.set_y(-15)
            self.set_font('Arial', 'I', 8)
            self.set_text_color(128, 128, 128)
            self.cell(0, 10, f'Pag {self.page_no()}', 0, 0, 'C')
    
    pdf = PDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font('Arial', '', 10)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, f"Fecha: {result['fecha']}", 0, 1)
    if 'capital' in result:
        pdf.cell(0, 10, f"Capital: EUR {result['capital']}", 0, 1)
    pdf.ln(5)
    pdf.set_font('Arial', '', 9)
    
    text = result['analisis']
    for old, new in [('—','-'),('€','EUR'),('█','#'),('═','=')]:
        text = text.replace(old, new)
    text = text.encode('latin-1', 'replace').decode('latin-1')
    
    for line in text.split('\n'):
        if line.strip():
            if line.startswith('###'):
                pdf.set_font('Arial', 'B', 11)
                pdf.multi_cell(0, 5, line.replace('###','').strip())
                pdf.set_font('Arial', '', 9)
            else:
                pdf.multi_cell(0, 5, line)
        else:
            pdf.ln(2)
    
    buffer = io.BytesIO()
    buffer.write(pdf.output(dest='S').encode('latin-1'))
    buffer.seek(0)
    return buffer

def send_telegram(message, token, chat_id):
    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        r = requests.post(url, json={'chat_id': chat_id, 'text': message, 'parse_mode': 'Markdown'})
        return r.status_code == 200
    except:
        return False

# ═══════════════════════════════════════════════════════════
# INTERFAZ
# ═══════════════════════════════════════════════════════════

st.markdown('<h1 class="main-title">📡 STOCK RADAR</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Sistema Inteligente de Análisis de Inversiones</p>', unsafe_allow_html=True)

st.markdown("""
<div class="disclaimer-box">
<strong>⚠️ DISCLAIMER:</strong> Esta herramienta proporciona análisis basado en datos públicos 
y no constituye asesoramiento financiero. Invierte solo capital que puedas permitirte perder.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

col_left, col_right = st.columns(2, gap="large")

# SWING TRADING
with col_left:
    st.markdown('<p class="section-header">🎯 Análisis Swing Trading</p>', unsafe_allow_html=True)
    st.markdown("Análisis automático **TOP 3 mejores oportunidades** swing trading.")
    
    capital = st.number_input("💰 Capital (€)", 100, 10000, 1000, 100, key="cap_swing")
    st.markdown("")
    
    if st.button("🚀 EJECUTAR ANÁLISIS", key="btn_swing", type="primary"):
        api_key = get_api_key()
        if not api_key:
            st.error("❌ API key no encontrada. Configura ANTHROPIC_API_KEY en secrets.")
        else:
            with st.spinner("🔍 Analizando mercado (30-60s)..."):
                prompt = PROMPT_SWING.format(fecha=datetime.now().strftime('%Y-%m-%d'), capital=capital)
                analisis = analyze_with_claude(prompt, api_key)
                
                if analisis:
                    st.success("✅ Análisis completado!")
                    result = {'fecha': datetime.now().strftime('%Y-%m-%d'), 'capital': capital, 'analisis': analisis}
                    
                    with st.expander("📄 Ver análisis", expanded=True):
                        st.markdown(analisis)
                    
                    st.markdown("---")
                    st.markdown("### 📤 Exportar")
                    
                    c1, c2 = st.columns(2)
                    with c1:
                        pdf = generate_pdf(result)
                        st.download_button("📥 PDF", pdf, f"swing_{result['fecha']}.pdf", "application/pdf")
                    
                    with c2:
                        with st.expander("📱 Telegram"):
                            token = st.text_input("Bot Token", type="password", key="t1")
                            chat = st.text_input("Chat ID", key="c1")
                            if st.button("Enviar", key="s1"):
                                if token and chat:
                                    msg = f"🎯 STOCK RADAR\n📅 {result['fecha']}\n\n{analisis[:4000]}..."
                                    if send_telegram(msg, token, chat):
                                        st.success("✅ Enviado!")
                                    else:
                                        st.error("❌ Error")

# CARTERA
with col_right:
    st.markdown('<p class="section-header">📊 Análisis de Cartera</p>', unsafe_allow_html=True)
    st.markdown("Analiza tu cartera y recibe recomendaciones para ampliar posiciones.")
    
    file = st.file_uploader("📂 Subir CSV", type=['csv'], key="up_port")
    
    if file:
        try:
            df = pd.read_csv(file)
            st.markdown("#### Vista previa:")
            st.dataframe(df.head(), use_container_width=True)
            st.markdown("")
            
            if st.button("🔬 ANALIZAR", key="btn_port", type="primary"):
                api_key = get_api_key()
                if not api_key:
                    st.error("❌ API key no encontrada")
                else:
                    with st.spinner("🔍 Analizando..."):
                        prompt = PROMPT_PORTFOLIO.format(portfolio=df.to_string())
                        analisis = analyze_with_claude(prompt, api_key, 6000)
                        
                        if analisis:
                            st.success("✅ Completado!")
                            result = {'fecha': datetime.now().strftime('%Y-%m-%d'), 'analisis': analisis}
                            
                            with st.expander("📄 Ver análisis", expanded=True):
                                st.markdown(analisis)
                            
                            st.markdown("---")
                            st.markdown("### 📤 Exportar")
                            
                            c1, c2 = st.columns(2)
                            with c1:
                                pdf = generate_pdf(result)
                                st.download_button("📥 PDF", pdf, f"cartera_{result['fecha']}.pdf", "application/pdf")
                            
                            with c2:
                                with st.expander("📱 Telegram"):
                                    token = st.text_input("Bot Token", type="password", key="t2")
                                    chat = st.text_input("Chat ID", key="c2")
                                    if st.button("Enviar", key="s2"):
                                        if token and chat:
                                            msg = f"📊 CARTERA\n📅 {result['fecha']}\n\n{analisis[:4000]}..."
                                            if send_telegram(msg, token, chat):
                                                st.success("✅ Enviado!")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
    else:
        st.info("👆 Sube un CSV con: Ticker, Acciones, Precio_Compra, Valor_Actual")

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
<p><strong>Stock Radar v1.0.2</strong> | Claude Sonnet 4 & Streamlit</p>
</div>
""", unsafe_allow_html=True)
