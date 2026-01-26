# Verificar y Corregir Netlify

## Estado Actual

El mensaje "Everything up-to-date" sugiere que los commits ya están en GitHub, aunque hubo un error HTTP 500 (puede ser temporal).

## Pasos para Verificar y Corregir

### Paso 1: Verificar en GitHub

1. Ve a: https://github.com/Davidmbp1/App_version_0
2. Verifica que existan estos archivos:
   - ✅ `netlify.toml` (en la raíz)
   - ✅ `web/index.html`
   - ✅ `web/data.js`
   - ✅ `web/images/` (carpeta con 962 imágenes)

### Paso 2: Verificar en Netlify

1. Ve a: https://app.netlify.com
2. Selecciona tu sitio: `sweet-brigadeiros-5877c2`
3. Ve a **Site settings** → **Build & deploy** → **Build settings**
4. Verifica la configuración:
   - **Publish directory**: Debe decir `web`
   - **Build command**: Debe estar vacío

### Paso 3: Si netlify.toml NO está en GitHub

Si no ves `netlify.toml` en GitHub, intenta hacer push de nuevo:

```powershell
# Verificar que netlify.toml existe localmente
Test-Path "netlify.toml"

# Si existe, agregarlo y hacer push
git add netlify.toml
git commit -m "Agregar netlify.toml"
git push origin main
```

Si el push falla por error HTTP 500, espera 5-10 minutos y vuelve a intentar.

### Paso 4: Si netlify.toml SÍ está en GitHub pero Netlify no lo detecta

**Configurar manualmente en Netlify:**

1. Ve a **Site settings** → **Build & deploy** → **Build settings**
2. Click en **Edit settings**
3. Cambia:
   - **Publish directory**: `web` (antes estaba vacío)
   - **Build command**: (dejar vacío)
4. **Save**
5. Ve a **Deploys** → **Trigger deploy** → **Deploy site**

### Paso 5: Verificar el Deploy

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

**NO deberías ver:**
- ❌ `index.html` en la raíz (ese es el viejo)
- ❌ Solo 3 archivos (license, readme.md, index.html)

## Solución Rápida (Si Todo Falla)

Si nada funciona, configura manualmente:

1. **Netlify** → Tu sitio → **Site settings**
2. **Build & deploy** → **Build settings** → **Edit**
3. **Publish directory**: `web`
4. **Save**
5. **Deploys** → **Trigger deploy** → **Deploy site**

## Verificar que Funciona

Una vez que el deploy esté correcto:

1. Abre tu sitio: `https://sweet-brigadeiros-5877c2.netlify.app`
2. Abre la consola del navegador (F12)
3. Ve a la pestaña **Network**
4. Recarga la página
5. Deberías ver que se cargan:
   - `index.html`
   - `data.js`
   - `images/IMG_XXX.png` (las imágenes)

Si ves errores 404 en las imágenes, significa que Netlify aún no está usando la carpeta `web/` correctamente.

## Comandos Útiles

```powershell
# Ver qué archivos están en el repositorio
git ls-files | Select-String "netlify.toml"
git ls-files web/ | Measure-Object -Line

# Ver commits locales vs remotos
git log --oneline origin/main..HEAD

# Forzar push (solo si es necesario y sabes lo que haces)
# git push --force origin main  # ⚠️ CUIDADO: Solo si es absolutamente necesario
```
