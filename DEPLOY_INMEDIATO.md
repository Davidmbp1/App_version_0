# Deploy Inmediato en Netlify - Instrucciones

## El Push a GitHub está fallando (HTTP 500)
Esto es un problema temporal de GitHub. Podemos hacer deploy en Netlify de dos formas:

## Opción 1: Deploy Manual desde Netlify Web (MÁS RÁPIDO)

### Pasos:
1. **Ve a Netlify**: https://app.netlify.com
2. **Selecciona tu sitio**: `sweet-brigadeiros-5877c2`
3. **Ve a "Deploys"** (en el menú izquierdo)
4. **Haz clic en "Trigger deploy"** (botón en la parte superior)
5. **Selecciona "Deploy site"**
6. **Espera 1-2 minutos**

Netlify usará el último commit que tenga en GitHub. Si el push no se completó, puedes usar la Opción 2.

## Opción 2: Deploy desde Netlify CLI (LOCAL)

Si Netlify CLI está instalado, podemos hacer deploy directamente desde tu máquina:

```powershell
# Si no tienes Netlify CLI instalado:
npm install -g netlify-cli

# Login en Netlify (solo la primera vez)
netlify login

# Deploy desde la carpeta web/
netlify deploy --prod --dir=web
```

## Opción 3: Verificar y Forzar Push a GitHub

Si quieres intentar el push de nuevo:

```powershell
# Verificar estado
git status

# Intentar push de nuevo
git push origin main

# Si sigue fallando, espera 10-15 minutos y vuelve a intentar
```

## Verificar que Funcionó

Después del deploy en Netlify:

1. **Abre tu sitio**: https://sweet-brigadeiros-5877c2.netlify.app
2. **Abre la consola del navegador** (F12)
3. **Ve a la pestaña Network**
4. **Recarga la página**
5. **Verifica que se cargan**:
   - ✅ `index.html`
   - ✅ `data.js`
   - ✅ Imágenes desde Firebase Storage (URLs como `https://storage.googleapis.com/...`)

## Si las Imágenes No se Cargan

1. Verifica que `USE_FIREBASE_STORAGE = true` en `web/index.html`
2. Verifica que el bucket sea: `foot-selfie---multiplatform.firebasestorage.app`
3. Verifica las reglas de Firebase Storage (deben permitir lectura pública de `Revision_de_callos`)
