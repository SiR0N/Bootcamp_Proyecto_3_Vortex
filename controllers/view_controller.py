from flask import Blueprint, render_template, request
from datetime import datetime
from controllers.compare_controller import compare_latest_records
import requests

view_bp = Blueprint("view", __name__, template_folder="../templates")

FASTAPI_URL = "http://localhost:8000"


def _cargar_zonas_indexadas():
    """Carga todas las zonas una sola vez y las indexa por id."""
    try:
        r = requests.get(f"{FASTAPI_URL}/zonas/?limit=1000", timeout=10)
        if r.status_code != 200:
            return {}
        return {z["id"]: z for z in r.json()}
    except Exception as e:
        print(f"Error cargando zonas: {e}")
        return {}


def get_mediciones_from_db(municipio=None, fecha=None, limit=500):
    """Obtiene mediciones de PostgreSQL vía FastAPI."""
    try:
        r = requests.get(f"{FASTAPI_URL}/mediciones/", params={"limit": limit}, timeout=10)
        if r.status_code != 200:
            return []
        mediciones = r.json()

        zonas_idx = _cargar_zonas_indexadas()
        resultados = []

        for m in mediciones:
            zona = zonas_idx.get(m.get("zona_id"), {})
            estacion = zona.get("estacion_id", "")
            nombre   = zona.get("nombre", "") or ""

            # Filtro por municipio: comparamos contra NOMBRE y estacion_id
            if municipio:
                mun_lower = municipio.lower()
                if mun_lower not in nombre.lower() and mun_lower not in estacion.lower():
                    continue

            if fecha:
                m_fecha = (m.get("fecha") or "")[:10]
                if fecha not in m_fecha:
                    continue

            resultados.append({
                "estacion_id":       estacion,
                "municipio":         nombre or estacion,
                "codigo_municipio":  estacion,
                "fecha":             m.get("fecha"),
                "temperatura":       m.get("temperatura"),
                "humedad":           m.get("humedad"),
                "viento":            m.get("viento"),
                "lluvia":            m.get("lluvia"),
                "presion":           m.get("presion"),
                "fuente":            m.get("fuente"),
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
    if request.method == "GET":
        return render_template("consulta.html", registros=get_mediciones_from_db())

    municipio = request.form.get("municipio", "").strip() or None

    fecha_raw = request.form.get("fecha", "").strip()
    fecha_filter = None
    if fecha_raw:
        try:
            fecha_filter = datetime.strptime(fecha_raw, "%Y-%m-%d").strftime("%Y-%m-%d")
        except ValueError:
            fecha_filter = None

    registros = get_mediciones_from_db(municipio=municipio, fecha=fecha_filter)
    return render_template("consulta.html", registros=registros)


@view_bp.route("/comparar", methods=["GET", "POST"])
def comparar():
    if request.method == "GET":
        return render_template("comparar.html", resultado=None)

    municipio = request.form.get("municipio", "").strip()
    fecha_html = request.form.get("fecha", "").strip()

    if not municipio:
        return render_template("comparar.html", resultado={"success": False, "message": "Debes introducir un municipio."})

    resultado = compare_latest_records(municipio, fecha_html)
    return render_template("comparar.html", resultado=resultado)