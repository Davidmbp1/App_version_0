# Script PowerShell para activar entorno y contar imágenes
# Uso: .\activar_y_contar.ps1

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Activando entorno virtual..." -ForegroundColor Yellow
Write-Host "========================================`n" -ForegroundColor Cyan

# Activar entorno virtual
& "..\.venv\Scripts\Activate.ps1"

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: No se pudo activar el entorno virtual" -ForegroundColor Red
    Write-Host "Asegúrate de estar en: D:\PLesion_upch\Fase3_piloto_entrenamientos\callos-annotation-tool" -ForegroundColor Yellow
    exit 1
}

Write-Host "Entorno activado correctamente`n" -ForegroundColor Green

# Contar imágenes
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Contando imágenes de test..." -ForegroundColor Yellow
Write-Host "========================================`n" -ForegroundColor Cyan

python backend/count_test_images.py `
  --lesion callos `
  --scenario all_weeks `
  --consensus-root "D:\PrevencionLesion-UPCH-Monitoreo\entrenamientos_2026\consensus_dataset_majority"

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Proceso completado" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Cyan
