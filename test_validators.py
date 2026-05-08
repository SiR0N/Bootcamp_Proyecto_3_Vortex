"""
Test rápido para validar normalizador
"""
import sys
import os

# Añadir la raíz del proyecto al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.validators import (
    validar_temperatura,
    validar_humedad,
    validar_viento,
    validar_lluvia,
    validate_weather_data
)

# Test 1: Temperatura válida
print("Test 1: Temperatura válida (25):", validar_temperatura(25))

# Test 2: Temperatura fuera de rango
print("Test 2: Temperatura fuera de rango (65):", validar_temperatura(65))

# Test 3: Humedad válida
print("Test 3: Humedad válida (50):", validar_humedad(50))

# Test 4: Registro completo válido
registro_valido = {
    "estacion_id": "EST-1234",
    "fecha": "29/04/2026",
    "temperatura": 25.5,
    "humedad": 60,
    "viento": 15.0,
    "lluvia": 0.0
}
print("Test 4: Registro completo válido:", validate_weather_data(registro_valido))

# Test 5: Registro inválido
registro_invalido = {
    "estacion_id": "EST-1234",
    "fecha": "29/04/2026",
    "temperatura": 65,  # Fuera de rango
    "humedad": 60,
    "viento": 15.0,
    "lluvia": 0.0
}
print("Test 5: Registro inválido (temp=65):", validate_weather_data(registro_invalido))

print("\n✅ Tests completados!")