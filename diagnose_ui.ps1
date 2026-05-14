$ErrorActionPreference = "SilentlyContinue"

Write-Host "=== DIAGNOSTICO INTERFAZ ===" -ForegroundColor Yellow

# 1. Verificar servidores
Write-Host "`n[1] ESTADO SERVIDORES:" -ForegroundColor Cyan
$fastapi_ok = $false
$flask_ok = $false

try {
    $r = Invoke-WebRequest -Uri "http://localhost:8000/" -UseBasicParsing -TimeoutSec 5
    $fastapi_ok = $r.StatusCode -eq 200
} catch {}

try {
    $r = Invoke-WebRequest -Uri "http://localhost:5000/" -UseBasicParsing -TimeoutSec 5
    $flask_ok = $r.StatusCode -eq 200
} catch {}

if ($fastapi_ok) { Write-Host "  FastAPI (8000): OK" -ForegroundColor Green } else { Write-Host "  FastAPI (8000): CAIDO" -ForegroundColor Red }
if ($flask_ok) { Write-Host "  Flask (5000): OK" -ForegroundColor Green } else { Write-Host "  Flask (5000): CAIDO" -ForegroundColor Red }

# 2. Si FastAPI caido, arrancarlo
if (-not $fastapi_ok) {
    Write-Host "`n[2] REARRANCANDO FastAPI..." -ForegroundColor Yellow
    $job1 = Start-Job -ScriptBlock {
        Set-Location "C:\Users\JUAN\Desktop\Proyectos\Bootcamp_Proyecto_3_Vortex"
        python -c "import uvicorn; uvicorn.run('api.main:app', host='0.0.0.0', port=8000, log_level='warning')"
    }
    Start-Sleep 5
    try {
        $r = Invoke-WebRequest -Uri "http://localhost:8000/" -UseBasicParsing -TimeoutSec 5
        $fastapi_ok = $r.StatusCode -eq 200
        Write-Host "  FastAPI REARRANCADO: OK" -ForegroundColor Green
    } catch {
        Write-Host "  FastAPI REARRANCADO: FALLO - $($_.Exception.Message)" -ForegroundColor Red
    }
}

# 3. Si Flask caido, arrancarlo
if (-not $flask_ok) {
    Write-Host "`n[3] REARRANCANDO Flask..." -ForegroundColor Yellow
    $job2 = Start-Job -ScriptBlock {
        Set-Location "C:\Users\JUAN\Desktop\Proyectos\Bootcamp_Proyecto_3_Vortex"
        python -c "from app import app; app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)"
    }
    Start-Sleep 5
    try {
        $r = Invoke-WebRequest -Uri "http://localhost:5000/" -UseBasicParsing -TimeoutSec 5
        $flask_ok = $r.StatusCode -eq 200
        Write-Host "  Flask REARRANCADO: OK" -ForegroundColor Green
    } catch {
        Write-Host "  Flask REARRANCADO: FALLO - $($_.Exception.Message)" -ForegroundColor Red
    }
}

# 4. Test completo de endpoints
Write-Host "`n[4] TESTING ENDPOINTS:" -ForegroundColor Cyan
$tests = @(
    @{ Url = "http://localhost:5000/"; Name = "Flask / (index)" },
    @{ Url = "http://localhost:5000/registro"; Name = "Flask /registro" },
    @{ Url = "http://localhost:5000/consulta"; Name = "Flask /consulta" },
    @{ Url = "http://localhost:5000/api"; Name = "Flask /api" },
    @{ Url = "http://localhost:5000/login"; Name = "Flask /login" },
    @{ Url = "http://localhost:5000/registro_usuario"; Name = "Flask /registro_usuario" },
    @{ Url = "http://localhost:8000/"; Name = "FastAPI /" },
    @{ Url = "http://localhost:8000/zonas/"; Name = "FastAPI /zonas/" },
    @{ Url = "http://localhost:8000/mediciones/"; Name = "FastAPI /mediciones/" },
    @{ Url = "http://localhost:8000/docs"; Name = "FastAPI /docs" }
)

$errores = @()
foreach ($t in $tests) {
    try {
        $r = Invoke-WebRequest -Uri $t.Url -UseBasicParsing -TimeoutSec 10
        if ($r.StatusCode -eq 200) {
            Write-Host "  [OK] $($t.Name) -> 200" -ForegroundColor Green
        } else {
            Write-Host "  [WARN] $($t.Name) -> $($r.StatusCode)" -ForegroundColor Yellow
            $errores += "$($t.Name): $($r.StatusCode)"
        }
    } catch {
        Write-Host "  [FAIL] $($t.Name): $($_.Exception.Message)" -ForegroundColor Red
        $errores += "$($t.Name): $($_.Exception.Message)"
    }
}

# 5. Verificar recursos estáticos
Write-Host "`n[5] RECURSOS ESTATICOS:" -ForegroundColor Cyan
$static_tests = @(
    "http://localhost:5000/static/css/index.css",
    "http://localhost:5000/static/css/auth.css",
    "http://localhost:5000/static/js/index.js",
    "http://localhost:5000/static/img/logo_vortex.png"
)
foreach ($url in $static_tests) {
    try {
        $r = Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 5
        $name = ($url -split '/')[-1]
        Write-Host "  [OK] $name -> $($r.StatusCode) ($($r.RawContentLength) bytes)" -ForegroundColor Green
    } catch {
        $name = ($url -split '/')[-1]
        Write-Host "  [FAIL] $name: $($_.Exception.Message)" -ForegroundColor Red
    }
}

# 6. Verificar si hay errores en template rendering
Write-Host "`n[6] TEST TEMPLATE (Flask /):" -ForegroundColor Cyan
try {
    $r = Invoke-WebRequest -Uri "http://localhost:5000/" -UseBasicParsing -TimeoutSec 10
    $html = $r.Content
    if ($html -match "logo_vortex") { Write-Host "  [OK] Logo encontrado" -ForegroundColor Green } else { Write-Host "  [WARN] Logo NO encontrado" -ForegroundColor Yellow }
    if ($html -match "mainTitle") { Write-Host "  [OK] mainTitle encontrado" -ForegroundColor Green } else { Write-Host "  [WARN] mainTitle NO encontrado" -ForegroundColor Yellow }
    if ($html -match "temperature") { Write-Host "  [OK] temperature elemento encontrado" -ForegroundColor Green } else { Write-Host "  [WARN] temperature NO encontrado" -ForegroundColor Yellow }
    if ($html -match "VORTEX") { Write-Host "  [OK] VORTEX branding encontrado" -ForegroundColor Green } else { Write-Host "  [WARN] VORTEX branding NO encontrado" -ForegroundColor Yellow }
    if ($html -match "error|Error|ERROR") { Write-Host "  [WARN] Posibles errores en HTML" -ForegroundColor Yellow }
} catch {
    Write-Host "  [FAIL] Error al cargar index: $($_.Exception.Message)" -ForegroundColor Red
}

if ($errores.Count -gt 0) {
    Write-Host "`n=== ERRORES ENCONTRADOS ===" -ForegroundColor Red
    $errores | ForEach-Object { Write-Host "  - $_" -ForegroundColor Red }
} else {
    Write-Host "`n=== TODO OK ===" -ForegroundColor Green
}

Write-Host "`n=== ABRIENDO NAVEGADOR ===" -ForegroundColor Yellow
[System.Diagnostics.Process]::Start("http://localhost:5000/") | Out-Null