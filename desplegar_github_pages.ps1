# Script para desplegar en GitHub Pages automáticamente
# Uso: .\desplegar_github_pages.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Despliegue en GitHub Pages" -ForegroundColor Cyan
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

# Verificar tamaño de archivos
Write-Host "[INFO] Verificando tamaño de archivos..." -ForegroundColor Yellow
$imagesSize = (Get-ChildItem -Path "web\images" -File -Recurse | Measure-Object -Property Length -Sum).Sum / 1MB
$dataJsSize = if (Test-Path "web\data.js") { (Get-Item "web\data.js").Length / 1MB } else { 0 }
$totalSize = $imagesSize + $dataJsSize

Write-Host "  - Imágenes: $([math]::Round($imagesSize, 2)) MB" -ForegroundColor Cyan
Write-Host "  - data.js: $([math]::Round($dataJsSize, 2)) MB" -ForegroundColor Cyan
Write-Host "  - Total: $([math]::Round($totalSize, 2)) MB" -ForegroundColor Cyan
Write-Host ""

if ($totalSize -gt 1000) {
    Write-Host "[ADVERTENCIA] El tamaño total es mayor a 1GB" -ForegroundColor Yellow
    Write-Host "             GitHub Pages tiene límites de almacenamiento." -ForegroundColor Yellow
    Write-Host "             Considera usar Netlify o Vercel para proyectos grandes." -ForegroundColor Yellow
    Write-Host ""
    $continue = Read-Host "¿Continuar de todas formas? (s/n)"
    if ($continue -ne "s") {
        exit 0
    }
}

# Verificar si ya es un repositorio Git
$isGitRepo = Test-Path ".git"

if (-not $isGitRepo) {
    Write-Host "[INFO] Inicializando repositorio Git..." -ForegroundColor Yellow
    git init
    Write-Host "[OK] Repositorio inicializado" -ForegroundColor Green
} else {
    Write-Host "[OK] Repositorio Git ya existe" -ForegroundColor Green
}

# Preguntar por el repositorio remoto
Write-Host ""
Write-Host "¿Ya tienes un repositorio en GitHub creado?" -ForegroundColor Yellow
Write-Host "1. Sí, ya lo creé"
Write-Host "2. No, necesito crearlo primero"
$opcion = Read-Host "Selecciona (1 o 2)"

if ($opcion -eq "2") {
    Write-Host ""
    Write-Host "Pasos para crear el repositorio:" -ForegroundColor Cyan
    Write-Host "1. Ve a https://github.com/new" -ForegroundColor White
    Write-Host "2. Crea un repositorio nuevo" -ForegroundColor White
    Write-Host "3. NO inicialices con README, .gitignore o licencia" -ForegroundColor White
    Write-Host "4. Puede ser público o privado (privado requiere GitHub Pro para Pages)" -ForegroundColor White
    Write-Host ""
    $continuar = Read-Host "Presiona Enter cuando hayas creado el repositorio..."
}

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

# Backend (opcional, puedes incluir si quieres)
# backend/

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

# Agregar archivos
Write-Host ""
Write-Host "[INFO] Agregando archivos..." -ForegroundColor Yellow
git add web/
git add .gitignore
git add README.md
git add DESPLIEGUE.md

# Verificar si hay cambios
$status = git status --porcelain
if ([string]::IsNullOrWhiteSpace($status)) {
    Write-Host "[INFO] No hay cambios nuevos para commitear" -ForegroundColor Yellow
} else {
    Write-Host "[INFO] Haciendo commit..." -ForegroundColor Yellow
    git commit -m "Desplegar herramienta de anotación de callos en GitHub Pages"
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
$hacerPush = Read-Host "¿Deseas hacer push al repositorio ahora? (s/n)"

if ($hacerPush -eq "s") {
    Write-Host "[INFO] Haciendo push..." -ForegroundColor Yellow
    try {
        git push -u origin $currentBranch
        Write-Host "[OK] Push completado" -ForegroundColor Green
    } catch {
        Write-Host "[ERROR] Error al hacer push" -ForegroundColor Red
        Write-Host "       Asegúrate de tener permisos y que el repositorio exista" -ForegroundColor Yellow
        exit 1
    }
}

# Instrucciones para configurar GitHub Pages
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "SIGUIENTE PASO: Configurar GitHub Pages" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "1. Ve a tu repositorio en GitHub: $repoUrl" -ForegroundColor White
Write-Host "2. Click en 'Settings' (Configuración)" -ForegroundColor White
Write-Host "3. En el menú lateral, click en 'Pages'" -ForegroundColor White
Write-Host "4. En 'Source', selecciona:" -ForegroundColor White
Write-Host "   - Branch: $currentBranch" -ForegroundColor Cyan
Write-Host "   - Folder: /web" -ForegroundColor Cyan
Write-Host "5. Click 'Save'" -ForegroundColor White
Write-Host ""
Write-Host "Tu sitio estará disponible en:" -ForegroundColor Yellow
$repoName = $repoUrl -replace ".*github.com/", "" -replace "\.git$", ""
$pagesUrl = "https://$($repoName -replace '/', '.github.io/')"
Write-Host "   $pagesUrl" -ForegroundColor Cyan
Write-Host ""
Write-Host "NOTA: Puede tardar 1-2 minutos en estar disponible" -ForegroundColor Yellow
Write-Host ""
