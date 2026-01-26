# Solución para Push de Imágenes a GitHub

## Problema
- Tienes 962 imágenes (~2.8 GB) que necesitan estar en GitHub
- El push falla con error HTTP 500 por el tamaño
- Netlify ya está configurado manualmente con `publish = "web"`

## Opciones

### Opción 1: Intentar Push Completo de Nuevo (Recomendado primero)
A veces GitHub tiene problemas temporales. Intenta:

```powershell
cd "D:\PLesion_upch\Fase3_piloto_entrenamientos\callos-annotation-tool"

# Configurar Git para manejar archivos grandes
git config http.postBuffer 524288000
git config http.maxRequestBuffer 100M
git config core.compression 0

# Intentar push completo
git push origin main
```

Si falla, espera 10-15 minutos y vuelve a intentar.

### Opción 2: Usar Git LFS (Large File Storage)
GitHub ofrece Git LFS para archivos grandes:

```powershell
# Instalar Git LFS (si no lo tienes)
# Descargar de: https://git-lfs.github.com/

# Inicializar Git LFS
git lfs install

# Trackear archivos PNG
git lfs track "web/images/*.png"

# Agregar .gitattributes
git add .gitattributes

# Agregar todo
git add web/images/
git commit -m "Agregar imágenes con Git LFS"

# Push
git push origin main
```

### Opción 3: Push Incremental (Más lento pero más seguro)
Hacer push de las imágenes en grupos pequeños:

```powershell
# Primero, hacer push solo de netlify.toml y archivos pequeños
git add netlify.toml web/index.html web/data.js
git commit -m "Agregar configuración Netlify"
git push origin main

# Luego, hacer push de imágenes en grupos de 50
# (Esto requiere un script personalizado)
```

### Opción 4: Usar Netlify Drop (Temporal pero Funcional)
Si solo necesitas que funcione AHORA:

1. Ve a: https://app.netlify.com/drop
2. Arrastra la carpeta `web/` completa
3. Netlify generará una URL temporal
4. **Nota**: Esto es temporal (7 días), pero funciona inmediatamente

### Opción 5: Almacenamiento Externo de Imágenes
1. Subir imágenes a un servicio de almacenamiento (AWS S3, Cloudinary, etc.)
2. Modificar `web/index.html` para cargar imágenes desde URLs externas
3. Esto requiere cambios en el código

## Recomendación Inmediata

**Para que funcione AHORA:**
1. Ve a Netlify → Deploys → Trigger deploy
2. Si el deploy falla porque no encuentra las imágenes, usa **Opción 4 (Netlify Drop)** temporalmente

**Para solución permanente:**
1. Intenta **Opción 1** (push completo) 2-3 veces con intervalos de 10 minutos
2. Si sigue fallando, usa **Opción 2 (Git LFS)**

## Verificar Estado Actual

```powershell
# Ver qué commits están en GitHub
git log origin/main --oneline

# Ver qué commits están solo localmente
git log origin/main..HEAD --oneline

# Ver tamaño del repositorio
git count-objects -vH
```
