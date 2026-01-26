# Pasos para Configurar Firebase Storage con Tu Proyecto

## ✅ Ya Tienes Configurado:
- ✅ Proyecto: **FS-multiplatform**
- ✅ Bucket: **foot-selfie---multiplatform.firebasestorage.app**
- ✅ Carpeta creada: **"Revision de callos"**

## 📋 Pasos Restantes:

### Paso 1: Configurar Reglas de Storage (2 minutos)

1. Ve a Firebase Console: https://console.firebase.google.com/
2. Selecciona tu proyecto: **FS-multiplatform**
3. Ve a **Storage** → **Rules**
4. Reemplaza las reglas con:
```javascript
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    match /Revision de callos/{imageName} {
      allow read: if true;  // Permite lectura pública (sin autenticación)
      allow write: if false; // Solo tú puedes escribir
    }
  }
}
```
5. Click **"Publish"**

### Paso 2: Obtener Credenciales para Subir Imágenes (3 minutos)

1. En Firebase Console, ve a **Project Settings** (⚙️) → **Service Accounts**
2. Click en **"Generate new private key"**
3. Click **"Generate key"** en el popup
4. Se descargará un archivo JSON (ej: `foot-selfie---multiplatform-firebase-adminsdk-xxxxx.json`)
5. **Guarda este archivo** en: `backend/firebase-credentials.json`

### Paso 3: Instalar Firebase Admin SDK

```powershell
# Activar entorno virtual
cd "D:\PLesion_upch\Fase3_piloto_entrenamientos\callos-annotation-tool"
..\.venv\Scripts\activate

# Instalar Firebase Admin SDK
pip install firebase-admin
```

### Paso 4: Subir Imágenes a Firebase Storage (10-30 minutos)

```powershell
# Asegúrate de estar en el directorio del proyecto
cd "D:\PLesion_upch\Fase3_piloto_entrenamientos\callos-annotation-tool"

# Subir imágenes (reemplaza con la ruta real de tu archivo JSON)
python backend/upload_images_firebase.py --images-dir "web/images" --firebase-credentials "backend/firebase-credentials.json" --storage-bucket "foot-selfie---multiplatform.firebasestorage.app"
```

**Nota**: Esto subirá las 962 imágenes a la carpeta "Revision de callos" en Firebase Storage. Puede tardar 10-30 minutos dependiendo de tu conexión.

### Paso 5: Verificar que las Imágenes se Subieron

1. Ve a Firebase Console → **Storage** → **Files**
2. Deberías ver la carpeta **"Revision de callos"** con todas las imágenes
3. Haz clic en una imagen para ver su URL pública

### Paso 6: Probar Localmente

1. Abre `web/index.html` en tu navegador
2. Verifica que las imágenes se cargan correctamente
3. Abre la consola del navegador (F12) y verifica que no hay errores 404

### Paso 7: Hacer Push a GitHub (Ahora será rápido, sin imágenes)

```powershell
# Agregar solo los archivos de código (sin imágenes)
git add web/index.html backend/upload_images_firebase.py backend/requirements.txt .gitignore
git commit -m "Configurar Firebase Storage para imágenes"
git push origin main
```

**Nota**: Asegúrate de que `web/images/` esté en `.gitignore` para no subir las imágenes a GitHub.

### Paso 8: Desplegar en Netlify

1. Netlify detectará automáticamente los cambios
2. El deploy será mucho más rápido (solo HTML/JS, no imágenes)
3. Las imágenes se cargarán desde Firebase Storage

## ✅ Checklist

- [ ] Reglas de Storage configuradas (lectura pública)
- [ ] Credenciales descargadas y guardadas en `backend/firebase-credentials.json`
- [ ] Firebase Admin SDK instalado (`pip install firebase-admin`)
- [ ] Imágenes subidas a Firebase Storage (carpeta "Revision de callos")
- [ ] Verificado que las imágenes están en Firebase Console
- [ ] Probado localmente que las imágenes se cargan
- [ ] Push a GitHub (sin imágenes)
- [ ] Deploy en Netlify exitoso

## 🎉 ¡Listo!

Ahora tu herramienta funciona con Firebase Storage:
- ✅ GitHub: Solo código (liviano)
- ✅ Netlify: Deploy rápido
- ✅ Firebase: Almacena y sirve las imágenes desde "Revision de callos"
- ✅ Todo funciona igual que antes, solo cambia dónde están las imágenes

## 🔍 Verificar URLs

Las imágenes estarán disponibles en:
```
https://storage.googleapis.com/foot-selfie---multiplatform.firebasestorage.app/Revision%20de%20callos/[nombre_imagen].png
```

Ejemplo:
```
https://storage.googleapis.com/foot-selfie---multiplatform.firebasestorage.app/Revision%20de%20callos/IMG_DMpersonal_DM136_izquierdo_Pie_Completo_1714472702.png
```
