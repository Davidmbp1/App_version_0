# Script para configurar y subir imágenes a Firebase Storage
# Ejecutar desde: D:\PLesion_upch\Fase3_piloto_entrenamientos\callos-annotation-tool

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Configuración de Firebase Storage" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Paso 1: Activar entorno virtual
Write-Host "[1/5] Activando entorno virtual..." -ForegroundColor Yellow
$venvPath = "..\.venv\Scripts\activate"
if (Test-Path $venvPath) {
    & $venvPath
    Write-Host "  ✓ Entorno virtual activado" -ForegroundColor Green
} else {
    Write-Host "  ⚠ Entorno virtual no encontrado en ..\.venv\" -ForegroundColor Red
    Write-Host "  Creando nuevo entorno virtual..." -ForegroundColor Yellow
    python -m venv ..\.venv
    & $venvPath
    Write-Host "  ✓ Entorno virtual creado y activado" -ForegroundColor Green
}

# Paso 2: Instalar Firebase Admin SDK
Write-Host ""
Write-Host "[2/5] Instalando Firebase Admin SDK..." -ForegroundColor Yellow
pip install firebase-admin
if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✓ Firebase Admin SDK instalado" -ForegroundColor Green
} else {
    Write-Host "  ✗ Error al instalar Firebase Admin SDK" -ForegroundColor Red
    exit 1
}

# Paso 3: Verificar credenciales
Write-Host ""
Write-Host "[3/5] Verificando credenciales de Firebase..." -ForegroundColor Yellow
$credentialsPath = "backend\firebase-credentials.json"
if (Test-Path $credentialsPath) {
    Write-Host "  ✓ Credenciales encontradas en: $credentialsPath" -ForegroundColor Green
} else {
    Write-Host "  ✗ Credenciales NO encontradas en: $credentialsPath" -ForegroundColor Red
    Write-Host ""
    Write-Host "  Para obtener las credenciales:" -ForegroundColor Yellow
    Write-Host "  1. Ve a Firebase Console → Project Settings → Service Accounts" -ForegroundColor White
    Write-Host "  2. Click en 'Generate new private key'" -ForegroundColor White
    Write-Host "  3. Guarda el archivo JSON en: $credentialsPath" -ForegroundColor White
    Write-Host ""
    $continue = Read-Host "¿Quieres continuar de todos modos? (s/n)"
    if ($continue -ne "s") {
        exit 1
    }
}

# Paso 4: Verificar que existen imágenes
Write-Host ""
Write-Host "[4/5] Verificando imágenes..." -ForegroundColor Yellow
$imagesDir = "web\images"
if (Test-Path $imagesDir) {
    $imageCount = (Get-ChildItem -Path $imagesDir -Filter "*.png").Count
    Write-Host "  ✓ Encontradas $imageCount imágenes PNG" -ForegroundColor Green
} else {
    Write-Host "  ✗ No se encontró la carpeta: $imagesDir" -ForegroundColor Red
    exit 1
}

# Paso 5: Subir imágenes
Write-Host ""
Write-Host "[5/5] ¿Subir imágenes a Firebase Storage?" -ForegroundColor Yellow
Write-Host "  Esto puede tardar 10-30 minutos dependiendo de tu conexión" -ForegroundColor White
$upload = Read-Host "  ¿Continuar? (s/n)"
if ($upload -eq "s") {
    Write-Host ""
    Write-Host "  Subiendo imágenes..." -ForegroundColor Yellow
    Write-Host "  (Esto puede tardar varios minutos)" -ForegroundColor White
    Write-Host ""
    
    python backend/upload_images_firebase.py `
        --images-dir "web/images" `
        --firebase-credentials "backend/firebase-credentials.json" `
        --storage-bucket "foot-selfie---multiplatform.firebasestorage.app"
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "  ✓ Imágenes subidas exitosamente" -ForegroundColor Green
    } else {
        Write-Host ""
        Write-Host "  ✗ Error al subir imágenes" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "  ⏭ Saltando subida de imágenes" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "¡Configuración completada!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Próximos pasos:" -ForegroundColor Yellow
Write-Host "  1. Verifica que las reglas de Storage permitan acceso público a 'Revision de callos'" -ForegroundColor White
Write-Host "  2. Verifica en Firebase Console que las imágenes se subieron" -ForegroundColor White
Write-Host "  3. Prueba localmente abriendo web/index.html" -ForegroundColor White
Write-Host "  4. Haz push a GitHub (sin imágenes): git add . && git commit -m 'Firebase Storage' && git push" -ForegroundColor White
Write-Host ""
