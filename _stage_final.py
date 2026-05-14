import subprocess, os

os.chdir("C:/Users/JUAN/Desktop/Proyectos/Bootcamp_Proyecto_3_Vortex")

# Reset completo
subprocess.run(["git", "reset"], capture_output=True)

# Eliminar el archivo si existe
if os.path.exists("REVIEW_PR65.md"):
    os.remove("REVIEW_PR65.md")
    print("  BORRADO: REVIEW_PR65.md")

# SOLO stagear archivos de código reales
archivos = [
    ".gitignore",
    "README_INICIO.md",
    "controllers/api_controller.py",
    "controllers/compare_controller.py",
    "controllers/view_controller.py",
    "data/registros_climaticos.json",
    "data/registros_climaticos_normalizados.json",
    "data/usuarios.json",
    "etl/pipeline.py",
    "services/alert_service.py",
    "services/normalizer_service.py",
    "services/weather_api_service.py",
    "static/css/index.css",
    "static/css/style.css",
    "static/js/index.js",
    "templates/api.html",
    "templates/comparar.html",
    "templates/consulta.html",
    "templates/index.html",
    "templates/login.html",
    "templates/registro.html",
    "templates/registro_usuario.html",
]

for f in archivos:
    if os.path.exists(f):
        subprocess.run(["git", "add", f], capture_output=True)
        print(f"  STAGE: {f}")

print("\n=== STATUS FINAL ===")
subprocess.run(["git", "status", "-s"])
print("\n=== LISTO PARA COMMIT + PUSH ===")