# Script PowerShell para generar predicciones con folds
# Uso: .\generar_predicciones.ps1

param(
    [int]$Fold = -1,
    [double]$Threshold = 0.50,
    [string]$DataJsName = "data.js"
)

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Generando predicciones para la web" -ForegroundColor Yellow
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "Configuración:" -ForegroundColor Yellow
Write-Host "  Fold: $Fold (Ensemble)" -ForegroundColor White
Write-Host "  Threshold: $Threshold" -ForegroundColor White
Write-Host "  Archivo salida: $DataJsName`n" -ForegroundColor White

# Activar entorno virtual
& "..\.venv\Scripts\Activate.ps1"

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: No se pudo activar el entorno virtual" -ForegroundColor Red
    exit 1
}

# Generar predicciones
python backend/export_predictions_folds.py `
  --lesion callos `
  --scenario all_weeks `
  --consensus-root "D:\PrevencionLesion-UPCH-Monitoreo\entrenamientos_2026\consensus_dataset_majority" `
  --out-root "D:\PLesion_upch\Fase3_piloto_entrenamientos\Entrenamientos_2026\output" `
  --web-dir "web" `
  --arch UnetPlusPlus `
  --encoder timm-efficientnet-b5 `
  --fold $Fold `
  --threshold $Threshold `
  --data-js-name $DataJsName

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n========================================" -ForegroundColor Cyan
    Write-Host "¡Predicciones generadas exitosamente!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "`nAbre web/index.html en tu navegador para revisar las predicciones.`n" -ForegroundColor Yellow
} else {
    Write-Host "`nError al generar predicciones" -ForegroundColor Red
}
