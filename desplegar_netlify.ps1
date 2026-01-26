# Script para preparar y desplegar en Netlify
# Uso: .\desplegar_netlify.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Despliegue en Netlify" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verificar que Git esté instalado
try {
    $gitVersion = git --version 2>&1
    Write-Host "[OK] Git encontrado: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Git no está instalado" -ForegroundColor Red
    Write-Host "       Descarga Git desde: https://git-scm.com/downloads" -ForegroundColor Yellow
    exit 1
}

# Verificar que existe el directorio web
if (-not (Test-Path "web")) {
    Write-Host "[ERROR] No se encontró el directorio 'web'" -ForegroundColor Red
    exit 1
}

# Verificar tamaño
Write-Host "[INFO] Verificando tamaño..." -ForegroundColor Yellow
python verificar_tamano.py
Write-Host ""

# Verificar si ya es un repositorio Git
$isGitRepo = Test-Path ".git"

if (-not $isGitRepo) {
    Write-Host "[INFO] Inicializando repositorio Git..." -ForegroundColor Yellow
    git init
    Write-Host "[OK] Repositorio inicializado" -ForegroundColor Green
} else {
    Write-Host "[OK] Repositorio Git ya existe" -ForegroundColor Green
}

# Crear .gitignore si no existe
if (-not (Test-Path ".gitignore")) {
    Write-Host "[INFO] Creando .gitignore..." -ForegroundColor Yellow
    @"
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
.venv/
venv/
ENV/

# Modelos (no subir checkpoints grandes)
models/
*.pth
*.pt

# Archivos temporales
.DS_Store
Thumbs.db
*.log

# IDE
.vscode/
.idea/
*.swp
*.swo
"@ | Out-File -FilePath ".gitignore" -Encoding UTF8
    Write-Host "[OK] .gitignore creado" -ForegroundColor Green
}

# Preguntar por el repositorio de GitHub
Write-Host ""
Write-Host "========================================" -ForegroundColor Yellow
Write-Host "PASO 1: Crear Repositorio en GitHub" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Yellow
Write-Host ""
Write-Host "¿Ya tienes un repositorio en GitHub creado?" -ForegroundColor Cyan
Write-Host "1. Sí, ya lo creé"
Write-Host "2. No, necesito crearlo primero"
$opcion = Read-Host "Selecciona (1 o 2)"

if ($opcion -eq "2") {
    Write-Host ""
    Write-Host "Pasos para crear el repositorio:" -ForegroundColor Cyan
    Write-Host "1. Ve a https://github.com/new" -ForegroundColor White
    Write-Host "2. Nombre del repositorio: (ej: callos-annotation-tool)" -ForegroundColor White
    Write-Host "3. Puede ser PÚBLICO o PRIVADO (ambos funcionan con Netlify)" -ForegroundColor White
    Write-Host "4. NO inicialices con README, .gitignore o licencia" -ForegroundColor White
    Write-Host "5. Click en 'Create repository'" -ForegroundColor White
    Write-Host ""
    $continuar = Read-Host "Presiona Enter cuando hayas creado el repositorio..."
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Yellow
Write-Host "PASO 2: Conectar con GitHub" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Yellow
Write-Host ""
$repoUrl = Read-Host "Ingresa la URL de tu repositorio (ej: https://github.com/usuario/repositorio.git)"

# Verificar si el remoto ya existe
$remoteExists = git remote -v 2>&1 | Select-String "origin"

if ($remoteExists) {
    Write-Host "[INFO] Remoto 'origin' ya existe" -ForegroundColor Yellow
    $cambiar = Read-Host "¿Deseas cambiarlo? (s/n)"
    if ($cambiar -eq "s") {
        git remote set-url origin $repoUrl
        Write-Host "[OK] Remoto actualizado" -ForegroundColor Green
    }
} else {
    git remote add origin $repoUrl
    Write-Host "[OK] Remoto agregado" -ForegroundColor Green
}

# Agregar archivos
Write-Host ""
Write-Host "[INFO] Agregando archivos..." -ForegroundColor Yellow
git add web/
git add .gitignore
git add README.md
git add DESPLIEGUE.md
git add RESUMEN_DESPLIEGUE.md
git add desplegar_netlify_permanente.md

# Verificar si hay cambios
$status = git status --porcelain
if ([string]::IsNullOrWhiteSpace($status)) {
    Write-Host "[INFO] No hay cambios nuevos para commitear" -ForegroundColor Yellow
    Write-Host "[INFO] Verificando si hay commits..." -ForegroundColor Yellow
    $hasCommits = git log --oneline 2>&1 | Select-String "."
    if (-not $hasCommits) {
        Write-Host "[INFO] No hay commits. Creando commit inicial..." -ForegroundColor Yellow
        git commit -m "Herramienta de anotación de callos - Despliegue Netlify"
        Write-Host "[OK] Commit inicial creado" -ForegroundColor Green
    }
} else {
    Write-Host "[INFO] Haciendo commit..." -ForegroundColor Yellow
    git commit -m "Herramienta de anotación de callos - Despliegue Netlify"
    Write-Host "[OK] Commit realizado" -ForegroundColor Green
}

# Verificar branch
$currentBranch = git branch --show-current 2>&1
if ($null -eq $currentBranch -or $currentBranch -eq "") {
    git branch -M main
    $currentBranch = "main"
}

Write-Host ""
Write-Host "[INFO] Branch actual: $currentBranch" -ForegroundColor Cyan

# Preguntar si hacer push
Write-Host ""
Write-Host "========================================" -ForegroundColor Yellow
Write-Host "PASO 3: Subir a GitHub" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Yellow
Write-Host ""
$hacerPush = Read-Host "¿Deseas hacer push al repositorio ahora? (s/n)"

if ($hacerPush -eq "s") {
    Write-Host "[INFO] Haciendo push..." -ForegroundColor Yellow
    try {
        git push -u origin $currentBranch
        Write-Host "[OK] Push completado exitosamente" -ForegroundColor Green
    } catch {
        Write-Host "[ERROR] Error al hacer push" -ForegroundColor Red
        Write-Host "       Posibles causas:" -ForegroundColor Yellow
        Write-Host "       - No tienes permisos en el repositorio" -ForegroundColor Yellow
        Write-Host "       - El repositorio no existe" -ForegroundColor Yellow
        Write-Host "       - Necesitas autenticarte (usuario/contraseña o token)" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "       Puedes hacer push manualmente más tarde con:" -ForegroundColor Cyan
        Write-Host "       git push -u origin $currentBranch" -ForegroundColor White
        exit 1
    }
} else {
    Write-Host "[INFO] Puedes hacer push más tarde con:" -ForegroundColor Yellow
    Write-Host "       git push -u origin $currentBranch" -ForegroundColor Cyan
}

# Instrucciones para Netlify
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "PASO 4: Configurar Netlify" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Ahora sigue estos pasos en Netlify:" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Ve a https://www.netlify.com" -ForegroundColor White
Write-Host "2. Crea una cuenta (puedes usar GitHub para login rápido)" -ForegroundColor White
Write-Host "3. Una vez dentro, click en 'Add new site' → 'Import an existing project'" -ForegroundColor White
Write-Host "4. Selecciona 'GitHub' y autoriza Netlify" -ForegroundColor White
Write-Host "5. Busca y selecciona tu repositorio: $repoUrl" -ForegroundColor White
Write-Host ""
Write-Host "6. Configuración del build:" -ForegroundColor Yellow
Write-Host "   - Build command: (DEJAR VACÍO)" -ForegroundColor Cyan
Write-Host "   - Publish directory: web" -ForegroundColor Cyan
Write-Host ""
Write-Host "7. Click en 'Deploy site'" -ForegroundColor White
Write-Host ""
Write-Host "8. Espera 2-5 minutos mientras Netlify despliega tu sitio" -ForegroundColor White
Write-Host ""
Write-Host "9. Una vez completado, tu sitio estará disponible en:" -ForegroundColor Yellow
Write-Host "   https://[nombre-aleatorio].netlify.app" -ForegroundColor Cyan
Write-Host ""
Write-Host "10. Puedes cambiar el nombre en:" -ForegroundColor White
Write-Host "    Site settings → Change site name" -ForegroundColor Cyan
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "¡Listo! Tu sitio estará disponible permanentemente" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "NOTAS IMPORTANTES:" -ForegroundColor Yellow
Write-Host "- Cada vez que hagas 'git push', Netlify actualizará automáticamente" -ForegroundColor White
Write-Host "- El sitio es permanente y gratuito" -ForegroundColor White
Write-Host "- Tienes 100 GB/mes de ancho de banda gratis" -ForegroundColor White
Write-Host "- HTTPS está habilitado automáticamente" -ForegroundColor White
Write-Host ""
