# 🔧 STOCK RADAR - GUÍA DE SOLUCIÓN DE ERRORES

## ❌ Error: ModuleNotFoundError (reportlab, python-telegram-bot, etc)

### Causa
Dependencias que requieren bibliotecas del sistema no disponibles en Streamlit Cloud.

### ✅ Solución Aplicada

1. **Reemplazado `reportlab` por `fpdf2`**:
   - `fpdf2` es más ligero
   - No requiere dependencias del sistema
   - Compatible 100% con Streamlit Cloud

2. **Removido `python-telegram-bot`**:
   - Usamos `requests` directo a Telegram API
   - Más simple y sin dependencias pesadas

3. **Añadido `packages.txt`**:
   - Archivo para dependencias del sistema
   - Streamlit Cloud lo instala automáticamente

### Archivos Modificados

```
requirements.txt
├─ ANTES: reportlab==4.0.9
├─ AHORA: fpdf2==2.7.9
│
├─ ANTES: python-telegram-bot==20.7
└─ AHORA: (removido, usamos requests)

+ packages.txt (nuevo)
```

### Cómo Aplicar el Fix

1. **Si ya desplegaste y tienes el error**:
   ```bash
   # En tu repo local
   git pull origin main
   git add requirements.txt packages.txt stock_radar_app.py
   git commit -m "Fix: Reemplazar reportlab por fpdf2"
   git push
   
   # Streamlit Cloud auto-redeploy en 2-3 min
   ```

2. **Si aún no desplegaste**:
   - Los archivos ya tienen el fix
   - Deploy normalmente
   - Debería funcionar sin problemas

---

## ❌ Error: UnicodeEncodeError en PDF

### Causa
Caracteres especiales (€, ñ, acentos, emojis) no soportados en PDF.

### Síntomas
```
UnicodeEncodeError: 'latin-1' codec can't encode character '\u20ac'
```

### ✅ Solución Implementada

La función `generate_pdf()` ahora:

1. **Reemplaza caracteres especiales**:
   ```python
   text = text.replace('—', '-')
   text = text.replace('€', 'EUR ')
   text = text.replace('█', '#')
   # ... etc
   ```

2. **Convierte a latin-1 con fallback**:
   ```python
   text = text.encode('latin-1', 'replace').decode('latin-1')
   ```

3. **Resultado**: 
   - PDF se genera siempre
   - Caracteres especiales → equivalentes ASCII
   - Ejemplo: "€1,000" → "EUR 1,000"

---

## ❌ Error: API key not found

### Síntomas
```
❌ No se encontró API key de Anthropic. 
   Configura ANTHROPIC_API_KEY en secrets.
```

### ✅ Solución

**En Streamlit Cloud**:

1. Ve a tu app desplegada
2. Click **"Manage app"** (esquina inferior derecha)
3. **Settings** → **Secrets**
4. Añade:
   ```toml
   ANTHROPIC_API_KEY = "sk-ant-api03-XXXXX"
   ```
5. **Save**
6. **Reboot app**

**Localmente**:

```bash
# Opción 1: Variable de entorno
export ANTHROPIC_API_KEY="sk-ant-api03-XXXXX"

# Opción 2: Archivo .streamlit/secrets.toml
mkdir -p .streamlit
echo 'ANTHROPIC_API_KEY = "sk-ant-api03-XXXXX"' > .streamlit/secrets.toml
```

### Verificar API Key

```python
# Test rápido
import anthropic
import os

api_key = os.getenv("ANTHROPIC_API_KEY")
print(f"API Key: {api_key[:20]}...")  # Mostrar primeros 20 chars

client = anthropic.Anthropic(api_key=api_key)
# Si no da error, la key funciona
```

---

## ❌ Error: HTTPError 401 (Anthropic API)

### Síntomas
```
anthropic.APIError: 401 - Invalid API key
```

### Causas Posibles

1. **API key incorrecta**:
   - Verificar que empiece con `sk-ant-api03-`
   - Sin espacios al inicio/final
   - Copiar directamente de Anthropic Console

2. **API key expirada**:
   - Regenerar en: https://console.anthropic.com/
   - Actualizar en secrets

3. **Créditos agotados**:
   - Verificar balance en Anthropic Console
   - Añadir método de pago si necesario

### ✅ Solución

```bash
# 1. Ir a https://console.anthropic.com/
# 2. API Keys → Create new key
# 3. Copiar key completa
# 4. Actualizar secrets en Streamlit Cloud
# 5. Reboot app
```

---

## ❌ Error: Timeout al analizar

### Síntomas
```
🔍 Analizando mercado... (más de 2 minutos)
Error: Request timeout
```

### Causas

1. **Claude API saturado**: Alta demanda, respuesta lenta
2. **Prompt muy largo**: >100k tokens
3. **Red lenta**: Conexión usuario <-> Streamlit Cloud

### ✅ Solución

**Si persiste**:

1. **Reducir timeout**:
   ```python
   # En stock_radar_app.py
   message = client.messages.create(
       model="claude-sonnet-4-20250514",
       max_tokens=6000,  # Reducir de 8000
       timeout=90,  # Añadir timeout 90 seg
       messages=[...]
   )
   ```

2. **Simplificar prompt**:
   - Usar versión más corta
   - Menos detalles en output

3. **Reintentar**:
   - Click de nuevo después 1 min
   - Momento de menos tráfico

---

## ❌ Error: CSV no se lee correctamente

### Síntomas
```
❌ Error leyendo CSV: ...
KeyError: 'Ticker'
```

### Causa
CSV no tiene las columnas esperadas.

### ✅ Solución

Tu CSV debe tener **exactamente** estas columnas:

```csv
Ticker,Acciones,Precio_Compra,Valor_Actual,Sector,Euros_Invertidos
AAPL,10,150.00,180.50,Technology,1500.00
MSFT,5,280.00,390.25,Technology,1400.00
```

**Columnas obligatorias**:
- `Ticker` (texto)
- `Acciones` (número)
- `Precio_Compra` (número decimal)
- `Valor_Actual` (número decimal)

**Columnas opcionales**:
- `Sector` (texto)
- `Euros_Invertidos` (número)

**Formato**:
- Separador: coma (`,`)
- Decimales: punto (`.`) no coma
- Sin símbolos: `150.00` no `€150,00`

### Verificación

```python
import pandas as pd

df = pd.read_csv('tu_cartera.csv')
print(df.columns)  # Debe mostrar: ['Ticker', 'Acciones', ...]
print(df.head())   # Primeras filas
```

---

## ❌ Error: Telegram no envía mensaje

### Síntomas
```
❌ Error enviando a Telegram
```

### Causas

1. **Bot Token incorrecto**
2. **Chat ID incorrecto**
3. **Bot no iniciado** (no has hecho /start)
4. **Bot bloqueado** por Telegram

### ✅ Solución Paso a Paso

**1. Crear Bot**:
```
- Abrir Telegram
- Buscar: @BotFather
- Enviar: /newbot
- Seguir instrucciones
- COPIAR: Bot Token (123456789:ABCdef...)
```

**2. Obtener Chat ID**:
```
- Buscar tu bot creado
- Enviar: /start
- Buscar: @userinfobot
- Enviar: /start
- COPIAR: Tu ID (123456789)
```

**3. Verificar**:
```bash
# Test con curl
curl -X POST \
  https://api.telegram.org/bot<BOT_TOKEN>/sendMessage \
  -d chat_id=<CHAT_ID> \
  -d text="Test desde Stock Radar"

# Debe devolver: {"ok":true,...}
```

**4. En la app**:
- Bot Token: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`
- Chat ID: `123456789`
- Click "Enviar"

---

## ❌ Error: App muy lenta

### Síntomas
- Carga inicial >30 segundos
- Análisis tarda >2 minutos

### Causas

1. **Primera carga**: Streamlit instala dependencias
2. **Cold start**: App "dormida" por inactividad
3. **API Claude lenta**: Alta demanda

### ✅ Solución

**Normal**:
- Primera carga: 20-40 segundos OK
- Análisis: 30-90 segundos OK

**Si muy lento**:
1. Esperar 1 minuto completo
2. Refrescar página
3. Intentar en hora de menos tráfico
4. Verificar tu conexión internet

**Optimización**:
```python
# Cachear datos que no cambian
@st.cache_data
def download_etf_holdings(etf):
    # ...
    
@st.cache_resource
def get_anthropic_client(api_key):
    return anthropic.Anthropic(api_key=api_key)
```

---

## 🆘 ERROR NO LISTADO AQUÍ

### Qué hacer:

1. **Ver logs completos**:
   - Streamlit Cloud → Manage app → Logs
   - Copiar error completo

2. **Google el error**:
   - "streamlit [error message]"
   - "anthropic api [error]"

3. **Revisar código**:
   - Línea del error
   - ¿Qué cambió recientemente?

4. **Rollback**:
   ```bash
   git log  # Ver commits
   git reset --hard <commit_anterior>
   git push --force
   ```

5. **Crear Issue en GitHub**:
   - Descripción clara
   - Error completo
   - Pasos para reproducir

---

## ✅ CHECKLIST ANTES DE REPORTAR ERROR

Antes de decir "no funciona", verifica:

- [ ] API key configurada correctamente
- [ ] Secrets guardados y app reiniciada
- [ ] requirements.txt actualizado
- [ ] packages.txt en el repo
- [ ] CSV con formato correcto
- [ ] Esperado tiempo suficiente (30-90 seg)
- [ ] Internet funcionando
- [ ] Logs revisados
- [ ] Error reproducible (no aleatorio)

---

## 📞 SOPORTE

Si nada funciona:

1. **GitHub Issues**: Reportar con detalles
2. **Streamlit Forum**: https://discuss.streamlit.io/
3. **Anthropic Discord**: Para errores API
4. **Revisar documentación**:
   - Streamlit: https://docs.streamlit.io/
   - Anthropic: https://docs.anthropic.com/

---

**Última actualización**: Febrero 2026
**Versión**: 1.0.1 (fix reportlab)
