@echo off
echo ========================================
echo   VORTEX - Arranque completo
echo ========================================
echo.

REM Activar entorno virtual si existe
if exist venv\Scripts\activate (
    echo Activando entorno virtual...
    call venv\Scripts\activate
) else (
    echo [WARN] No se encontro venv, usando Python global
)

REM Arrancar FastAPI en segundo plano
echo Arrancando FastAPI (puerto 8000)...
start "FastAPI" cmd /c "python -c "import uvicorn; uvicorn.run('api.main:app', host='0.0.0.0', port=8000, log_level='warning')" & echo FastAPI detenido"

REM Esperar a que FastAPI arranque
timeout /t 5 /nobreak >nul

REM Arrancar Flask
echo Arrancando Flask (puerto 5000)...
start "Flask" cmd /c "python app.py & echo Flask detenido"

echo.
echo ========================================
echo   SERVIDORES ARRANCADOS
echo   - Flask:  http://localhost:5000
echo   - FastAPI: http://localhost:8000
echo ========================================
echo.

REM Verificar
timeout /t 3 /nobreak >nul

powershell -Command "Invoke-WebRequest http://localhost:5000/ -UseBasicParsing | ForEach-Object { $_.StatusCode }" >nul 2>&1 && (
    echo [OK] Flask 5000 responde
) || echo [WARN] Flask no responde aun

powershell -Command "Invoke-WebRequest http://localhost:8000/ -UseBasicParsing | ForEach-Object { $_.StatusCode }" >nul 2>&1 && (
    echo [OK] FastAPI 8000 responde
) || echo [WARN] FastAPI no responde aun

echo.
echo Abriendo navegador en http://localhost:5000/
start http://localhost:5000/

echo.
echo Pulsa cualquier tecla para detener servidores...
pause >nul

REM Detener
taskkill /FI "WINDOWTITLE eq FastAPI" /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq Flask" /F >nul 2>&1
echo Servidores detenidos.