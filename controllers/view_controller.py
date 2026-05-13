from flask import Blueprint, render_template, request
from datetime import datetime
from controllers.compare_controller import compare_latest_records
import requests

view_bp = Blueprint("view", __name__, template_folder="../templates")

FASTAPI_URL = "http://localhost:8000"


def get_mediciones_from_db(municipio=None, fecha=None, limit=500):
    """Obtiene mediciones de PostgreSQL via FastAPI"""
    try:
        response = requests.get(f"{FASTAPI_URL}/mediciones/", params={"limit": limit}, timeout=10)
        if response.status_code != 200:
            return []

        mediciones = response.json()

        resultados = []
        for m in mediciones:
            zona_response = requests.get(f"{FASTAPI_URL}/zonas/{m.get('zona_id')}", timeout=5)
            zona_nombre = zona_response.json().get("estacion_id", "") if zona_response.status_code == 200 else ""

            if municipio:
                if municipio.lower() not in zona_nombre.lower():
                    continue

            if fecha:
                m_fecha = m.get("fecha", "")[:10] if m.get("fecha") else ""
                if fecha not in m_fecha:
                    continue

            resultados.append({
                "estacion_id": zona_nombre,
                "fecha": m.get("fecha"),
                "temperatura": m.get("temperatura"),
                "humedad": m.get("humedad"),
                "viento": m.get("viento"),
                "lluvia": m.get("lluvia"),
                "presion": m.get("presion"),
                "fuente": m.get("fuente")
            })

        return resultados
    except Exception as e:
        print(f"Error consultando FastAPI: {e}")
        return []


@view_bp.route("/")
def index():
    return render_template("index.html")


@view_bp.route("/registro")
def registro():
    return render_template("registro.html")


@view_bp.route("/registro_usuario")
def registro_usuario():
    return render_template("registro_usuario.html")


@view_bp.route("/login")
def login():
    return render_template("login.html")


@view_bp.route("/api")
def api_view():
    return render_template("api.html")


@view_bp.route("/consulta", methods=["GET", "POST"])
def consulta():
    """Muestra el histórico filtrado por municipio y fecha desde PostgreSQL"""
    if request.method == "GET":
        registros = get_mediciones_from_db()
        return render_template("consulta.html", registros=registros)

    municipio = request.form.get("municipio", "").strip()
    if not municipio:
        municipio = None

    fecha_raw = request.form.get("fecha", "").strip()
    fecha_formateada = None

    if fecha_raw:
        try:
            fecha_obj = datetime.strptime(fecha_raw, "%Y-%m-%d")
            fecha_formateada = fecha_obj.strftime("%d/%m/%Y")
        except ValueError:
            fecha_formateada = None

    registros = get_mediciones_from_db(municipio=municipio, fecha=fecha_formateada)

    return render_template("consulta.html", registros=registros)


@view_bp.route("/comparar", methods=["GET", "POST"])
def comparar():
    """Realiza la comparativa entre JSON y API."""
    if request.method == "GET":
        return render_template("comparar.html", resultado=None)

    municipio = request.form.get("municipio", "").strip()
    fecha_html = request.form.get("fecha", "").strip()

    if not municipio:
        return render_template("comparar.html", resultado={"success": False, "message": "Debes introducir un municipio."})

    resultado = compare_latest_records(municipio, fecha_html)
    return render_template("comparar.html", resultado=resultado)