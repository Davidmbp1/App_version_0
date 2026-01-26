# Script PowerShell para iniciar el servidor web local
# Uso: .\servidor_local.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Iniciando servidor web local..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verificar que Python esté disponible
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[OK] Python encontrado: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Python no está instalado o no está en el PATH" -ForegroundColor Red
    Write-Host "       Instala Python desde https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

# Verificar que existe el directorio web
if (-not (Test-Path "web")) {
    Write-Host "[ERROR] No se encontró el directorio 'web'" -ForegroundColor Red
    exit 1
}

# Iniciar el servidor
Write-Host "[INFO] Iniciando servidor en http://localhost:8000" -ForegroundColor Yellow
Write-Host "[INFO] Presiona Ctrl+C para detener el servidor" -ForegroundColor Yellow
Write-Host ""

python servidor_local.py
