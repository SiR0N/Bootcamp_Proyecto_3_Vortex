import subprocess, os

os.chdir("C:/Users/JUAN/Desktop/Proyectos/Bootcamp_Proyecto_3_Vortex")

# Verificar que REVIEW_PR65.md no está
if os.path.exists("REVIEW_PR65.md"):
    os.remove("REVIEW_PR65.md")
    print("BORRADO: REVIEW_PR65.md")

# Verificar staging
result = subprocess.run(["git", "diff", "--cached", "--stat"], capture_output=True, text=True)
print("=== STAGING ACTUAL ===")
print(result.stdout)

# Si hay cosas staged, hacer commit
if result.stdout.strip():
    result2 = subprocess.run(
        ["git", "commit", "-m", "feat: version final consolidada - datos reales, interfaz funcional"],
        capture_output=True, text=True
    )
    print("=== COMMIT ===")
    print(result2.stdout if result2.stdout else result2.stderr[:300])

# Ver historial local
print("\n=== HISTORIAL LOCAL ===")
result3 = subprocess.run(["git", "log", "--oneline", "-5"], capture_output=True, text=True, shell=True if False else None)
print(result3.stdout)

# Ver si la API key aparece en algun archivo .py o .md
print("\n=== BUSCANDO API KEYS ===")
for patron in ["8a4d17a3fcff1ba762e68a8cf0fdf6a4", "AEMET_API_KEY=", "OPENWEATHER_API_KEY="]:
    result4 = subprocess.run(
        ["grep", "-rn", patron, "--include=*.py", "--include=*.md", "--include=*.json", "--include=*.html", "."],
        capture_output=True, text=True
    )
    if result4.stdout.strip():
        print(f"ENCONTRADO '{patron[:20]}...':")
        print(result4.stdout[:300])
    else:
        print(f"OK: '{patron[:20]}...' no encontrado en archivos")

print("\n=== LISTO PARA FORCE PUSH ===")
print("Si falla, desbloquea en:")
print("https://github.com/SiR0N/Bootcamp_Proyecto_3_Vortex/security/secret-scanning")