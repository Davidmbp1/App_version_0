# Instrucciones para Deploy en Netlify

## ⚠️ El Push a GitHub está fallando (HTTP 500)
Esto es un problema temporal de GitHub. Podemos hacer deploy en Netlify de forma manual.

## 🚀 Deploy Manual en Netlify (RECOMENDADO)

### Paso 1: Ir a Netlify
1. Abre tu navegador
2. Ve a: **https://app.netlify.com**
3. Inicia sesión si es necesario
4. Selecciona tu sitio: **sweet-brigadeiros-5877c2**

### Paso 2: Trigger Deploy Manual
1. En el menú izquierdo, haz clic en **"Deploys"**
2. En la parte superior derecha, busca el botón **"Trigger deploy"**
3. Haz clic en **"Trigger deploy"** → **"Deploy site"**
4. Espera 1-2 minutos mientras Netlify hace el deploy

**Nota**: Si el push a GitHub no se completó, Netlify usará el último commit que tenga. Si necesitas los cambios más recientes, puedes hacer deploy desde Netlify CLI (ver abajo).

### Paso 3: Verificar Configuración
Antes del deploy, verifica:

1. Ve a **Site settings** → **Build & deploy** → **Build settings**
2. Verifica:
   - **Publish directory**: `web` ✅
   - **Build command**: (vacío) ✅

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
1. Abre: **https://sweet-brigadeiros-5877c2.netlify.app**
2. Abre la consola del navegador (F12)
3. Ve a la pestaña **Network**
4. Recarga la página
5. Verifica que se cargan:
   - ✅ `index.html`
   - ✅ `data.js`
   - ✅ Imágenes desde Firebase Storage

## 🔧 Si el Push a GitHub se Completa Más Tarde

Si el push a GitHub se completa exitosamente más tarde:

1. Netlify detectará automáticamente los cambios
2. Hará un nuevo deploy automáticamente
3. No necesitas hacer nada más

## ✅ Checklist Final

- [ ] Deploy manual ejecutado en Netlify
- [ ] Sitio funciona: https://sweet-brigadeiros-5877c2.netlify.app
- [ ] Las imágenes se cargan desde Firebase Storage
- [ ] No hay errores 404 en la consola del navegador
- [ ] El push a GitHub se completará más tarde (opcional)
