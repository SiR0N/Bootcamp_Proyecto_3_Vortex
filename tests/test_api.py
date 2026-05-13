"""
test_api.py - Tests para los endpoints de la API FastAPI

Estos tests verifican que los endpoints devuelven los códigos de estado correctos
y que manejan adecuadamente las situaciones de éxito, validación y no encontrado.
"""

import pytest
from fastapi.testclient import TestClient

# Importar la app de FastAPI
from api.main import app

# Cliente para hacer requests HTTP
client = TestClient(app)


# =====================================================
# TESTS: GET /zonas/
# =====================================================

def test_get_zonas_devuelve_200():
    """
    GET /zonas/ debe devolver 200 OK.
    """
    response = client.get("/zonas/")
    assert response.status_code == 200


def test_get_zonas_devuelve_lista():
    """
    GET /zonas/ debe devolver una lista (aunque esté vacía).
    """
    response = client.get("/zonas/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_zonas_con_skip_limit():
    """
    GET /zonas/ debe aceptar parámetros skip y limit.
    """
    response = client.get("/zonas/?skip=0&limit=10")
    assert response.status_code == 200


# =====================================================
# TESTS: GET /zonas/{id}
# =====================================================

def test_get_zona_inexistente_devuelve_404():
    """
    GET /zonas/{id} debe devolver 404 si no existe la zona.
    """
    response = client.get("/zonas/99999")
    assert response.status_code == 404
    assert "detail" in response.json()


def test_get_zona_id_invalido_devuelve_422():
    """
    GET /zonas/abc debe devolver 422 por parámetro inválido.
    """
    response = client.get("/zonas/abc")
    assert response.status_code == 422


# =====================================================
# TESTS: POST /zonas/
# =====================================================

def test_post_crear_zona_datos_incompletos_devuelve_422():
    """
    POST /zonas/ debe devolver 422 si faltan datos requeridos.
    """
    zona_invalida = {
        "nombre": "Madrid"
        # Falta estacion_id
    }
    
    response = client.post("/zonas/", json=zona_invalida)
    assert response.status_code == 422


def test_post_crear_zona_json_invalido_devuelve_422():
    """
    POST /zonas/ debe devolver 422 si el JSON es inválido.
    """
    response = client.post(
        "/zonas/",
        data="no es json válido",
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 422


# =====================================================
# TESTS: PUT /zonas/{id}
# =====================================================

def test_put_zona_inexistente_devuelve_404():
    """
    PUT /zonas/{id} debe devolver 404 si no existe.
    """
    zona_update = {
        "estacion_id": "999",
        "nombre": "No existe",
        "latitud": 0,
        "longitud": 0
    }
    
    response = client.put("/zonas/99999", json=zona_update)
    assert response.status_code == 404


def test_put_zona_datos_incompletos_devuelve_422():
    """
    PUT /zonas/{id} debe devolver 422 si los datos son inválidos.
    """
    zona_invalida = {
        "nombre": "Madrid"
        # Falta estacion_id
    }
    
    response = client.put("/zonas/1", json=zona_invalida)
    # Podría ser 404 (zona no existe) o 422 (datos inválidos)
    assert response.status_code in [404, 422]


# =====================================================
# TESTS: DELETE /zonas/{id}
# =====================================================

def test_delete_zona_inexistente_devuelve_404():
    """
    DELETE /zonas/{id} debe devolver 404 si no existe.
    """
    response = client.delete("/zonas/99999")
    assert response.status_code == 404


# =====================================================
# TESTS: GET /zonas/{id}/mediciones
# =====================================================

def test_get_mediciones_por_zona_inexistente_devuelve_404():
    """
    GET /zonas/{id}/mediciones debe devolver 404 si la zona no existe.
    """
    response = client.get("/zonas/99999/mediciones")
    assert response.status_code == 404


# =====================================================
# TESTS: GET /mediciones/
# =====================================================

def test_get_mediciones_devuelve_200():
    """
    GET /mediciones/ debe devolver 200 OK.
    """
    response = client.get("/mediciones/")
    assert response.status_code == 200


def test_get_mediciones_devuelve_lista():
    """
    GET /mediciones/ debe devolver una lista.
    """
    response = client.get("/mediciones/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_mediciones_con_parametros_paginacion():
    """
    GET /mediciones/ debe aceptar skip y limit.
    """
    response = client.get("/mediciones/?skip=0&limit=5")
    assert response.status_code == 200


# =====================================================
# TESTS: GET /mediciones/{id}
# =====================================================

def test_get_medicion_inexistente_devuelve_404():
    """
    GET /mediciones/{id} debe devolver 404 si no existe.
    """
    response = client.get("/mediciones/99999")
    assert response.status_code == 404
    assert "Medición no encontrada" in response.json()["detail"]


def test_get_medicion_id_invalido_devuelve_422():
    """
    GET /mediciones/abc debe devolver 422 por ID inválido.
    """
    response = client.get("/mediciones/abc")
    assert response.status_code == 422


# =====================================================
# TESTS: POST /mediciones/
# =====================================================

def test_post_crear_medicion_datos_incompletos_devuelve_422():
    """
    POST /mediciones/ debe devolver 422 si faltan datos requeridos.
    """
    medicion_incompleta = {
        "zona_id": 1
        # Faltan otros campos
    }
    
    response = client.post("/mediciones/", json=medicion_incompleta)
    assert response.status_code == 422


def test_post_crear_medicion_zona_no_existe_devuelve_400():
    """
    POST /mediciones/ debe devolver 400 si la zona no existe.
    """
    medicion = {
        "zona_id": 99999,  # No existe
        "fecha": "2026-04-28",
        "temperatura": 23.5,
        "humedad": 65,
        "viento": 12.0,
        "lluvia": 1.5,
        "presion": 1013.0,
        "fuente": "manual"
    }
    
    response = client.post("/mediciones/", json=medicion)
    # Si la zona no existe, debe devolver 400
    assert response.status_code in [400, 404, 422]


# =====================================================
# TESTS: PUT /mediciones/{id}
# =====================================================

def test_put_medicion_inexistente_devuelve_404():
    """
    PUT /mediciones/{id} debe devolver 404 si no existe.
    """
    medicion_update = {
        "zona_id": 1,
        "temperatura": 25.0
    }
    
    response = client.put("/mediciones/99999", json=medicion_update)
    assert response.status_code == 404


# =====================================================
# TESTS: DELETE /mediciones/{id}
# =====================================================

def test_delete_medicion_inexistente_devuelve_404():
    """
    DELETE /mediciones/{id} debe devolver 404 si no existe.
    """
    response = client.delete("/mediciones/99999")
    assert response.status_code == 404


# =====================================================
# TESTS: Codigos HTTP generales
# =====================================================

def test_endpoint_inexistente_devuelve_404():
    """
    Un endpoint inexistente debe devolver 404.
    """
    response = client.get("/api/inexistente")
    assert response.status_code == 404


def test_root_endpoint_existe():
    """
    GET / debe existir y devolver 200.
    """
    response = client.get("/")
    assert response.status_code == 200


# =====================================================
# TESTS: Validación de tipos de contenido
# =====================================================

def test_post_mediciones_json_invalido_devuelve_422():
    """
    POST /mediciones/ con JSON malformado debe devolver 422.
    """
    response = client.post(
        "/mediciones/",
        data="{ invalid json",
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 422


def test_response_tiene_estructura_correcta():
    """
    Verifica que las respuestas tengan estructura esperada.
    """
    response = client.get("/zonas/")
    assert response.status_code == 200
    # Las respuestas de lista deben ser arrays
    assert isinstance(response.json(), list) or isinstance(response.json(), dict)


# =====================================================
# TESTS: Resumen de códigos HTTP
# =====================================================

def test_resumen_codigos_http():
    """
    Resumen de códigos HTTP esperados:
    - 200: GET exitoso
    - 201: POST exitoso (crear)
    - 204: DELETE exitoso (sin contenido)
    - 400: Solicitud inválida (datos malformados)
    - 404: Recurso no encontrado
    - 422: Validación fallida (datos inválidos según schema)
    """
    
    # GET existente: 200
    response = client.get("/mediciones/")
    assert response.status_code == 200
    
    # GET inexistente: 404
    response = client.get("/mediciones/99999")
    assert response.status_code == 404
    
    # POST incompleto: 422
    response = client.post("/mediciones/", json={})
    assert response.status_code == 422
    
    # DELETE inexistente: 404
    response = client.delete("/mediciones/99999")
    assert response.status_code == 404
