# Script para generar predicciones de callos para la herramienta web
# Usa solo las imágenes de TEST del CSV

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Generando predicciones para la web" -ForegroundColor Yellow
Write-Host "========================================`n" -ForegroundColor Cyan

# Activar entorno virtual
& "..\.venv\Scripts\Activate.ps1"

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: No se pudo activar el entorno virtual" -ForegroundColor Red
    Write-Host "Asegúrate de estar en: D:\PLesion_upch\Fase3_piloto_entrenamientos\callos-annotation-tool" -ForegroundColor Yellow
    exit 1
}

Write-Host "Entorno activado correctamente`n" -ForegroundColor Green

# Generar predicciones
python backend/export_predictions_folds.py `
  --lesion callos `
  --scenario all_weeks `
  --consensus-root "D:\PrevencionLesion-UPCH-Monitoreo\entrenamientos_2026\consensus_dataset_majority" `
  --out-root "D:\PLesion_upch\Fase3_piloto_entrenamientos\Entrenamientos_2026\output" `
  --web-dir "web" `
  --arch UnetPlusPlus `
  --encoder timm-efficientnet-b5 `
  --fold -1 `
  --threshold 0.50

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n========================================" -ForegroundColor Cyan
    Write-Host "¡Predicciones generadas exitosamente!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "`nArchivos generados:" -ForegroundColor Yellow
    Write-Host "  - web/data.js" -ForegroundColor White
    Write-Host "  - web/images/*.png (962 imagenes de test)" -ForegroundColor White
    Write-Host "`nAbre web/index.html en tu navegador para revisar las predicciones.`n" -ForegroundColor Yellow
} else {
    Write-Host "`nError al generar predicciones" -ForegroundColor Red
}
