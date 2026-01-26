# 🔧 Solución: Netlify No Reconoce la Carpeta web/

## Problema

Netlify está desplegando desde la **raíz** del repositorio y solo muestra 3 archivos:
- index.html
- license  
- readme.md

**Faltan:**
- ❌ `web/images/` (962 imágenes)
- ❌ `web/data.js` (134 MB)
- ❌ `web/index.html` (el correcto)

## Causa

1. **La carpeta `web/` NO está en el repositorio Git**
2. **Netlify no está configurado para usar `web/` como publish directory**

## Solución Paso a Paso

### Paso 1: Agregar la carpeta web/ al repositorio

```powershell
# Verificar que web/ existe localmente
Test-Path "web/index.html"  # Debe ser True

# Agregar toda la carpeta web/
git add web/

# Ver qué se va a agregar (primeros 10 archivos)
git status --short | Select-Object -First 10

# Hacer commit
git commit -m "Agregar carpeta web completa con imágenes y data.js"

# Hacer push (esto puede tardar varios minutos por el tamaño)
git push
```

⚠️ **IMPORTANTE:** El push puede tardar 10-30 minutos porque son 2.8 GB de datos.

### Paso 2: Configurar Netlify

**Opción A: Usar netlify.toml (Recomendado)**

Ya creé el archivo `netlify.toml`. Agrégalo al repositorio:

```powershell
git add netlify.toml
git commit -m "Configurar Netlify para usar carpeta web/"
git push
```

**Opción B: Configurar en la interfaz de Netlify**

1. Ve a https://app.netlify.com
2. Selecciona tu sitio: `sweet-brigadeiros-5877c2`
3. **Site settings** → **Build & deploy** → **Build settings**
4. Edita:
   - **Publish directory**: `web` (antes estaba vacío)
   - **Build command**: (dejar vacío)
5. **Save**
6. **Deploys** → **Trigger deploy** → **Deploy site**

### Paso 3: Verificar el Deploy

Después del deploy, en **Deploy file browser** deberías ver:

```
web/
├── index.html (1,410 líneas)
├── data.js (8,868,792 líneas)
└── images/
    ├── IMG_001.png
    ├── IMG_002.png
    └── ... (962 archivos)
```

## Comandos Completos (Copia y Pega)

```powershell
# 1. Agregar netlify.toml
git add netlify.toml
git commit -m "Configurar Netlify"

# 2. Agregar carpeta web/ completa
git add web/
git commit -m "Agregar carpeta web con imágenes y data.js"

# 3. Hacer push (tardará varios minutos)
git push

# 4. Esperar a que termine el push
# 5. En Netlify, hacer nuevo deploy manual si es necesario
```

## Verificación

### Verificar qué está en el repositorio

```powershell
# Ver archivos en web/
git ls-files web/ | Measure-Object -Line

# Debe mostrar aproximadamente 964 líneas (962 imágenes + index.html + data.js)
```

### Verificar tamaño

```powershell
python verificar_tamano.py
```

## Si el Push Falla

### Error: "File too large"

Si GitHub rechaza archivos > 100 MB:

1. **data.js es 134 MB** - Puede ser rechazado
2. **Solución:** Usar Git LFS (Large File Storage)

```powershell
# Instalar Git LFS
git lfs install

# Rastrear data.js con LFS
git lfs track "web/data.js"
git add .gitattributes
git add web/data.js
git commit -m "Usar Git LFS para data.js"
git push
```

### Error: "Push timeout"

Si el push tarda mucho o se cae:

```powershell
# Hacer push en partes más pequeñas
# Primero solo netlify.toml
git add netlify.toml
git commit -m "Configurar Netlify"
git push

# Luego web/index.html
git add web/index.html
git commit -m "Agregar index.html"
git push

# Luego las imágenes (esto puede tardar)
git add web/images/
git commit -m "Agregar imágenes"
git push

# Finalmente data.js (puede necesitar LFS)
git add web/data.js
git commit -m "Agregar data.js"
git push
```

## Resultado Final

Una vez corregido, tu sitio en Netlify debería:
- ✅ Mostrar todas las imágenes
- ✅ Cargar data.js correctamente  
- ✅ Funcionar completamente

URL: `https://sweet-brigadeiros-5877c2.netlify.app`

## ¿Necesitas Ayuda?

Si tienes algún error durante el proceso, comparte:
1. El mensaje de error completo
2. El resultado de `git status`
3. El resultado de `python verificar_tamano.py`
