import subprocess, os

os.chdir("C:/Users/JUAN/Desktop/Proyectos/Bootcamp_Proyecto_3_Vortex")

# Deshacer el último commit pero mantener los cambios
print("=== RESETANDO ULTIMO COMMIT ===")
subprocess.run(["git", "reset", "--soft", "HEAD~1"])

# Eliminar el archivo del repo y del disco
if os.path.exists("REVIEW_PR65.md"):
    os.remove("REVIEW_PR65.md")
    print("  BORRADO: REVIEW_PR65.md")

# Verificar status
print("\n=== STATUS ===")
result = subprocess.run(["git", "status", "-s"], capture_output=True, text=True)
print(result.stdout)

print("=== LISTO - Documento eliminado, otros cambios intactos ===")