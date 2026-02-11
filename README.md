# 📡 Stock Radar

**Sistema Inteligente de Análisis de Inversiones**

Aplicación Streamlit para análisis automatizado de swing trading y gestión de carteras de inversión.

![Stock Radar](https://img.shields.io/badge/version-1.0-blue)
![Python](https://img.shields.io/badge/python-3.9+-green)
![Streamlit](https://img.shields.io/badge/streamlit-1.31-red)

---

## 🎯 Características

### 📈 Análisis Swing Trading
- **TOP 3 mejores oportunidades** en small/mid caps
- Score multi-criterio (0-150 puntos)
- Probabilidad de éxito estimada (30-85%)
- Entradas, stops y targets específicos
- Plan de compra con cantidades exactas

### 📊 Análisis de Cartera
- Sube tu cartera en CSV
- Análisis de posiciones actuales
- Recomendaciones para ampliar posiciones
- Justificación fundamentada

### 📤 Exportación
- **PDF descargable** con análisis completo
- **Envío a Telegram** (opcional)

---

## 🚀 Despliegue en Streamlit Cloud

### Opción 1: Deploy Directo (Recomendado)

1. **Fork este repositorio** en tu cuenta GitHub

2. **Ve a [Streamlit Cloud](https://share.streamlit.io/)**

3. **Conecta tu repositorio GitHub**

4. **Configura los secrets**:
   - Ve a Settings → Secrets
   - Añade tu API key:
   ```toml
   ANTHROPIC_API_KEY = "sk-ant-..."
   ```

5. **Deploy!**
   - La app estará disponible en: `https://tu-usuario-stock-radar.streamlit.app`

### Opción 2: Deploy Manual

```bash
# Clonar repo
git clone https://github.com/TU-USUARIO/stock-radar.git
cd stock-radar

# Instalar dependencias
pip install -r requirements.txt

# Configurar API key
export ANTHROPIC_API_KEY="sk-ant-..."

# Ejecutar localmente
streamlit run stock_radar_app.py
```

---

## 📋 Requisitos

### API Keys Necesarias

1. **Anthropic API Key** (obligatoria)
   - Obtener en: https://console.anthropic.com/
   - Modelo usado: Claude Sonnet 4
   - Costo aproximado: $0.10-0.30 por análisis

2. **Telegram Bot** (opcional, solo si quieres enviar notificaciones)
   - Crear bot: @BotFather en Telegram
   - Obtener Bot Token y Chat ID

### Formato CSV Cartera

Tu archivo CSV debe tener estas columnas:

```csv
Ticker,Acciones,Precio_Compra,Valor_Actual,Sector
AAPL,10,150.00,180.50,Technology
MSFT,5,280.00,390.25,Technology
KO,20,55.00,62.30,Consumer Staples
```

---

## 🛠️ Estructura del Proyecto

```
stock-radar/
├── stock_radar_app.py          # Aplicación principal
├── requirements.txt             # Dependencias
├── README.md                    # Este archivo
├── .streamlit/
│   └── config.toml             # Configuración Streamlit
├── prompts/
│   ├── prompt_swing_v3_1.txt   # Prompt swing trading
│   └── prompt_portfolio.txt    # Prompt análisis cartera
├── utils/
│   ├── data_fetcher.py         # Funciones Stooq/iShares
│   ├── pdf_generator.py        # Generación PDFs
│   └── telegram_sender.py      # Envío Telegram
└── .gitignore
```

---

## 🔐 Configuración de Secrets

### Streamlit Cloud

Archivo `.streamlit/secrets.toml`:

```toml
ANTHROPIC_API_KEY = "sk-ant-api03-xxxxx"

# Opcional: Telegram
TELEGRAM_BOT_TOKEN = "123456789:ABCdefGHIjklMNOpqrsTUVwxyz"
TELEGRAM_CHAT_ID = "123456789"
```

### Local

Crear archivo `.env`:

```bash
ANTHROPIC_API_KEY=sk-ant-api03-xxxxx
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_CHAT_ID=123456789
```

---

## 📊 Fuentes de Datos

La aplicación usa **solo fuentes públicas y gratuitas**:

1. **iShares ETF Holdings** (CSVs públicos)
   - IWM (Russell 2000)
   - IWC (Micro-Cap)
   - IJR (S&P Small-Cap)

2. **Stooq.com** (datos EOD gratuitos)
   - OHLCV diario
   - Histórico hasta 20+ años

3. **Claude Sonnet 4 API** (análisis)
   - Procesamiento de datos
   - Generación de insights
   - Ranking multi-criterio

---

## 💡 Uso de la Aplicación

### Análisis Swing Trading

1. Introduce capital disponible (€500-1000)
2. Click en **"Ejecutar Análisis Swing"**
3. Espera 30-60 segundos
4. Revisa TOP 3 oportunidades
5. Descarga PDF o envía a Telegram

### Análisis Cartera

1. Sube tu CSV con la cartera
2. Verifica la vista previa
3. Click en **"Analizar Cartera"**
4. Espera resultados
5. Revisa recomendaciones
6. Descarga PDF o envía a Telegram

---

## ⚠️ Disclaimer

Esta herramienta proporciona análisis basado en datos públicos y **no constituye asesoramiento financiero**.

- Las decisiones de inversión son responsabilidad del usuario
- Invierte solo capital que puedas permitirte perder
- Los rendimientos pasados no garantizan resultados futuros
- La información puede contener errores
- Consulta con un asesor financiero profesional

---

## 🐛 Solución de Problemas

### Error: "API key not found"
- Verifica que hayas configurado `ANTHROPIC_API_KEY` en secrets
- Formato correcto: `sk-ant-api03-...`

### Error al descargar ETF holdings
- iShares puede cambiar URLs
- Verificar conectividad
- Intentar más tarde

### Error en análisis
- Verificar API key válida
- Comprobar créditos API
- Revisar formato CSV cartera

---

## 📈 Roadmap

- [ ] Soporte para más ETFs (large caps, sectores)
- [ ] Histórico de análisis guardado
- [ ] Sistema de alertas automáticas
- [ ] Integración con brokers (solo lectura)
- [ ] Dashboard de performance
- [ ] Versión móvil optimizada

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas!

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📄 Licencia

MIT License - ver archivo LICENSE para detalles

---

## 👨‍💻 Autor

**Stock Radar** - Sistema de análisis de inversiones

- Powered by **Claude Sonnet 4** (Anthropic)
- Built with **Streamlit**
- Data from **Stooq** & **iShares**

---

## 📞 Soporte

¿Problemas o preguntas?

- Abre un Issue en GitHub
- Revisa la documentación
- Consulta los ejemplos

---

**⭐ Si te gusta este proyecto, dale una estrella en GitHub!**
