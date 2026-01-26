# Deploy Inmediato en Netlify

## Pasos para Deploy Manual en Netlify

### Paso 1: Ir a Netlify
1. Abre: https://app.netlify.com
2. Inicia sesión si es necesario
3. Selecciona tu sitio: **sweet-brigadeiros-5877c2**

### Paso 2: Trigger Deploy Manual
1. En el menú izquierdo, haz clic en **"Deploys"**
2. En la parte superior, busca el botón **"Trigger deploy"**
3. Haz clic en **"Trigger deploy"** → **"Deploy site"**
4. Espera 1-2 minutos mientras Netlify hace el deploy

### Paso 3: Verificar Configuración
Antes del deploy, verifica que la configuración esté correcta:

1. Ve a **Site settings** → **Build & deploy** → **Build settings**
2. Verifica:
   - **Publish directory**: `web` (debe estar configurado)
   - **Build command**: (debe estar vacío)

### Paso 4: Verificar el Deploy
Después del deploy:

1. Ve a la pestaña **Deploys**
2. Haz clic en el deploy más reciente
3. En **"Deploy file browser"**, deberías ver:
   ```
   web/
   ├── index.html
   ├── data.js
   └── (NO deberías ver web/images/ porque está en .gitignore)
   ```

### Paso 5: Probar el Sitio
1. Abre: `https://sweet-brigadeiros-5877c2.netlify.app`
2. Abre la consola del navegador (F12)
3. Verifica que las imágenes se cargan desde Firebase Storage
4. Las URLs deberían ser: `https://storage.googleapis.com/foot-selfie---multiplatform.firebasestorage.app/Revision_de_callos/...`

## Si el Deploy Falla

### Error: "No se encontraron archivos"
- Verifica que `netlify.toml` esté en el repositorio con `publish = "web"`
- O configura manualmente en Netlify: **Site settings** → **Build & deploy** → **Publish directory**: `web`

### Error: "Las imágenes no se cargan"
- Verifica que `USE_FIREBASE_STORAGE = true` en `web/index.html`
- Verifica que el bucket sea correcto: `foot-selfie---multiplatform.firebasestorage.app`
- Verifica las reglas de Firebase Storage (deben permitir lectura pública de `Revision_de_callos`)

## Alternativa: Deploy desde Netlify CLI

Si prefieres hacer deploy desde tu máquina local:

```powershell
# Instalar Netlify CLI (si no lo tienes)
npm install -g netlify-cli

# Login
netlify login

# Deploy
cd "D:\PLesion_upch\Fase3_piloto_entrenamientos\callos-annotation-tool"
netlify deploy --prod --dir=web
```
