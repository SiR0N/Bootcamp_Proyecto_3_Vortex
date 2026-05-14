import subprocess, os

os.chdir("C:/Users/JUAN/Desktop/Proyectos/Bootcamp_Proyecto_3_Vortex")

# Ver los últimos 3 commits de fix/integration (los que subió después)
print("=== ÚLTIMOS 5 COMMITS DE fix/integration ===")
r = subprocess.run(
    ["git", "log", "--oneline", "origin/fix/integration", "-5"],
    capture_output=True, text=True, encoding="utf-8", errors="replace"
)
print(r.stdout)

# Ver el diff entre el penúltimo commit y el último (1c4c131)
print("\n=== DIFF del último commit (1c4c131) ===")
r2 = subprocess.run(
    ["git", "diff", "1c4c131^..1c4c131"],
    capture_output=True, text=True, encoding="utf-8", errors="replace"
)
print(r2.stdout[:3000])

print("\n=== DIFF del commit anterior (5fb1e51) ===")
r3 = subprocess.run(
    ["git", "diff", "5fb1e51^..5fb1e51"],
    capture_output=True, text=True, encoding="utf-8", errors="replace"
)
print(r3.stdout[:3000])

# Ver el diff entre nuestra rama y la última de Elizabeth
print("\n=== NUESTRO HEAD vs ELIZABETH HEAD ===")
r4 = subprocess.run(
    ["git", "diff", "--stat", "origin/feat/implementations", "origin/fix/integration"],
    capture_output=True, text=True, encoding="utf-8", errors="replace"
)
print("Archivos que difieren:", r4.stdout[:1000])