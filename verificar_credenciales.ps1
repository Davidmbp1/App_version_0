# Script para verificar y ayudar a encontrar las credenciales de Firebase

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Verificacion de Credenciales Firebase" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$targetPath = "backend\firebase-credentials.json"
if (Test-Path $targetPath) {
    Write-Host "Credenciales encontradas en: $targetPath" -ForegroundColor Green
    Write-Host ""
    Write-Host "Puedes ejecutar el script de subida ahora:" -ForegroundColor Yellow
    Write-Host 'python backend/upload_images_firebase.py --images-dir "web/images" --firebase-credentials "backend/firebase-credentials.json" --storage-bucket "foot-selfie---multiplatform.firebasestorage.app"' -ForegroundColor Cyan
    exit 0
}

Write-Host "No se encontraron credenciales en: $targetPath" -ForegroundColor Red
Write-Host ""

Write-Host "Buscando archivos de Firebase en Descargas..." -ForegroundColor Yellow
$downloadsPath = "$env:USERPROFILE\Downloads"
$firebaseFiles = Get-ChildItem -Path $downloadsPath -Filter "*firebase*adminsdk*.json" -ErrorAction SilentlyContinue

if ($firebaseFiles) {
    Write-Host ""
    Write-Host "Se encontraron archivos de Firebase en Descargas:" -ForegroundColor Green
    $firebaseFiles | ForEach-Object {
        Write-Host "  - $($_.Name)" -ForegroundColor White
    }
    Write-Host ""
    $copy = Read-Host "Quieres copiar el archivo mas reciente a backend/firebase-credentials.json? (s/n)"
    if ($copy -eq "s") {
        $latestFile = $firebaseFiles | Sort-Object LastWriteTime -Descending | Select-Object -First 1
        Copy-Item -Path $latestFile.FullName -Destination $targetPath -Force
        Write-Host ""
        Write-Host "Archivo copiado a: $targetPath" -ForegroundColor Green
        Write-Host ""
        Write-Host "Ahora puedes ejecutar el script de subida:" -ForegroundColor Yellow
        Write-Host 'python backend/upload_images_firebase.py --images-dir "web/images" --firebase-credentials "backend/firebase-credentials.json" --storage-bucket "foot-selfie---multiplatform.firebasestorage.app"' -ForegroundColor Cyan
    }
} else {
    Write-Host "No se encontraron archivos de Firebase en Descargas." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Para obtener las credenciales:" -ForegroundColor Yellow
    Write-Host "1. Ve a Firebase Console -> Project Settings -> Service Accounts" -ForegroundColor White
    Write-Host "2. Click en Generate new private key" -ForegroundColor White
    Write-Host "3. Guarda el archivo JSON descargado en: $targetPath" -ForegroundColor White
    Write-Host ""
    Write-Host "O ejecuta este script de nuevo despues de descargar el archivo." -ForegroundColor Yellow
}
