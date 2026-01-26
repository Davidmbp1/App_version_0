# Desplegar en Netlify de Forma Permanente

## ⚠️ Importante: Netlify Drop es TEMPORAL

**Netlify Drop** (https://app.netlify.com/drop) solo mantiene tu sitio por **7 días**. Después de eso, se elimina automáticamente.

Para un despliegue **permanente y gratuito**, sigue estos pasos:

## 🚀 Inicio Rápido (Automático)

**Usa el script automatizado:**

```powershell
.\desplegar_netlify.ps1
```

El script te guiará paso a paso y preparará todo automáticamente.

## Pasos para Despliegue Permanente

### Opción A: Script Automatizado (Recomendado) ⭐

```powershell
.\desplegar_netlify.ps1
```

El script te guiará paso a paso y hará todo automáticamente.

### Opción B: Pasos Manuales

#### 1. Crear Repositorio en GitHub

Si no tienes GitHub, puedes usar GitLab o Bitbucket también.

1. Ve a https://github.com/new
2. Crea un repositorio nuevo (puede ser privado)
3. **NO** inicialices con README, .gitignore o licencia

#### 2. Subir tu Código a GitHub

```powershell
# En el directorio del proyecto
git init

# Agregar solo la carpeta web (o todo el proyecto si prefieres)
git add web/
git commit -m "Herramienta de anotación de callos"

# Conectar con GitHub (reemplaza con tu URL)
git remote add origin https://github.com/TU_USUARIO/TU_REPOSITORIO.git
git branch -M main
git push -u origin main
```

#### 3. Conectar Netlify con GitHub

1. Ve a https://www.netlify.com y crea una cuenta (gratis)
   - Puedes usar "Sign up with GitHub" para login rápido
2. Click en "Add new site" → "Import an existing project"
3. Selecciona "GitHub" y autoriza Netlify
   - Si es la primera vez, te pedirá permisos
   - Autoriza el acceso a tus repositorios
4. Busca y selecciona tu repositorio
5. **Configuración IMPORTANTE:**
   - **Build command:** (DEJAR VACÍO - no necesitas build)
   - **Publish directory:** `web` (sin barra al final)
6. Click "Deploy site"
7. Espera 2-5 minutos mientras Netlify despliega

### 4. ¡Listo!

Tu sitio estará disponible permanentemente en:
- URL automática: `https://tu-proyecto-aleatorio.netlify.app`
- Puedes cambiar el nombre en Settings → Site details → Change site name

## Actualizar el Sitio

Cada vez que generes nuevas predicciones:

```powershell
# Actualizar los archivos en web/
git add web/
git commit -m "Actualizar predicciones"
git push
```

Netlify detectará el cambio y actualizará automáticamente en 1-2 minutos.

## Hacer el Sitio Privado

### Opción A: Repositorio Privado
- Haz tu repositorio de GitHub privado
- Netlify seguirá funcionando, pero solo tú verás el código

### Opción B: Protección con Contraseña (Netlify Pro)
- Requiere plan de pago de Netlify
- Puedes proteger el sitio con contraseña

### Opción C: Usar otra plataforma
- GitHub Pages con repositorio privado (requiere GitHub Pro)
- O usar el servidor local (Opción 1)

## Ventajas de este Método

✅ **Permanente** - No expira nunca  
✅ **Gratis** - Plan gratuito de Netlify es suficiente  
✅ **Automático** - Se actualiza solo cuando haces `git push`  
✅ **HTTPS** - Certificado SSL automático  
✅ **Rápido** - CDN global de Netlify  

## Alternativas Permanentes

Si prefieres no usar Netlify:

1. **GitHub Pages** - Ver `DESPLIEGUE.md` Opción 2
2. **Vercel** - Similar a Netlify, también permanente
3. **Servidor Local** - Opción 1 en `DESPLIEGUE.md`
