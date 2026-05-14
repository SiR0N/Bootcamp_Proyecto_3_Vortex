import subprocess, os

os.chdir("C:/Users/JUAN/Desktop/Proyectos/Bootcamp_Proyecto_3_Vortex")

# Ver el diff de los últimos 3 commits de Elizabeth
commits = ["34c6b43", "cebc70a"]

for commit in commits:
    print(f"\n{'='*70}")
    print(f"COMMIT: {commit}")
    print(f"{'='*70}")
    r = subprocess.run(
        ["git", "show", "--stat", commit],
        capture_output=True, text=True, encoding="utf-8", errors="replace"
    )
    print(r.stdout[:1500])
    
    # Ver los archivos específicos
    if commit == "34c6b43":
        print("\n=== CONTENIDO DE api/routes/zonas.py ===")
        r2 = subprocess.run(
            ["git", "show", f"{commit}:api/routes/zonas.py"],
            capture_output=True, text=True, encoding="utf-8", errors="replace"
        )
        with open("C:/tmp/elizabeth_zonas.py", "w", encoding="utf-8") as f:
            f.write(r2.stdout)
        print("Guardado en C:/tmp/elizabeth_zonas.py")
        
    if commit == "cebc70a":
        print("\n=== CONTENIDO DE db/models/medicion.py ===")
        r3 = subprocess.run(
            ["git", "show", f"{commit}:db/models/medicion.py"],
            capture_output=True, text=True, encoding="utf-8", errors="replace"
        )
        with open("C:/tmp/elizabeth_medicion.py", "w", encoding="utf-8") as f:
            f.write(r3.stdout)
        print("Guardado en C:/tmp/elizabeth_medicion.py")