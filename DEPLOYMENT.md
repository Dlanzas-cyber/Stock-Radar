# 🚀 GUÍA DE DEPLOYMENT - STOCK RADAR

## Paso a Paso para Desplegar en Streamlit Cloud

### ✅ PASO 1: Preparar Repositorio GitHub

1. **Crear nuevo repositorio en GitHub**:
   ```
   Nombre: stock-radar
   Descripción: Sistema Inteligente de Análisis de Inversiones
   Visibilidad: Público o Privado
   ```

2. **Subir archivos**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Stock Radar v1.0"
   git branch -M main
   git remote add origin https://github.com/TU-USUARIO/stock-radar.git
   git push -u origin main
   ```

### ✅ PASO 2: Obtener API Key de Anthropic

1. **Ir a**: https://console.anthropic.com/
2. **Crear cuenta** (si no tienes)
3. **API Keys** → **Create Key**
4. **Copiar** la key (empieza con `sk-ant-api03-...`)
5. **Guardar** en lugar seguro

### ✅ PASO 3: Desplegar en Streamlit Cloud

1. **Ir a**: https://share.streamlit.io/

2. **Sign in con GitHub**

3. **New app** → Seleccionar:
   - Repository: `TU-USUARIO/stock-radar`
   - Branch: `main`
   - Main file path: `stock_radar_app.py`

4. **Advanced settings** → **Secrets**:
   ```toml
   ANTHROPIC_API_KEY = "sk-ant-api03-XXXXX"
   ```

5. **Deploy!**

6. **Esperar 2-3 minutos**

7. **Tu app estará en**:
   ```
   https://TU-USUARIO-stock-radar.streamlit.app
   ```

### ✅ PASO 4: Probar la Aplicación

1. **Abrir la URL** de tu app

2. **Probar Swing Trading**:
   - Capital: €1000
   - Click "Ejecutar Análisis Swing"
   - Esperar resultados
   - Descargar PDF

3. **Probar Análisis Cartera**:
   - Subir `example_portfolio.csv`
   - Click "Analizar Cartera"
   - Revisar recomendaciones

### ✅ PASO 5: Configurar Telegram (Opcional)

1. **Crear Bot**:
   - Abrir Telegram
   - Buscar: @BotFather
   - Comando: `/newbot`
   - Nombre: "Stock Radar Bot"
   - Username: `stock_radar_bot`
   - **Copiar Bot Token**

2. **Obtener Chat ID**:
   - Buscar: @userinfobot
   - Comando: `/start`
   - **Copiar tu Chat ID**

3. **Actualizar Secrets**:
   ```toml
   ANTHROPIC_API_KEY = "sk-ant-api03-XXXXX"
   TELEGRAM_BOT_TOKEN = "123456789:ABCdefGHIjklMNOpqrs"
   TELEGRAM_CHAT_ID = "123456789"
   ```

4. **Reiniciar app** en Streamlit Cloud

### ✅ PASO 6: Personalizar (Opcional)

Editar `stock_radar_app.py`:

1. **Cambiar título**:
   ```python
   st.markdown('<h1 class="main-title">📡 TU NOMBRE</h1>', ...)
   ```

2. **Ajustar colores** (CSS en el archivo)

3. **Modificar disclaimer**

4. **Añadir logo** (si tienes)

5. **Commit y push**:
   ```bash
   git add stock_radar_app.py
   git commit -m "Personalización"
   git push
   ```

6. **Streamlit Cloud** auto-redeploy

---

## 🐛 Solución de Problemas

### Error: "ModuleNotFoundError"
**Solución**: Verificar `requirements.txt` tiene todas las dependencias

### Error: "API key not found"
**Solución**: 
1. Settings → Secrets en Streamlit Cloud
2. Copiar exactamente: `ANTHROPIC_API_KEY = "sk-ant-..."`
3. Save
4. Reboot app

### App muy lenta
**Solución**: 
- Normal en primer uso (carga librerías)
- Análisis tarda 30-60 segundos
- Si >2 min, revisar logs en Streamlit Cloud

### Error al descargar datos ETF
**Solución**:
- iShares puede cambiar URLs
- Verificar conexión internet
- Intentar en 1 hora

---

## 📊 Costos Estimados

### API de Anthropic

- **Modelo**: Claude Sonnet 4
- **Costo por análisis**: $0.10 - $0.30
- **Plan gratuito**: $5 crédito inicial
- **Análisis con $5**: ~20-50 análisis

### Streamlit Cloud

- **Plan Community**: **GRATIS**
- **Límites**:
  - 1 app pública
  - 1GB RAM
  - 1 CPU compartido
- **Suficiente para**: Uso personal/pequeño equipo

### Total

- **Deploy**: $0
- **Uso mensual**: $5-20 (según frecuencia análisis)

---

## 🔄 Actualización de la App

### Modificar código:

```bash
# Editar archivos
nano stock_radar_app.py

# Commit
git add .
git commit -m "Descripción cambios"
git push

# Streamlit Cloud auto-redeploy en 1-2 min
```

### Actualizar secrets:

1. Streamlit Cloud → Tu app
2. Settings → Secrets
3. Editar
4. Save
5. Reboot app

---

## 📱 Acceso Móvil

La app funciona perfecto en móvil:

1. **Abrir**: `https://tu-app.streamlit.app`
2. **Añadir a pantalla inicio** (Chrome/Safari)
3. **Usar como app nativa**

---

## ✅ Checklist Final

Antes de compartir la app:

- [ ] App desplegada y funcionando
- [ ] API key configurada
- [ ] Probado análisis swing
- [ ] Probado análisis cartera
- [ ] PDF descargable funciona
- [ ] Telegram configurado (si aplica)
- [ ] README actualizado
- [ ] Disclaimer visible
- [ ] Logs sin errores

---

## 🎉 ¡Listo!

Tu app Stock Radar está lista para usar.

**URL de tu app**: `https://TU-USUARIO-stock-radar.streamlit.app`

Comparte con tu equipo o úsala personalmente.

---

**¿Problemas?** Revisa los logs en Streamlit Cloud o abre un Issue en GitHub.
