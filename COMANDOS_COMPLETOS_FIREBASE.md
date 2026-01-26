# Comandos Completos para Configurar Firebase Storage

## ⚠️ IMPORTANTE: Actualizar Reglas de Storage Primero

1. Ve a Firebase Console → Storage → Rules
2. Reemplaza las reglas con el contenido de `REGLAS_FIREBASE_STORAGE.txt`
3. Click **"Publish"**

Esto permitirá acceso público a "Revision de callos" sin afectar el resto de tu bucket.

## 📦 Paso 1: Verificar/Activar Entorno Virtual

**NO necesitas crear un entorno nuevo**, puedes usar el mismo `.venv`:

```powershell
# Navegar al proyecto
cd "D:\PLesion_upch\Fase3_piloto_entrenamientos\callos-annotation-tool"

# Activar el entorno virtual existente
..\.venv\Scripts\activate
```

Si el entorno no existe o hay problemas:
```powershell
# Crear nuevo entorno (solo si es necesario)
python -m venv ..\.venv
..\.venv\Scripts\activate
```

## 📦 Paso 2: Instalar Firebase Admin SDK

```powershell
# Asegúrate de que el entorno esté activado (deberías ver (.venv) al inicio)
pip install firebase-admin
```

## 📦 Paso 3: Obtener Credenciales de Firebase

1. Ve a Firebase Console: https://console.firebase.google.com/
2. Selecciona tu proyecto: **FS-multiplatform**
3. Ve a **Project Settings** (⚙️) → **Service Accounts**
4. Click en **"Generate new private key"**
5. Click **"Generate key"** en el popup
6. Se descargará un archivo JSON (ej: `foot-selfie---multiplatform-firebase-adminsdk-xxxxx.json`)
7. **Mueve o copia** este archivo a: `D:\PLesion_upch\Fase3_piloto_entrenamientos\callos-annotation-tool\backend\firebase-credentials.json`

## 📤 Paso 4: Subir Imágenes a Firebase Storage

```powershell
# Asegúrate de estar en el directorio del proyecto
cd "D:\PLesion_upch\Fase3_piloto_entrenamientos\callos-annotation-tool"

# Verificar que el entorno esté activado
# (deberías ver (.venv) al inicio de la línea)

# Subir imágenes (reemplaza con la ruta real de tu archivo JSON si es diferente)
python backend/upload_images_firebase.py --images-dir "web/images" --firebase-credentials "backend/firebase-credentials.json" --storage-bucket "foot-selfie---multiplatform.firebasestorage.app"
```

**Nota**: Esto subirá las 962 imágenes. Puede tardar 10-30 minutos dependiendo de tu conexión.

## 📄 Paso 5: ¿Subir data.js?

**NO es necesario subir `data.js` a Firebase Storage** porque:
- ✅ Es un archivo pequeño (~8.8 MB de texto)
- ✅ Puede ir en GitHub/Netlify sin problemas
- ✅ Se carga rápido desde Netlify
- ✅ Solo las imágenes necesitan Firebase Storage (son 2.8 GB)

**Solo necesitas subir las imágenes**, `data.js` se queda en el repositorio.

## ✅ Paso 6: Verificar que Funcionó

1. Ve a Firebase Console → **Storage** → **Files**
2. Deberías ver la carpeta **"Revision de callos"** con todas las imágenes
3. Haz clic en una imagen para ver su URL pública
4. Abre `web/index.html` en tu navegador y verifica que las imágenes se cargan

## 🚀 Paso 7: Hacer Push a GitHub (Sin Imágenes)

```powershell
# Agregar solo los archivos de código
git add web/index.html backend/upload_images_firebase.py backend/requirements.txt .gitignore REGLAS_FIREBASE_STORAGE.txt COMANDOS_COMPLETOS_FIREBASE.md

# Commit
git commit -m "Configurar Firebase Storage para imágenes - usar carpeta Revision de callos"

# Push (ahora será rápido, sin imágenes)
git push origin main
```

## 📋 Checklist Completo

- [ ] Reglas de Storage actualizadas (incluir "Revision de callos" con acceso público)
- [ ] Entorno virtual activado
- [ ] Firebase Admin SDK instalado (`pip install firebase-admin`)
- [ ] Credenciales descargadas y guardadas en `backend/firebase-credentials.json`
- [ ] Imágenes subidas a Firebase Storage (carpeta "Revision de callos")
- [ ] Verificado que las imágenes están en Firebase Console
- [ ] Probado localmente que las imágenes se cargan en `web/index.html`
- [ ] Push a GitHub (sin imágenes)
- [ ] Deploy en Netlify exitoso

## 🐛 Solución de Problemas

### Error: "No se encontró el archivo de credenciales"
```powershell
# Verificar que el archivo existe
Test-Path "backend/firebase-credentials.json"

# Si no existe, verifica la ruta donde descargaste el JSON de Firebase
```

### Error: "Permission denied" al subir
- Verifica que las reglas de Storage permitan escritura temporalmente
- O sube manualmente desde Firebase Console → Storage → Upload file

### Error: "ModuleNotFoundError: No module named 'firebase_admin'"
```powershell
# Asegúrate de que el entorno esté activado
..\.venv\Scripts\activate

# Reinstalar
pip install firebase-admin
```

### Las imágenes no se cargan en el navegador
1. Verifica que `USE_FIREBASE_STORAGE = true` en `web/index.html`
2. Verifica que el bucket sea correcto: `foot-selfie---multiplatform.firebasestorage.app`
3. Abre la consola del navegador (F12) para ver errores
4. Verifica que las imágenes estén en Firebase Storage → Files → "Revision de callos"
5. Verifica que las reglas de Storage permitan lectura pública de "Revision de callos"
