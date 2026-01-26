# Deploy en Netlify - Pasos Completos

## Opción 1: Deploy Automático desde GitHub (Recomendado)

Si el push a GitHub se completa exitosamente, Netlify debería detectar automáticamente los cambios y hacer deploy.

1. Ve a: https://app.netlify.com
2. Selecciona tu sitio: `sweet-brigadeiros-5877c2`
3. Ve a la pestaña **Deploys**
4. Deberías ver un nuevo deploy en progreso o completado

## Opción 2: Deploy Manual desde Netlify

Si el push automático no funciona o quieres forzar un deploy:

1. Ve a: https://app.netlify.com
2. Selecciona tu sitio: `sweet-brigadeiros-5877c2`
3. Ve a la pestaña **Deploys**
4. Haz clic en **"Trigger deploy"** → **"Deploy site"**
5. Espera a que termine el deploy (1-2 minutos)

## Opción 3: Deploy desde Netlify CLI (Local)

Si prefieres hacer deploy desde tu máquina local:

```powershell
# Instalar Netlify CLI (si no lo tienes)
npm install -g netlify-cli

# Login en Netlify
netlify login

# Deploy desde la carpeta web/
netlify deploy --prod --dir=web
```

## Verificar que Funcionó

Después del deploy:

1. Abre tu sitio: `https://sweet-brigadeiros-5877c2.netlify.app`
2. Abre la consola del navegador (F12)
3. Ve a la pestaña **Network**
4. Recarga la página
5. Deberías ver que se cargan:
   - `index.html`
   - `data.js`
   - Imágenes desde Firebase Storage (URLs como `https://storage.googleapis.com/...`)

Si ves errores 404 en las imágenes, verifica:
- Que las reglas de Firebase Storage permitan lectura pública de `Revision_de_callos`
- Que `USE_FIREBASE_STORAGE = true` en `web/index.html`
- Que el bucket sea correcto: `foot-selfie---multiplatform.firebasestorage.app`
