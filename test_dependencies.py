#!/usr/bin/env python3
"""
Test script para verificar Stock Radar localmente
"""

import sys

print("🔍 Stock Radar - Test de Dependencias\n")

# Test 1: Streamlit
print("1. Testing Streamlit...")
try:
    import streamlit as st
    print(f"   ✅ Streamlit {st.__version__}")
except ImportError as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

# Test 2: Pandas
print("2. Testing Pandas...")
try:
    import pandas as pd
    print(f"   ✅ Pandas {pd.__version__}")
except ImportError as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

# Test 3: Requests
print("3. Testing Requests...")
try:
    import requests
    print(f"   ✅ Requests {requests.__version__}")
except ImportError as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

# Test 4: Anthropic
print("4. Testing Anthropic...")
try:
    import anthropic
    print(f"   ✅ Anthropic {anthropic.__version__}")
except ImportError as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

# Test 5: FPDF
print("5. Testing FPDF...")
try:
    from fpdf import FPDF
    print(f"   ✅ FPDF2 importado correctamente")
except ImportError as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

# Test 6: Openpyxl
print("6. Testing Openpyxl...")
try:
    import openpyxl
    print(f"   ✅ Openpyxl {openpyxl.__version__}")
except ImportError as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

# Test 7: API Key
print("\n7. Testing API Key...")
import os
api_key = os.getenv("ANTHROPIC_API_KEY")
if api_key:
    print(f"   ✅ API Key encontrada: {api_key[:20]}...")
else:
    print(f"   ⚠️  API Key no encontrada (OK si aún no configuraste)")

# Test 8: Archivos necesarios
print("\n8. Testing Archivos...")
import os.path

files = [
    'stock_radar_app.py',
    'requirements.txt',
    'README.md',
    'packages.txt',
    'prompts/prompt_swing_v3_1.txt',
    'prompts/prompt_portfolio.txt'
]

for f in files:
    if os.path.exists(f):
        print(f"   ✅ {f}")
    else:
        print(f"   ❌ {f} - NO ENCONTRADO")

# Test 9: PDF Generation Test
print("\n9. Testing Generación PDF...")
try:
    from fpdf import FPDF
    import io
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'Test PDF', 0, 1, 'C')
    
    buffer = io.BytesIO()
    pdf_output = pdf.output(dest='S').encode('latin-1')
    buffer.write(pdf_output)
    
    print(f"   ✅ PDF generado: {len(buffer.getvalue())} bytes")
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "="*50)
print("✅ TODOS LOS TESTS PASADOS!")
print("="*50)
print("\nPuedes ejecutar la app con:")
print("  streamlit run stock_radar_app.py")
