# Guía de Despliegue - Callos Annotation Tool

Esta guía explica cómo desplegar la herramienta de anotación para que los médicos puedan accederla sin necesidad de abrir archivos HTML localmente.

## Opción 1: Servidor Web Local (Recomendado para uso interno) ⭐

### Requisitos
- Python 3.6+ instalado
- Acceso a la red local (misma red WiFi/LAN)

### Pasos

1. **Iniciar el servidor:**
   ```powershell
   # Desde PowerShell en el directorio del proyecto
   python servidor_local.py
   
   # O usar el script PowerShell
   .\servidor_local.ps1
   ```

2. **Acceder desde la misma computadora:**
   - Abre el navegador en: `http://localhost:8000`

3. **Acceder desde otras computadoras en la misma red:**
   - El script mostrará la IP local (ej: `192.168.1.100`)
   - Desde otras computadoras, abre: `http://192.168.1.100:8000`
   - **Importante:** Asegúrate de que el firewall de Windows permita conexiones en el puerto 8000

### Configurar Firewall de Windows

Si otros dispositivos no pueden acceder, ejecuta en PowerShell (como Administrador):

```powershell
New-NetFirewallRule -DisplayName "Callos Annotation Tool" -Direction Inbound -LocalPort 8000 -Protocol TCP -Action Allow
```

### Ventajas
- ✅ No requiere internet
- ✅ Funciona en red local
- ✅ Fácil de configurar
- ✅ Control total sobre los datos

### Desventajas
- ⚠️ El servidor debe estar corriendo mientras se usa
- ⚠️ Solo accesible en la red local

---

## Opción 2: GitHub Pages (Gratis, permanente) ⭐⭐

### ⚠️ Límites de GitHub Pages
- **Repositorios públicos:** 1 GB máximo, 100 GB/mes ancho de banda
- **Repositorios privados:** Requiere GitHub Pro ($4/mes) para Pages privadas
- **Archivo individual:** Máximo 100 MB

**Verifica el tamaño de tus archivos antes de continuar.** Ver `GITHUB_PAGES_LIMITES.md` para más detalles.

### Requisitos
- Cuenta de GitHub
- Git instalado

### Pasos Automatizados (Recomendado)

**Usa el script automatizado:**

```powershell
.\desplegar_github_pages.ps1
```

El script te guiará paso a paso y verificará el tamaño de tus archivos.

### Pasos Manuales

1. **Crear un repositorio en GitHub:**
   - Ve a https://github.com/new
   - Crea un repositorio (puede ser privado)
   - **NO** inicialices con README, .gitignore o licencia

2. **Preparar el repositorio:**
   ```powershell
   # Inicializar git (si no está inicializado)
   git init
   
   # Agregar archivos (solo web/)
   git add web/
   git commit -m "Herramienta de anotación de callos"
   
   # Agregar el remoto de GitHub
   git remote add origin https://github.com/TU_USUARIO/TU_REPOSITORIO.git
   git branch -M main
   git push -u origin main
   ```

3. **Configurar GitHub Pages:**
   - Ve a Settings → Pages en tu repositorio
   - Source: selecciona "main" branch
   - Folder: selecciona "/web"
   - Guarda

4. **Acceder:**
   - Tu herramienta estará disponible en: `https://TU_USUARIO.github.io/TU_REPOSITORIO/`
   - Puede tardar 1-2 minutos en estar disponible

### Nota sobre datos sensibles
⚠️ **IMPORTANTE:** GitHub Pages es público por defecto. Si tus datos son sensibles:
- Usa un repositorio privado (requiere GitHub Pro para Pages privadas)
- O considera otra opción (Netlify con repositorio privado, servidor local)

---

## Opción 3: Netlify (Gratis, permanente) ⭐⭐⭐

### ⚠️ IMPORTANTE: Netlify Drop es TEMPORAL
**Netlify Drop** (https://app.netlify.com/drop) solo mantiene el sitio por **7 días**. Para un despliegue **permanente**, usa la opción con Git.

### Requisitos
- Cuenta de Netlify (gratis en https://www.netlify.com)
- Repositorio Git (GitHub, GitLab, o Bitbucket)

### Pasos para Despliegue PERMANENTE

1. **Crear cuenta en Netlify:**
   - Ve a https://www.netlify.com
   - Regístrate (puedes usar GitHub, Google, etc.)

2. **Subir tu código a Git:**
   ```powershell
   # Si no tienes Git inicializado
   git init
   git add web/
   git commit -m "Herramienta de anotación"
   
   # Crear repositorio en GitHub/GitLab y conectar
   git remote add origin https://github.com/TU_USUARIO/TU_REPO.git
   git push -u origin main
   ```

3. **Conectar con Netlify:**
   - En Netlify, ve a "Add new site" → "Import an existing project"
   - Conecta tu repositorio de Git
   - Configuración:
     - **Build command:** (dejar vacío)
     - **Publish directory:** `web`
   - Click "Deploy site"

4. **Resultado:**
   - Tu sitio estará disponible permanentemente en una URL como: `https://tu-proyecto.netlify.app`
   - Cada vez que hagas `git push`, se actualizará automáticamente

### Ventajas
- ✅ **Permanente** (no expira)
- ✅ Muy fácil de usar
- ✅ HTTPS automático
- ✅ Actualizaciones automáticas desde Git
- ✅ Puede ser privado (con plan pago o repositorio privado)

---

## Opción 4: Vercel (Similar a Netlify)

### Pasos

1. Instala Vercel CLI:
   ```powershell
   npm install -g vercel
   ```

2. Despliega:
   ```powershell
   cd web
   vercel
   ```

3. Sigue las instrucciones en pantalla.

---

## Opción 5: Servidor Interno de la Organización

Si tu organización tiene un servidor web interno:

1. **Sube los archivos:**
   - Copia toda la carpeta `web/` al servidor
   - Asegúrate de mantener la estructura de carpetas

2. **Configurar servidor web:**
   - **Apache:** Coloca `web/` en `htdocs/` o configura un VirtualHost
   - **Nginx:** Configura un server block apuntando a `web/`
   - **IIS:** Crea un sitio web apuntando a `web/`

3. **Acceder:**
   - Los médicos acceden a través de la URL interna del servidor

---

## Comparación Rápida

| Opción | Dificultad | Costo | Acceso | Privacidad |
|--------|-----------|-------|--------|------------|
| Servidor Local | ⭐ Fácil | Gratis | Red local | ✅ Total |
| GitHub Pages | ⭐⭐ Media | Gratis | Internet | ⚠️ Público* |
| Netlify | ⭐ Muy fácil | Gratis | Internet | ⚠️ Público* |
| Vercel | ⭐⭐ Media | Gratis | Internet | ⚠️ Público* |
| Servidor Interno | ⭐⭐⭐ Avanzado | Depende | Red/Internet | ✅ Total |

*Puede ser privado con planes de pago

---

## Recomendación

- **Para uso interno en hospital/clínica:** Opción 1 (Servidor Local) o Opción 5 (Servidor Interno)
- **Para acceso remoto permanente:** Opción 3 (Netlify con Git) o Opción 2 (GitHub Pages)
- **⚠️ NO uses Netlify Drop** - Solo dura 7 días, usa la opción con Git para que sea permanente

---

## Actualizar Datos

Cuando generes nuevas predicciones con `export_predictions_folds.py`:

1. **Servidor Local:** Solo reinicia el servidor (Ctrl+C y vuelve a ejecutar)
2. **GitHub Pages/Netlify/Vercel:** 
   ```powershell
   git add web/
   git commit -m "Actualizar predicciones"
   git push
   ```
   (Se actualizará automáticamente)

---

## Solución de Problemas

### "No se puede acceder desde otras computadoras"
- Verifica que estén en la misma red
- Verifica el firewall de Windows
- Verifica que el servidor muestre la IP correcta

### "Puerto 8000 ya está en uso"
- Cambia el puerto en `servidor_local.py` (línea `PORT = 8000`)
- O cierra la aplicación que usa ese puerto

### "Los datos no se cargan"
- Verifica que `data.js` y las imágenes estén en `web/`
- Abre la consola del navegador (F12) para ver errores
- Verifica que el servidor esté sirviendo desde `web/`
