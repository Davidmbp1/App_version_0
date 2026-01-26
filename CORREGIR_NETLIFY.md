# Corregir Configuración de Netlify

## Problema Detectado

Netlify está desplegando desde la **raíz del repositorio** en lugar de la carpeta `web/`. Por eso solo ves 3 archivos (index.html, license, readme.md) en lugar de todas las imágenes y data.js.

## Solución Rápida

### Opción 1: Configurar en la Interfaz de Netlify (Más Rápido)

1. Ve a tu sitio en Netlify: https://app.netlify.com
2. Selecciona tu sitio: `sweet-brigadeiros-5877c2`
3. Ve a **Site settings** → **Build & deploy** → **Build settings**
4. En la sección **Build settings**, busca:
   - **Publish directory**: Cambia de (vacío) a `web`
   - **Build command**: Déjalo vacío
5. Click en **Save**
6. Ve a **Deploys** y haz click en **Trigger deploy** → **Deploy site**

### Opción 2: Usar archivo netlify.toml (Recomendado)

Ya he creado el archivo `netlify.toml` en tu proyecto. Ahora:

1. **Agregar el archivo al repositorio:**
   ```powershell
   git add netlify.toml
   git commit -m "Agregar configuración de Netlify"
   git push
   ```

2. **Netlify detectará automáticamente** el archivo y usará la configuración.

3. **Hacer un nuevo deploy:**
   - Ve a Netlify → Deploys
   - Click en **Trigger deploy** → **Deploy site**

## Verificación

Después de corregir, deberías ver en el deploy:

```
Deploy file browser:
web/
├── index.html
├── data.js
└── images/
    ├── IMG_001.png
    ├── IMG_002.png
    └── ... (962 imágenes)
```

## Si Aún No Funciona

### Verificar qué se subió al repositorio

```powershell
# Ver qué archivos están en el repositorio
git ls-files

# Verificar que web/ esté incluido
git ls-files web/
```

### Si web/ no está en el repositorio

```powershell
# Agregar la carpeta web/
git add web/
git commit -m "Agregar carpeta web con imágenes y data.js"
git push
```

### Verificar tamaño del push

Si el push falló por tamaño, verifica:

```powershell
# Ver tamaño de lo que se va a subir
python verificar_tamano.py
```

Si es muy grande, GitHub puede rechazar el push. En ese caso:
- Usa Git LFS para las imágenes grandes
- O comprime las imágenes antes de subir

## Comandos Completos para Corregir

```powershell
# 1. Agregar netlify.toml
git add netlify.toml
git commit -m "Configurar Netlify para usar carpeta web/"

# 2. Verificar que web/ esté en el repositorio
git ls-files web/ | Select-Object -First 10

# 3. Si no está, agregarlo
git add web/
git commit -m "Agregar carpeta web completa"
git push

# 4. En Netlify, hacer nuevo deploy
# Ve a Deploys → Trigger deploy → Deploy site
```

## Resultado Esperado

Después de corregir, tu sitio debería:
- ✅ Mostrar todas las imágenes
- ✅ Cargar data.js correctamente
- ✅ Funcionar completamente

Tu URL será: `https://sweet-brigadeiros-5877c2.netlify.app`
